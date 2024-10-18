import streamlit as st
import base64

def load_svg(svg_file):
    with open(svg_file, "r") as f:
        return f.read()

def render_svg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    st.write(html, unsafe_allow_html=True)

def format_currency(amount):
    return f"${amount:,.2f}"

def validate_input(input_data):
    # Add input validation logic here
    pass
