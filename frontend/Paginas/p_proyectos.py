import streamlit as st 
from .proyectos import project_logistic_test
from .proyectos import project_prediccion_consumo
from .proyectos import project_prediccion



def proyectos():
    titulos_proyectos = ["Logistic Test", "Predicción de consumo", "Predicción"]
    opcion = st.selectbox("Selecciona un proyecto", titulos_proyectos)

    if opcion == "Logistic Test":
        project_logistic_test.logistic_test()
    elif opcion == "Predicción de consumo":
        project_prediccion_consumo.prediccion_consumo()
    elif opcion == "Predicción":
        project_prediccion.prediccion()



