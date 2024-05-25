import streamlit as st 
import requests
import pandas as pd
URL_BACKEND = "http://127.0.0.1:8000/"

def user():
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión para poder ver esta página")
    else:
        headers = {"Authorization": f"{st.session_state.token}"}
        user_predictions = requests.get(url=f"{URL_BACKEND}predictions",
                                        headers=headers).json()
        user_info = user_predictions[0]["user"]
        st.markdown(f"""

## Información del usuario
- Nombre: {user_info["name"]}
- Apellido: {user_info["surname"]}
- Correo: {user_info["email"]}
- Fecha de creación: {"-".join(user_info["created_at"].split("T")[0].split("-")[-1::-1])}
## Historial de predicciones
""")
        models_info = requests.get(url=f"{URL_BACKEND}ml-models", headers=headers).json()
        title_models = [model["title"] for model in models_info]
        modelo_predictions = st.selectbox(label="Selecciona el modelo del que quieras ver tus predicciones",
                                          options=title_models)
        dfs_pred = {}
        for pred in user_predictions:
            if pred["ml_model"]["title"] == modelo_predictions:
                fecha = '-'.join(pred['created_at'].split('T')[0].split('-')[-1::-1])
                hora = pred["created_at"].split("T")[1].split(".")[0]
                df_pred = []
                for index_pred in pred["prediction_input"].keys():
                    dict_pred = {}
                    dict_pred["Fecha"] = fecha
                    dict_pred["Hora"] = hora
                    for input_col in pred["prediction_input"][index_pred].keys():
                        dict_pred[input_col] = pred["prediction_input"][index_pred][input_col]
                    for output_col in pred["prediction_output"][index_pred].keys():
                        dict_pred[output_col] = pred["prediction_output"][index_pred][output_col]
                    df_pred.append(dict_pred)
                df_pred = pd.DataFrame(df_pred)
                dfs_pred[f"{fecha}T{hora}"] = df_pred
        
        filter = st.selectbox("¿Cómo quieres ver las predicciones?",
                              options=["Todas en un DataFrame", "Cada una por separado"])
        if filter == "Todas en un DataFrame":
            df_all = pd.DataFrame()
            for pred in dfs_pred.keys():
                df_all = pd.concat([df_all, dfs_pred[pred]])
            st.dataframe(df_all)
        elif filter == "Cada una por separado":
            dates = pd.to_datetime(pd.Series(dfs_pred.keys()), format="%d-%m-%YT%H:%M:%S")
            orden_fecha = st.selectbox(label="¿En qué orden quieres que aparezcan?",
                                       options=["De la más reciente a la más antigua",
                                                "De la más antigua a la más reciente"])
            if orden_fecha == "De la más reciente a la más antigua":
                dates = dates.sort_values(ascending=False).apply(lambda x: x.strftime("%d-%m-%YT%H:%M:%S"))
                st.write(dates)
            elif orden_fecha == "De la más antigua a la más reciente":
                dates = dates.apply(lambda x: x.strftime("%d-%m-%YT%H:%M:%S"))
                st.write(dates)


        st.write(user_predictions)
    