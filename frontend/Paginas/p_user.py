import streamlit as st 
import requests
URL_BACKEND = "http://127.0.0.1:8000/"

def user():
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión para poder ver esta página")
    else:
        headers = {"Authorization": f"{st.session_state.token}"}
        user_predictions = requests.get(url=f"{URL_BACKEND}predictions",
                                        headers=headers).json()
        st.write(user_predictions)
    