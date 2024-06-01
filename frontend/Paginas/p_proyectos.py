import streamlit as st 
from .proyectos import project_prediccion_consumo



def proyectos():
    titulos_proyectos = ["Predicción de consumo"]
    opcion = st.selectbox("Selecciona un proyecto", titulos_proyectos)

    if opcion == "Predicción de consumo":
        project_prediccion_consumo.prediccion_consumo()



