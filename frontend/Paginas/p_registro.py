import streamlit as st 
import requests

URL_BACKEND = "http://127.0.0.1:8000/"

def registro():
    st.markdown("""
<div style="text-align: justify;">

## Registro
¿Aún no estás registrado? Rellena el siguiente formulario y dale 
al botón *registrarse*. Seguidamente se te enviará un correo con un 
Token de acceso. Para confirmar la cuenta simplemente pega el token 
el formulario de más abajo y clicka en el botón *confirmar cuenta*.      
</div>
""", unsafe_allow_html=True)
    name = st.text_input(label="Nombre")
    surname = st.text_input(label="Apellidos")
    correo = st.text_input(label="Correo electrónico")
    password = st.text_input(label="Contraseña", type="password")

    json_registrarse = {"name": name,
                        "surname": surname, 
                        "email": correo,
                        "password": password}
    
    if st.button("Registrarse"):
        response = requests.post(url=f"{URL_BACKEND}users", json=json_registrarse)

        if response.status_code==200:
            st.success("Registro realizado exitosamente. Correo con token de confirmación enviado.")
    
        elif response.status_code != 500:
            st.warning(f"El correo ya está en uso o no es válido.")

        else:
            st.warning("¡Ha ocurrido un error inesperado!")
