import streamlit as st
import requests
import pandas as pd

# URL de la API backend
URL_BACKEND = "http://127.0.0.1:8000/"

# Función para la página de introducción y tutorial
def pagina_introduccion():
    st.markdown("""
    # Introducción y tutorial
        
    Aquí escribimos una pequeña introducción y tutorial a la API y a la web

    ## Inicio de sesión
    Rellena el siguiente formulario para iniciar sesión.
    """)

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




def informacion_del_usuario():
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión para poder ver esta página")
    else:
        st.markdown(f"""
- Correo: {st.session_state.correo}
""")
        headers = {"Authorization": f"{st.session_state.token}"}
        articles = requests.get(url=f"{URL_BACKEND}articles",
                                headers=headers).json()
        name_articles = []
        for art in articles:
            name_articles.append(art["title"])
        
        modelo_of_predictions = st.selectbox(label="Selecciona el modelo del que quieras ver tus predicciones",
                                            options=name_articles)
        user_preds = requests.get(url=f"{URL_BACKEND}predictions",
                                  headers=headers).json()
        preds_of_model = []
        for pred in user_preds:
            if pred["article"]["title"] == modelo_of_predictions:
                pred_of_model = pred["prediction_input"]
                name_pred = list(pred["prediction_output"].keys())[0]
                pred_of_model[name_pred] = pred["prediction_output"][name_pred]
                preds_of_model.append(pred_of_model)
        df_of_preds = pd.DataFrame(preds_of_model)
        st.dataframe(df_of_preds)
# Función para la página de artículos
def pagina_proyectos():
    
    # Lista para almacenar los títulos de los artículos
    titulos_articulos = ["Regresión logística para hacer pruebas", "Artículo 2"]

    # Selectbox con los títulos de los artículos
    opcion = st.selectbox("Selecciona un artículo", titulos_articulos)

    # Mostrar texto dependiendo de la opción seleccionada
    if opcion == "Regresión logística para hacer pruebas":
        indice = st.radio("¿Qué quieres ver aquí?", options=["Descripción del proyecto", "Predicción única"])
        if indice == "Descripción del proyecto":
            st.markdown("""
## Regresión logística para hacer pruebas
En este artículo habrá un modelo de regresión logística que nos permitirá hacer pruebas.
No está optimizado ni mucho menos.
Es simplemente para ver que todo funciona
## Predicción única
Escoge los parámetros de entrada:              
    """)
        elif indice == "Predicción única":
            age = st.slider("Edad del individuo.", value=30,
                            min_value=20, max_value=65, step=1)
            work_experience = st.slider("Años de experiencia.", value=5,
                                        min_value=0, max_value=35, step=1)
            gender = st.selectbox("Sexo", options=["male", "female"])
            ever_married = st.selectbox("¿Está o ha estado casado?", options=["yes", "no"])
            graduated = st.selectbox("¿Está graduado?", options=["yes", "no"])
            profession = st.selectbox("Escoge una profesión", options=["Artist", "Doctor", "Engineer", "Entertainment", "Executive", "Healthcare", "Homemaker", "Lawyer"])
            input_data = {
                "age": age, "work_experience": work_experience,
                "gender": gender, "graduated": graduated, 
                "profession": profession, "ever_married": ever_married
            }
            if st.button("Realizar predicción"):
                if "token" not in st.session_state.keys():
                    st.warning("Tienes que iniciar sesión")
                else:
                    headers = {"Authorization": st.session_state.token}
                    response = requests.post(url=f"{URL_BACKEND}predictions/logistic_test_model", json=input_data, headers=headers)
                    st.success(f"Se espera que el salario del individuo sea: {response.json()['prediction_output']['predicted_salary']}")
    elif opcion == "Artículo 2":
        st.write("Texto del artículo 2: Adiós")


# Barra lateral con opciones de navegación
def main():
    st.sidebar.title("Navegación")
    seleccion = st.sidebar.radio("Selecciona una opción", ["Introducción y tutorial", "Proyectos", "Información del usuario"])

    if seleccion == "Introducción y tutorial":
        pagina_introduccion()
    elif seleccion == "Proyectos":
        pagina_proyectos()
    elif seleccion == "Información del usuario":
        informacion_del_usuario()


if __name__ == "__main__":
    main()



















