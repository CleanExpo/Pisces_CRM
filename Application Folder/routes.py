from flask import render_template, request, jsonify, redirect, url_for
from flask_socketio import emit, join_room, leave_room
from extensions import db
from models import User, Inspection, InspectionStep, InspectionData, SSRA, GridMap
from ai_processing import process_input, generate_comprehensive_report
from insurance_integration import InsuranceIntegration, format_inspection_for_claim
import json

def register_routes(app, socketio):
    @app.route('/inspection/<int:inspection_id>')
    def inspection(inspection_id):
        inspection = Inspection.query.get_or_404(inspection_id)
        steps = InspectionStep.query.filter_by(inspection_id=inspection_id).all()
        ssra_data = SSRA.query.filter_by(inspection_id=inspection_id).all()
        grid_map = GridMap.query.filter_by(inspection_id=inspection_id).first()
        return render_template('inspection.html', inspection=inspection, steps=steps, ssra_data=ssra_data, grid_map=grid_map)

    @app.route('/submit_claim/<int:inspection_id>', methods=['POST'])
    def submit_claim(inspection_id):
        inspection = Inspection.query.get_or_404(inspection_id)
        insurance_integration = InsuranceIntegration()
        
        inspection_data = format_inspection_for_claim(inspection)
        prepared_claim = insurance_integration.prepare_claim_data(inspection_data)
        
        result = insurance_integration.store_claim_in_crm(prepared_claim)
        
        if result:
            return jsonify({'message': 'Claim data stored in CRM successfully', 'crm_reference': result.get('reference_id')}), 200
        else:
            return jsonify({'message': 'Failed to store claim data in CRM'}), 500

    @app.route('/test_submit_claim/<int:inspection_id>')
    def test_submit_claim(inspection_id):
        inspection = Inspection.query.get_or_404(inspection_id)
        insurance_integration = InsuranceIntegration()
        
        inspection_data = format_inspection_for_claim(inspection)
        result = insurance_integration.submit_claim(inspection_data)
        
        if result:
            return jsonify({'message': 'Test claim submitted successfully', 'claim_id': result.get('claim_id')}), 200
        else:
            return jsonify({'message': 'Failed to submit test claim'}), 500

    @socketio.on('join')
    def on_join(data):
        inspection_id = data['inspection_id']
        technician_name = data.get('technician_name', 'A technician')
        join_room(f'inspection_{inspection_id}')
        emit('user_joined', {'message': f'{technician_name} joined the inspection.', 'technician_name': technician_name}, to=f'inspection_{inspection_id}')

    @socketio.on('leave')
    def on_leave(data):
        inspection_id = data['inspection_id']
        technician_name = data.get('technician_name', 'A technician')
        leave_room(f'inspection_{inspection_id}')
        emit('user_left', {'message': f'{technician_name} left the inspection.', 'technician_name': technician_name}, to=f'inspection_{inspection_id}')

    @socketio.on('chat_message')
    def handle_chat_message(data):
        inspection_id = data['inspection_id']
        message = data['message']
        technician_name = data.get('technician_name', 'Technician')
        emit('new_chat_message', {'sender': technician_name, 'message': message}, to=f'inspection_{inspection_id}')

    @socketio.on('typing')
    def handle_typing(data):
        inspection_id = data['inspection_id']
        technician_name = data.get('technician_name', 'A technician')
        is_typing = data['is_typing']
        emit('technician_typing', {'technician_name': technician_name, 'is_typing': is_typing}, to=f'inspection_{inspection_id}', include_self=False)

    @socketio.on('working_on_step')
    def handle_working_on_step(data):
        inspection_id = data['inspection_id']
        step_id = data['step_id']
        technician_name = data.get('technician_name', 'A technician')
        emit('technician_working', {'technician_name': technician_name, 'step_id': step_id}, to=f'inspection_{inspection_id}')

    @socketio.on('step_completed')
    def handle_step_completed(data):
        inspection_id = data['inspection_id']
        step_id = data['step_id']
        technician_name = data.get('technician_name', 'A technician')
        emit('step_completed', {'technician_name': technician_name, 'step_id': step_id}, to=f'inspection_{inspection_id}')

    @socketio.on('submit_inspection_data')
    def handle_submit_inspection_data(data):
        inspection_id = data['inspection_id']
        step_id = data['step_id']
        data_type = data['data_type']
        data_content = data['data_content']
        technician_name = data.get('technician_name', 'A technician')
        
        ai_interpretation = process_input(data_type, data_content, f"Inspection {inspection_id}, Step {step_id}")
        
        inspection_data = InspectionData(inspection_id=inspection_id, step_id=step_id, data_type=data_type, data_content=data_content, ai_interpretation=ai_interpretation)
        db.session.add(inspection_data)
        db.session.commit()
        
        emit('inspection_data_update', {
            'step_id': step_id,
            'data_type': data_type,
            'data_content': data_content,
            'ai_interpretation': ai_interpretation,
            'technician_name': technician_name
        }, to=f'inspection_{inspection_id}')

    @socketio.on('submit_ssra')
    def handle_submit_ssra(data):
        inspection_id = data['inspection_id']
        hazard = data['hazard']
        risk_level = data['risk_level']
        control_measure = data['control_measure']
        technician_name = data.get('technician_name', 'A technician')
        
        ssra_entry = SSRA(inspection_id=inspection_id, hazard=hazard, risk_level=risk_level, control_measure=control_measure)
        db.session.add(ssra_entry)
        db.session.commit()
        
        emit('ssra_update', {
            'id': ssra_entry.id,
            'hazard': hazard,
            'risk_level': risk_level,
            'control_measure': control_measure,
            'technician_name': technician_name
        }, to=f'inspection_{inspection_id}')

    @socketio.on('update_grid_map')
    def handle_update_grid_map(data):
        inspection_id = data['inspection_id']
        grid_data = data['grid_data']
        technician_name = data.get('technician_name', 'A technician')
        
        grid_map = GridMap.query.filter_by(inspection_id=inspection_id).first()
        if not grid_map:
            grid_map = GridMap(inspection_id=inspection_id)
        grid_map.set_grid_data(grid_data)
        db.session.add(grid_map)
        db.session.commit()
        
        emit('grid_map_update', {'grid_data': grid_data, 'technician_name': technician_name}, to=f'inspection_{inspection_id}')

    return app