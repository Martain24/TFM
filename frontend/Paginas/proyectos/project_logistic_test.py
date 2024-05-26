import streamlit as st 
import requests
URL_BACKEND = "http://127.0.0.1:8000/"
import pandas as pd
def logistic_test():
    indice = st.radio("¿Qué quieres ver aquí?", options=["Descripción del proyecto", "Predicción única", "Predicción Excel", "Predicción pescado"])
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
            1: {"age": age, "work_experience": work_experience,
            "gender": gender, "graduated": graduated, 
            "profession": profession, "ever_married": ever_married}
        }
        if st.button("Realizar predicción"):
            if "token" not in st.session_state.keys():
                st.warning("Tienes que iniciar sesión")
            else:
                headers = {"Authorization": st.session_state.token}
                response = requests.post(url=f"{URL_BACKEND}predictions/logistic_test_model", json=input_data, headers=headers)
                st.success(f"Se espera que el salario del individuo sea: {response.json()}")
    elif indice == "Predicción Excel":
        st.markdown("""
## Predicción excel 
En esta sección podrás subir un excel para obtener una predicción masica.
Cada columna del excel tiene que representar una variable input del modelo. 
En concreto, el archivo tiene que tener una estructura como esta
""")        
        df_plantilla = pd.DataFrame()
        df_plantilla["age"] = [20, 30, 50, 35, 60, 40, 20, 18]
        df_plantilla["work_experience"] = [10, 5, 3, 15,8, 11, 20, 10]
        df_plantilla["gender"] = ["male"]*4 + ["female"]*4 
        df_plantilla["ever_married"] = ["yes"]*4 + ["no"]*4 
        df_plantilla["graduated"] = ["yes"]*4 + ["no"]*4 
        df_plantilla["profession"] = ["Artist", "Doctor", "Engineer", "Entertainment", "Executive", "Healthcare", "Homemaker", "Lawyer"]
        st.dataframe(df_plantilla)
        excel_upload = st.file_uploader("Selecciona archivo excel.")
        if st.button("Make Prediction"):
            try:
                df_pred = pd.read_excel(excel_upload)
                if "Unnamed: 0" in df_pred.columns:
                    df_pred = df_pred.drop("Unnamed: 0", axis="columns")
                st.dataframe(df_pred)
            except ValueError:
                df_pred = pd.read_csv(excel_upload)
                if "Unnamed: 0" in df_pred.columns:
                    df_pred = df_pred.drop("Unnamed: 0", axis="columns")
                st.dataframe(df_pred)
            except:
                st.warning("Archivo no válido")
            df_pred.columns = [col.lower() for col in df_pred.columns]
            if set(df_pred.columns) != set(df_plantilla.columns):
                st.warning("El excel tiene que tener las columnas en el mismo formato que la plantilla")
            df_pred = df_pred[df_plantilla.columns]
            dtype_correct = True
            for col in df_plantilla:
                if str(df_plantilla[col].dtype) != str(df_pred[col].dtype):
                    st.warning(f"La columna {col} no está en el formato requerido.")
                    dtype_correct = False 
                    break 
            if dtype_correct:
                input_data = {}
                def save_data(row):
                    data = {
                        "age": row["age"], "work_experience": row["work_experience"],
                        "gender": row["gender"], "graduated": row["graduated"], 
                        "profession": row["profession"], "ever_married": row["ever_married"]
                    }
                    input_data[row.name] = data
                df_pred.apply(save_data, axis=1)
                if "token" not in st.session_state.keys():
                    st.warning("Tienes que iniciar sesión")
                else:
                    headers = {"Authorization": st.session_state.token}
                    response = requests.post(url=f"{URL_BACKEND}predictions/logistic_test_model", json=input_data, headers=headers)
                
                def create_predicted_salary(row):
                    return response.json()["prediction_output"][f"{row.name}"]["predicted_salary"]
                df_pred["predicted_salary"] = df_pred.apply(create_predicted_salary, axis=1)

                st.markdown("Aquí tienes tu DataFrame con la predicción")
                st.dataframe(df_pred)
    elif indice == "Predicción pescado":
        age = st.slider("Edad del individuo.", value=30,
                        min_value=20, max_value=65, step=1)
        