import streamlit as st 
from .proyectos import project_logistic_test
from .proyectos import project_prediccion_consumo



def proyectos():
    titulos_proyectos = ["Logistic Test", "Predicción de consumo"]
    opcion = st.selectbox("Selecciona un proyecto", titulos_proyectos)

    if opcion == "Logistic Test":
        project_logistic_test.logistic_test()
    elif opcion == "Predicción de consumo":
        project_prediccion_consumo.prediccion_consumo()



