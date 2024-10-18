import streamlit as st
import pandas as pd
from database import fetch_all

def generate_report():
    st.subheader("Generate Report")
    
    report_type = st.selectbox("Select report type", ["Summary", "Detailed"])
    date_range = st.date_input("Select date range", [])
    
    if st.button("Generate Report"):
        if report_type == "Summary":
            return generate_summary_report(date_range)
        else:
            return generate_detailed_report(date_range)

def generate_summary_report(date_range):
    # Fetch summary data from database
    query = """
    SELECT COUNT(*) as total_cases, AVG(estimated_cost) as avg_cost
    FROM cases
    WHERE date_created BETWEEN %s AND %s
    """
    result = fetch_all(query, date_range)
    
    if result:
        df = pd.DataFrame(result, columns=["Total Cases", "Average Cost"])
        st.dataframe(df)
        return df
    else:
        st.warning("No data available for the selected date range.")
        return None

def generate_detailed_report(date_range):
    # Fetch detailed data from database
    query = """
    SELECT id, description, estimated_cost, status, date_created
    FROM cases
    WHERE date_created BETWEEN %s AND %s
    ORDER BY date_created DESC
    """
    result = fetch_all(query, date_range)
    
    if result:
        df = pd.DataFrame(result, columns=["ID", "Description", "Estimated Cost", "Status", "Date Created"])
        st.dataframe(df)
        return df
    else:
        st.warning("No data available for the selected date range.")
        return None
