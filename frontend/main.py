from .pages import p_introduccion
from .pages import p_registro 
from .pages import p_inicio_sesion 
from .pages import p_proyectos 
from .pages import p_user
import streamlit as st



def main():
    st.sidebar.title("Navegación")
    seleccion = st.sidebar.radio("Selecciona una página",
                                 ["Introducción", "Registro", "Inicio Sesión", "Proyectos", "Información del usuario"])
    
    if seleccion == "Introducción":
        p_introduccion.introduccion()
    elif seleccion == "Registro":
        p_registro.registro()
    elif seleccion == "Inicio Sesión":
        p_inicio_sesion.inicio_sesion()
    elif seleccion == "Proyectos":
        p_proyectos.proyectos()
    elif seleccion == "Información del ususario":
        p_user.user()

if __name__ == "__main__":
    main()