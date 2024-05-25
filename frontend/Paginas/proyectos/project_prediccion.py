import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import io
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Mi Aplicación con Streamlit")

# Function to save matplotlib figure to a BytesIO object
def save_fig_to_bytesio(fig):
    img_bytesio = io.BytesIO()
    fig.savefig(img_bytesio, format='png')
    img_bytesio.seek(0)
    return img_bytesio

def run_eda():
    st.header("Análisis Exploratorio de Datos (EDA)")
    uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV subido
            df = pd.read_csv(uploaded_file, delimiter="\t")


            # Sección 1: Variables de Datos Personales
            st.subheader("Variables de Datos Personales")
            
            # Opciones de gráficos para esta sección
            personal_vars = {
                "Distribución de ingresos": "Income",
                "Distribución del nivel educativo": "Education",
                "Distribución del estado civil": "Marital_Status",
                "Distribución de edad" : "Year_Birth",
                "Distribución de hijos en casa" : "Kidhome",
                "Distribución de adolescentes en casa": "Teenhome",
                "Distribución de año de inscripción" : "Dt_Customer"
            }
            selected_personal_vars = st.multiselect(
                "Selecciona los gráficos que deseas ver:",
                options=list(personal_vars.keys()),
                default=list(personal_vars.keys())
            )
            
            # To save graphs
            graphs_in_memory = []
            
            # Gráficos de variables personales
            for var in selected_personal_vars:
                if var == "Distribución de ingresos":
                    st.write("### Distribución de ingresos")
                    st.write("Este gráfico muestra la distribución de los ingresos anuales de los clientes. "
                            "Nos permite ver cómo se distribuyen los ingresos y si hay grupos de clientes con ingresos similares.")
                    fig, ax = plt.subplots()
                    sns.histplot(df['Income'].dropna(), kde=True, ax=ax)
                    ax.set_title('Distribución de ingresos')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución de ingresos', save_fig_to_bytesio(fig)))
                elif var == "Distribución del nivel educativo":
                    st.write("### Distribución del nivel educativo")
                    st.write("Este gráfico muestra la distribución de los niveles educativos de los clientes. "
                            "Nos ayuda a entender el perfil educativo de los clientes.")
                    fig, ax = plt.subplots()
                    sns.countplot(data=df, x='Education', ax=ax)
                    ax.set_title('Distribución del nivel educativo')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución del nivel educativo', save_fig_to_bytesio(fig)))
                elif var == "Distribución del estado civil":
                    st.write("### Distribución del estado civil")
                    st.write("Este gráfico muestra la distribución del estado civil de los clientes. "
                            "Nos ayuda a entender la composición familiar de los clientes.")
                    fig, ax = plt.subplots()
                    sns.countplot(data=df, x='Marital_Status', ax=ax)
                    ax.set_title('Distribución del estado civil')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución del estado civil', save_fig_to_bytesio(fig)))
                elif var == "Distribución de edad":
                    st.write("### Distribución de edad")
                    st.write("Este gráfico muestra la distribución de edad de los clientes. "
                            "Nos permite ver cómo se distribuyen los clientes en función de su edad.")
                    fig, ax = plt.subplots()
                    sns.histplot(df["Year_Birth"].apply(lambda x: datetime.now().year - x).dropna(), kde=True, ax=ax)
                    ax.set_title('Distribución de edad')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución de edad', save_fig_to_bytesio(fig)))
                elif var == "Distribución de hijos en casa":
                    st.write("### Distribución de hijos en casa")
                    st.write("Este gráfico muestra la distribución del número de hijos en casa de los clientes.")
                    fig, ax = plt.subplots()
                    sns.countplot(data=df, x='Kidhome', ax=ax)
                    ax.set_title('Distribución de hijos en casa')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución de hijos en casa', save_fig_to_bytesio(fig)))
                elif var == "Distribución de adolescentes en casa":
                    st.write("### Distribución de adolescentes en casa")
                    st.write("Este gráfico muestra la distribución del número de adolescentes en casa de los clientes.")
                    fig, ax = plt.subplots()
                    sns.countplot(data=df, x='Teenhome', ax=ax)
                    ax.set_title('Distribución de adolescentes en casa')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución de adolescentes en casa', save_fig_to_bytesio(fig)))
                elif var == "Distribución de año de inscripción":
                    st.write("### Distribución de año de inscripción")
                    st.write("Este gráfico muestra la distribución del año de inscripción de los clientes. "
                            "Nos permite ver cómo se distribuyen los clientes en función de su antigüedad.")
                    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
                    df['Dt_Customer'] = df['Dt_Customer'].dt.year
                    fig, ax = plt.subplots()
                    sns.countplot(data=df, x='Dt_Customer', ax=ax)
                    ax.set_title('Distribución de año de inscripción')
                    st.pyplot(fig)
                    # Save the figure
                    graphs_in_memory.append(('Distribución de año de inscripción', save_fig_to_bytesio(fig)))
            
            ## Sección 2: Variables de Compra de Productos
            st.subheader("Total de ventas por categoría de producto")

            # Descripción de la sección
            st.write("Este gráfico muestra el total de ventas por cada categoría de producto. "
                "Nos ayuda a identificar qué categorías generan más ingresos.")

            # Opciones de gráficos para esta sección
            category_vars = {
                "Total de ventas por categoría": ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts']
            }
            selected_category_vars = st.multiselect(
                "Selecciona los gráficos que deseas ver:",
                options=list(category_vars.keys()),
                default=list(category_vars.keys())
            )

            # Gráfico: Total de ventas por categoría
            if "Total de ventas por categoría" in selected_category_vars:
                st.write("### Total de ventas por categoría")
                st.write("Este gráfico muestra el total de ventas por cada categoría de producto. "
                        "Nos ayuda a identificar qué categorías generan más ingresos.")
                # Definición de las categorías
                categories = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts']
                # Reemplazar 'Mnt' con una cadena vacía para obtener los nombres de categoría deseados
                category_names = [category.replace('Mnt', '') for category in categories]
                # Calcular el total de ventas por categoría
                sales_by_category = df[categories].sum().reset_index()
                sales_by_category.columns = ['Category', 'Total_Sales']
                # Reemplazar los nombres de las categorías en el DataFrame con los nombres modificados
                sales_by_category['Category'] = category_names
                # Creación del gráfico
                fig2, ax2 = plt.subplots()
                sns.barplot(data=sales_by_category, x='Category', y='Total_Sales', ax=ax2)
                ax2.set_title('Total de ventas por categoría')
                st.pyplot(fig2)
                # Save the figure
                graphs_in_memory.append(('Total de ventas por categoría', save_fig_to_bytesio(fig2)))

            # Sección 3: Variables de Promociones y Campañas Publicitarias
            st.subheader("Variables de Promociones y Campañas Publicitarias")
            
            # Opciones de gráficos para esta sección
            campaign_vars = {
                "Comparación de respuestas a campañas de marketing": ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
            }
            selected_campaign_vars = st.multiselect(
                "Selecciona los gráficos que deseas ver:",
                options=list(campaign_vars.keys()),
                default=list(campaign_vars.keys())
            )
            
            # Gráfico: Comparación de respuestas a campañas de marketing
            if "Comparación de respuestas a campañas de marketing" in selected_campaign_vars:
                st.write("### Comparación de respuestas a campañas de marketing")
                st.write("Este gráfico muestra el número de respuestas positivas a diferentes campañas de marketing. "
                        "Nos ayuda a evaluar la efectividad de cada campaña.")
                campaigns = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', "Response"]
                campaigns_names = [campaign.replace('Accepted', '') for campaign in campaigns]
                total_responses = df[campaigns].sum().reset_index()
                total_responses.columns = ['Campaign', 'Total_Responses']
                total_responses["Campaign"] = campaigns_names
                fig5, ax5 = plt.subplots()
                sns.barplot(data=total_responses, x='Campaign', y='Total_Responses', ax=ax5)
                ax5.set_title('Respuestas a campañas de marketing')
                st.pyplot(fig5)
                # Save the figure
                graphs_in_memory.append(('Respuestas a campañas de marketing', save_fig_to_bytesio(fig5)))
            
            
            # Sección 4: Variables de Modalidad de Compra
            st.subheader("Variables de Modalidad de Compra")
            
            # Opciones de gráficos para esta sección
            purchase_vars = {
                "Compras por tipo de producto": ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases'],
                "Visitas web y compras": ['NumWebVisitsMonth', 'NumWebPurchases']
            }
            selected_purchase_vars = st.multiselect(
                "Selecciona los gráficos que deseas ver:",
                options=list(purchase_vars.keys()),
                default=list(purchase_vars.keys())
            )
            
            # Gráfico: Compras por tipo de producto
            if "Compras por tipo de producto" in selected_purchase_vars:
                st.write("### Compras por tipo de producto")
                st.write("Este gráfico muestra el número total de compras realizadas a través de diferentes canales. "
                        "Nos permite ver qué canales de venta son más utilizados por los clientes.")
                purchases = purchase_vars["Compras por tipo de producto"]
                purchases_names = [purchase.replace('Num', '') for purchase in purchases]

                total_purchases = df[purchases].sum().reset_index()
                total_purchases.columns = ['Purchase_Type', 'Total_Purchases']
                total_purchases['Purchase_Type'] = purchases_names
                fig6, ax6 = plt.subplots()
                sns.barplot(data=total_purchases, x='Purchase_Type', y='Total_Purchases', ax=ax6)
                ax6.set_title('Compras por tipo de producto')
                st.pyplot(fig6)
                # Save the figure
                graphs_in_memory.append(('Compras por tipo de producto', save_fig_to_bytesio(fig6)))
            
            # Gráfico: Visitas web y compras
            if "Visitas web y compras" in selected_purchase_vars:
                st.write("### Visitas web y compras")
                st.write("Este gráfico de dispersión muestra la relación entre el número de visitas a la web y las compras realizadas a través de la web. "
                        "Nos ayuda a entender si las visitas a la web se traducen en compras.")
                fig7, ax7 = plt.subplots()
                sns.scatterplot(data=df, x='NumWebVisitsMonth', y='NumWebPurchases', ax=ax7)
                ax7.set_title('Visitas web y compras')
                st.pyplot(fig7)
                # Save the figure
                graphs_in_memory.append(('Visitas web y compras', save_fig_to_bytesio(fig7)))

            # Opción para descargar los gráficos en un archivo Excel
            if st.button("Descargar gráficos en Excel"):
                output = io.BytesIO()
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "Gráficos EDA"
                
                row_start = 1
                for title, image_data in graphs_in_memory:
                    # Insert the title for the plot
                    sheet.cell(row=row_start, column=1, value=title)
                    # Insert the image below the title
                    img = Image(image_data)
                    img.anchor = f'A{row_start + 1}'
                    sheet.add_image(img)
                    row_start += 30  # Adjust the row offset as needed
                
                workbook.save(output)
                output.seek(0)
                st.download_button(
                    label="Descargar gráficos en Excel",
                    data=output,
                    file_name="eda_graphs.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Error al cargar el archivo CSV: {e}")
    else:
        st.warning("Por favor, sube un archivo CSV para continuar.")

