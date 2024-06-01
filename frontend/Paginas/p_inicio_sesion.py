import streamlit as st 
import requests

URL_BACKEND = "http://127.0.0.1:8000/"
URL_BACKEND = "https://tfm-z7o5.onrender.com/"

def inicio_sesion():
    st.markdown("""
<div style="text-align: justify;">

## Inicio de sesión
Si ya estas registrado puedes iniciar sesión aquí. 
En caso de que aún no tengas confirmada la cuenta se te enviará un token
al correo para que puedas hacerlo desde la página *Registro*.      
</div>
""", unsafe_allow_html=True)
    correo = st.text_input(label="Correo electrónico")
    password = st.text_input(label="Contraseña", type="password")
    json_inicio_sesion = {
        "username": correo,
        "password": password
    }

    if st.button("Iniciar sesión"):
        response = requests.post(url=f"{URL_BACKEND}login", data=json_inicio_sesion)
        if response.status_code == 200:
            st.success("Sesión iniciada con éxito")
            st.session_state.token = f"{response.json()['token_type']} {response.json()['access_token']}"
            st.session_state.correo = correo
        else:
            st.warning(response.json()["detail"])