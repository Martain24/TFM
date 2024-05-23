import streamlit as st 



def pagina_introduccion():

    # Campos de entrada para el correo electrónico y la contraseña
    correo = st.text_input(label="Correo electrónico")
    contraseña = st.text_input(label="Contraseña", type="password")

    # JSON para enviar al backend
    json_log_reg = {"email": correo, "password": contraseña}

    # Botón para iniciar sesión
    if st.button("Iniciar Sesión"):
        # Realizar una solicitud POST al endpoint de inicio de sesión de la API backend
        response = requests.post(url=f"{URL_BACKEND}users/login", json=json_log_reg)
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            st.success("Inicio de sesión con éxito")
            if "token_type" in dict(response.json()).keys():
                # Guardar el token en la sesión de Streamlit
                st.session_state.token = f"{response.json()['token_type']} {response.json()['access_token']}"
                st.session_state.correo = correo
            else:
                st.markdown("""¡La cuenta no está confirmada!
Hemos enviado un correo con un token de cofirmación.
Pega ese token en el formulario de abajo y haz click en enviar
Una vez tu cuenta esté confirmada puedes volver a iniciar sesión para usar el frontend""")
        elif response.status_code != 500:
            st.warning(f"Contraseña o correo no válidos.")
        else:
            st.warning("¡Ha ocurrido un error inesperado!")

    # Mensaje para invitar al usuario a registrarse
    st.markdown("""
    *¿Aún no tienes una cuenta? Rellena el formulario con tu correo y contraseña y haz click en el siguiente botón:*
    """)

    # Botón para registrarse
    if st.button("Registrarse"):
        # Realizar una solicitud POST al endpoint de registro de la API backend
        response = requests.post(url=f"{URL_BACKEND}users/", json=json_log_reg)
        # Verificar el código de estado de la respuesta
        if response.status_code == 201:
            st.success("¡Tu cuenta ha sido registrada exitosamente!")
            st.markdown("""El siguiente paso es iniciar sesión
Se te enviará un token de confirmación a tu correo.
Copia ese token de confirmación en el formulario de abajo y haz click en Enviar
Después vuelve a iniciar sesión... ¡y a disfrutar de la página web!""")
        elif response.status_code != 500:
            st.warning(f"El correo ya está en uso o no es válido.")
        else:
            st.warning("¡Ha ocurrido un error inesperado!")
    st.markdown("""
    *¿Tienes una cuenta, pero aún no está confirmada?*      
    Si inicias sesión se te enviará un token de confirmación a tu correo.          
    Pega ese token aquí y haz click en Enviar para terminar de confirmar tu cuenta.         
    Sino realizas este paso no podrás usar las funcionalidades del frontend.
    """)
    user_token = st.text_input("Pega aquí tu token de confirmación", type="password")
    if st.button("Enviar"):
        headers = {"Authorization": f"bearer {user_token}"}
        response_verify = requests.put(url=f"{URL_BACKEND}users", headers=headers)
        if response_verify.status_code == 200:
            st.success("Tu cuenta ha sido confirmada con éxito. Inicia sesión para usar el frontend")
        else:
            st.warning("Ha habido un error inesperado")

def inicio_sesion():
    st.markdown("""
<div style="text-align: justify;">



</div>
""")
    pass