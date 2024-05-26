import streamlit as st 
import requests
import pandas as pd
URL_BACKEND = "http://127.0.0.1:8000/"

def user():
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión para poder ver esta página")
        return None
    headers = {"Authorization": f"{st.session_state.token}"}
    user_predictions = requests.get(url=f"{URL_BACKEND}predictions",
                                    headers=headers)
    if user_predictions.status_code!=200:
        st.warning("Tu sesión ha caducado")
        return None
    elif len(user_predictions.json())==0:
        st.warning("Para que te aparezca esta página tienes que haber hecho al menos una predicción con cualquier modelo.")
        return None
    user_predictions = user_predictions.json()
    user_info = user_predictions[0]["user"]
    user_comments = requests.get(url=f"{URL_BACKEND}comments", headers=headers).json()
    st.markdown(f"""

## Información del usuario
- Nombre: {user_info["name"]}
- Apellido(s): {user_info["surname"]}
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
            dfs_pred[f"{fecha}T{hora}_{pred['id']}"] = df_pred
    
    filter = st.selectbox("¿Cómo quieres ver las predicciones?",
                        options=["Todas en un DataFrame", "Cada una por separado"])
    if filter == "Todas en un DataFrame":
        df_all = pd.DataFrame()
        for pred in dfs_pred.keys():
            df_all = pd.concat([df_all, dfs_pred[pred]])
        st.dataframe(df_all.set_index("Fecha"))
    elif filter == "Cada una por separado":
        df_dates_id = pd.DataFrame()
        dates = pd.to_datetime(pd.Series(dfs_pred.keys()).apply(lambda x: x.split("_")[0]),
                            format="%d-%m-%YT%H:%M:%S")
        df_dates_id["Fecha"] = dates 
        df_dates_id["id"] = pd.Series(dfs_pred.keys()).apply(lambda x: x.split("_")[1])
        orden_fecha = st.selectbox(label="¿En qué orden quieres que aparezcan?",
                                options=["De la más reciente a la más antigua",
                                            "De la más antigua a la más reciente"])
        if orden_fecha == "De la más reciente a la más antigua":
            df_dates_id = df_dates_id.sort_values(by="Fecha", ascending=False)
            dates = df_dates_id["Fecha"].apply(lambda x: x.strftime("%d-%m-%YT%H:%M:%S"))
            ids = df_dates_id["id"]
        elif orden_fecha == "De la más antigua a la más reciente":
            dates = df_dates_id["Fecha"].apply(lambda x: x.strftime("%d-%m-%YT%H:%M:%S"))
            ids = df_dates_id["id"]
        for date,id in zip(dates, ids):
            df_pred = dfs_pred[f"{date}_{id}"].set_index("Fecha")
            fecha, hora = date.split("T")[0], date.split("T")[1]
            st.markdown("---")
            st.markdown(f"##### Predicción del {fecha} a las {hora}")
            st.dataframe(df_pred)
            if st.button("Borrar predicción", key=f"{date}_{id}_borrar_pred", type="primary"):
                requests.delete(url=f"{URL_BACKEND}predictions/{id}", headers=headers)
                st.rerun()
            with st.expander("Ver comentarios sobre la predicción"):
                comments_pred = [comment for comment in user_comments if str(comment["prediction"]["id"])==str(id)]
                for c in comments_pred:
                    st.markdown(f"""💬 {c['content']} ({'-'.join(c['created_at'].split('T')[0].split('-')[-1::-1])} a las {c['created_at'].split('T')[1].split('.')[0]})""")
                content_new_comment = st.text_area(label="Añade un comentario para esta predicción", key=id)
                new_comment = {"content": content_new_comment, "prediction_id": id}
                if st.button("Subir comentario", key=f"{date}_{id}"):
                    requests.post(url=f"{URL_BACKEND}comments", json=new_comment, headers=headers)
                    st.rerun()
                if st.button("Borrar comentarios anteriores", type="primary", key=f"{date}_{id}_borrar"):
                    print(len(comments_pred))
                    for c in comments_pred:
                        requests.delete(url=f"{URL_BACKEND}comments/{c['id']}", headers=headers)
                    st.rerun()
    