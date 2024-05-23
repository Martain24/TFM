from Paginas.p_introduccion import introduccion
from Paginas.p_registro import registro 
from Paginas.p_inicio_sesion import inicio_sesion 
from Paginas.p_proyectos import proyectos 
from Paginas.p_user import user
import streamlit as st



st.sidebar.title("Navegación")
seleccion = st.sidebar.radio("Selecciona una página",
                                ["Introducción", "Registro", "Inicio Sesión", "Proyectos", "Información del usuario"])

if seleccion == "Introducción":
    introduccion()
elif seleccion == "Registro":
    registro()
elif seleccion == "Inicio Sesión":
    inicio_sesion()
elif seleccion == "Proyectos":
    proyectos()
elif seleccion == "Información del usuario":
    user()