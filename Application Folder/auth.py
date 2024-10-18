import streamlit as st
import hashlib
from database import execute_query, fetch_one

def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        result = fetch_one(query, (username, hashed_password))
        
        if result:
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.success("Logged out successfully!")
    st.experimental_rerun()

def is_authenticated():
    return st.session_state.get('authenticated', False)