def make_prediction_vino(input_data):
    # Define the API endpoint
    api_endpoint = "https://your-api-endpoint.com/predictions/vino"

    # Make the POST request to the API
    response = requests.post(api_endpoint, json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the prediction result from the response
        prediction = response.json()["prediction"]
        return prediction
    else:
        st.error("Error occurred while making prediction for Vino. Please try again.")
        return None

def make_prediction_fish(input_data):
    # Define the API endpoint
    api_endpoint = "https://your-api-endpoint.com/fish/predict"

    # Make the POST request to the API
    response = requests.post(api_endpoint, json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the prediction result from the response
        prediction = response.json()["prediction"]
        return prediction
    else:
        st.error("Error occurred while making prediction for Fish. Please try again.")
        return None

def make_prediction_meat(input_data):
    # Define the API endpoint
    api_endpoint = "https://your-api-endpoint.com/meat/predict"

    # Make the POST request to the API
    response = requests.post(api_endpoint, json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the prediction result from the response
        prediction = response.json()["prediction"]
        return prediction
    else:
        st.error("Error occurred while making prediction for Meat. Please try again.")
        return None

def make_prediction_sweet(input_data):
    # Define the API endpoint
    api_endpoint = "https://your-api-endpoint.com/sweet/predict"

    # Make the POST request to the API
    response = requests.post(api_endpoint, json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the prediction result from the response
        prediction = response.json()["prediction"]
        return prediction
    else:
        st.error("Error occurred while making prediction for Sweet. Please try again.")
        return None

def make_prediction_fruit(input_data):
    # Define the API endpoint
    api_endpoint = "https://your-api-endpoint.com/fruit/predict"

    # Make the POST request to the API
    response = requests.post(api_endpoint, json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the prediction result from the response
        prediction = response.json()["prediction"]
        return prediction
    else:
        st.error("Error occurred while making prediction for Fruit. Please try again.")
        return None


def prediccion_unica():
    st.title("Aplicación de Predicciones")

    st.header("Predicción")
    st.write("Aquí irían los detalles de la predicción (esto es solo un placeholder).")

    # Explanation of each column
    st.subheader("Explicación de las columnas:")
    st.write("""
    - **Age**: La edad del individuo.
    - **Education**: El nivel más alto de educación alcanzado por el individuo.
    - **Marital_Status**: El estado civil del individuo.
    - **Income**: El ingreso anual del individuo.
    - **Kidhome**: El número de hijos que viven en casa.
    - **Teenhome**: El número de adolescentes que viven en casa.
    - **Year_Customer_Entered**: El año en que el cliente ingresó.
    - **Recency**: La recencia del cliente (en días).
    - **Complain**: Indica si el cliente ha presentado alguna queja (0 para no, 1 para sí).
    """)


    # Place select box at the top of the page
    option = st.selectbox("Selecciona una predicción", ["Vino", "Fruit", "Meat", "Fish", "Sweet"])


    # Selectors for each column
    age = st.slider("Edad", min_value=0, max_value=100, value=30, step=1)
    education = st.selectbox("Educación", ["PhD", "Master", "Graduation", "2n Cycle", "Basic"])
    marital_status = st.selectbox("Estado Civil", ["Single", "Together", "Married", "Divorced", "Widow", "Alone", "Absurd"])
    income_str = st.text_input("Ingreso Anual", "50000")
    try:
        income = float(income_str)
    except ValueError:
        st.error("Por favor, introduce un número válido para el ingreso anual.")
    kidhome = st.number_input("Hijos en Casa", min_value=0, max_value=10, value=0)
    teenhome = st.number_input("Adolescentes en Casa", min_value=0, max_value=10, value=0)
    year_customer_entered = st.number_input("Año de Ingreso del Cliente", min_value=1900, max_value=2025, value=2010)
    recency_str = st.text_input("Recencia (en días)", "30")
    try:
        recency = int(recency_str)
    except ValueError:
        st.error("Por favor, introduce un número válido para la recencia.")
    complain = st.radio("¿Ha Presentado Queja?", ["No", "Sí"])

    # Button for making a single prediction
    if st.button("Realizar Predicción"):
        # Prepare input data for prediction
        input_data = {
            "age": age,
            "education": education,
            "marital_status": marital_status,
            "income": income,
            "kidhome": kidhome,
            "teenhome": teenhome,
            "year_customer_entered": year_customer_entered,
            "recency": recency,
            "complain": 1 if complain == "Sí" else 0
        }
        
        # Make prediction
        if option == "Vino":
            prediction = make_prediction_vino(input_data)()
        elif option == "Fruit":
            prediction = make_prediction_fruit(input_data)()()
        elif option == "Meat":
            prediction = make_prediction_meat(input_data)()()
        elif option == "Fish":
            prediction = make_prediction_fish(input_data)()()
        elif option == "Sweet":
            prediction = make_prediction_sweet(input_data)()()

  
        if prediction is not None:
            st.write(f"Predicción realizada: {prediction}")

def prediccion_excel():

    st.markdown("""
## Predicción excel 
En esta sección podrás subir un excel para obtener una predicción masiva.
Cada columna del excel tiene que representar una variable input del modelo. 
En concreto, el archivo tiene que tener una estructura como esta
""")        
    # Crear un DataFrame de ejemplo
    df_plantilla = pd.DataFrame({
        "Age": [67, 70, 59, 40, 43],
        "Education": ["Graduation", "Graduation", "Graduation", "Graduation", "PhD"],
        "Marital_Status": ["Single", "Single", "Together", "Together", "Married"],
        "Income": [58138.0, 46344.0, 71613.0, 26646.0, 58293.0],
        "Kidhome": [0, 1, 0, 1, 1],
        "Teenhome": [0, 1, 0, 0, 0],
        "Dt_Customer": ['04-09-2012', '08-03-2014', '21-08-2013', '10-02-2014', '19-01-2014'],
        "Recency": [58, 38, 26, 26, 94],
        "Complain": [0, 0, 1, 0, 0]
    })
    
    # Mostrar el DataFrame de ejemplo
    st.dataframe(df_plantilla)

    excel_upload = st.file_uploader("Elige un archivo Excel")
    if st.button("Make Prediction"):
            try:
                df_pred = pd.read_excel(excel_upload, thousands=',')
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
            df_plantilla.columns = [col.lower() for col in df_plantilla.columns]

            if set(df_pred.columns) != set(df_plantilla.columns):
                st.warning("El excel tiene que tener las columnas en el mismo formato que la plantilla")
            df_pred = df_pred[df_plantilla.columns]
            dtype_correct = True
            for col in df_plantilla:
                if str(df_plantilla[col].dtype) != str(df_pred[col].dtype):
                    st.warning(f"La columna {col} no está en el formato requerido.")
                    dtype_correct = False 
                    break 

def prediccion():
    indice = st.radio("¿Qué quieres ver aquí?", options=["Exploratory Data Analysis", "Predicción única", "Predicción Excel"])
    if indice=="Exploratory Data Analysis":
        run_eda()
    elif indice == "Predicción única":
        prediccion_unica()
    elif indice == "Predicción Excel":
        prediccion_excel()