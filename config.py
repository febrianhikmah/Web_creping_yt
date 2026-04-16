import streamlit as st

API_KEY = st.secrets["API_KEY"]

DB_CONFIG = {
    "host": st.secrets["DB_HOST"],
    "database": st.secrets["DB_NAME"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASS"],
    "port": st.secrets["DB_PORT"]
}
