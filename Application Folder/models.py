from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='In Progress')

class InspectionStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

class InspectionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('inspection_step.id'), nullable=False)
    data_type = db.Column(db.String(20), nullable=False)
    data_content = db.Column(db.Text, nullable=False)
    ai_interpretation = db.Column(db.Text)

class SSRA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    hazard = db.Column(db.String(255), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    control_measure = db.Column(db.Text, nullable=False)

class GridMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    grid_data = db.Column(db.Text, nullable=False)

    def set_grid_data(self, data):
        self.grid_data = db.json.dumps(data)

    def get_grid_data(self):
        return db.json.loads(self.grid_data)
