import streamlit as st
from database import execute_query, fetch_all

def generate_workflow(processed_data):
    # Use the processed data to generate a workflow
    # This is a simplified example and should be expanded based on specific requirements
    workflow = [
        "1. Initial assessment",
        "2. Water extraction",
        "3. Drying and dehumidification",
        "4. Cleaning and sanitizing",
        "5. Restoration and repairs"
    ]
    
    # Save workflow to database
    save_workflow(workflow)
    
    return workflow

def save_workflow(workflow):
    workflow_str = "\n".join(workflow)
    query = "INSERT INTO workflows (steps) VALUES (%s)"
    execute_query(query, (workflow_str,))

def get_workflows():
    query = "SELECT id, steps, created_at FROM workflows ORDER BY created_at DESC"
    return fetch_all(query)

def display_workflows():
    workflows = get_workflows()
    for workflow in workflows:
        st.subheader(f"Workflow {workflow[0]}")
        st.text(workflow[1])
        st.text(f"Created at: {workflow[2]}")
        st.markdown("---")
