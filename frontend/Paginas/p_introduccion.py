import streamlit as st 
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .main {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        color: white;
        padding: 10px;
        border-radius: 15px;
        font-family: 'Arial', sans-serif;
    }}
    .container {{
        background: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 10px;
    }}
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {{
        color: #FFFFFF; /* Cambio del color del texto a blanco */
        margin-bottom: 20px; /* Aumento del espacio entre títulos y párrafos */
    }}
    .main p {{
        font-size: 20px; /* Aumento del tamaño de la letra */
        line-height: 2; /* Aumento del espacio entre líneas */
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def introduccion():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(current_directory, 'Fondo_Intro.jpg')
    set_background(image_path)

    st.markdown("""
    <div class="main">
    
    ## Bienvenido a Nuestra Plataforma de Análisis de Datos para Supermercados y Tiendas de Alimentación
    
    En el mundo actual, muchos datos valiosos están infrautilizados porque sus propietarios no saben cómo extraer su verdadero valor.
    Nuestra plataforma ha sido diseñada específicamente para cambiar eso.
    
    Esta web está creada para que propietarios y trabajadores de supermercados y tiendas de alimentación 
    puedan empezar a obtener beneficios de sus datos y comprender su valor real.
    
    **Funciones Clave de Nuestra Plataforma:**
    
    - **Navegación Intuitiva:** A través de una interfaz sencilla, los usuarios pueden explorar diferentes pestañas que les permitirán utilizar varios modelos para realizar predicciones de diversos tipos.
    - **Visualizaciones Interactivas:** Obtén visualizaciones interactivas de tus datos que te ayudarán a comprender tu negocio en profundidad, permitiéndote tomar decisiones informadas y maximizar el rendimiento de tu tienda.
    - **Conocimiento del Cliente:** Conoce a tus clientes y sus preferencias, lo que te permitirá personalizar tus ofertas y mejorar su experiencia de compra.
    - **Comentarios y Retroalimentación:** Los usuarios pueden dejar comentarios que nos ayudarán a entender mejor sus necesidades, para que podamos ofrecer un servicio lo más personalizado posible.
    
    Nuestro objetivo es proporcionarte las herramientas necesarias para que puedas exprimir tu negocio al 100%, optimizando la toma de decisiones y potenciando el crecimiento a través del análisis de datos.
    
    ¡Comienza a descubrir el potencial oculto de tus datos con nosotros!
    
    </div>
    """, unsafe_allow_html=True)