import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import zscore
import seaborn as sns
sns.set_style("whitegrid")
import utils_frontend
import io
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image

def descripcion_del_proyecto():

    st.markdown("""
                
    <div style="text-align: justify;">

    # Predicción del Consumo en Supermercados

    Un aspecto crucial para los supermercados es anticiparse al consumo de sus clientes. Si, en base a una serie de características personales de los clientes, los propietarios pudieran aproximarse a la demanda de manera más precisa, podrían implementar estrategias que aumenten los beneficios y fidelicen a los clientes.

    ## Objetivo
    Disponer de un modelo capaz de predecir el consumo de cada producto en base a los datos de consumo y características de los clientes.

    ## Productos Analizados
    Se ha desarrollado un modelo específico para cada uno de los siguientes productos:
    - Vino
    - Carne
    - Pescado
    - Fruta
    - Productos Dulces

    ## Modelos Utilizados
    Tras probar diversos modelos de predicción de consumo, se observó que el regresor **XGBoost** ofrecía los mejores resultados.

    ## Proceso de Optimización
    Mediante un exhaustivo proceso de ajuste de hiperparámetros, se optimizó este modelo, logrando resultados muy satisfactorios.

    ## Resultados
    Todos los modelos presentaron un porcentaje de error inferior al 10%, lo que demuestra su alta precisión.

    ## Beneficios Esperados
    - **Aumento de Beneficios**: Mejorar la precisión en la predicción de la demanda puede llevar a una gestión más eficiente del inventario, reduciendo costos de almacenamiento y desperdicio.
    - **Fidelización de Clientes**: Anticiparse a las necesidades de los clientes y ofrecer productos en el momento adecuado puede aumentar la satisfacción y lealtad del cliente.
    </div>
    """, unsafe_allow_html=True)

def exploratory_data_analysis():
    st.markdown("""
<div style="text-align: justify;">
                
## Análisis Exploratorio de Datos
Antes de abordar cualquier problema relacionado con los datos, resulta fundamental comprender la naturaleza de los mismos.
Para ello necesitamos sumergirnos en un proceso conocido como análisis exploratorio de datos.
Aquí, presentamos las primeras 5 filas de nuestro DataFrame, un paso inicial en la comprensión de su estructura y contenido.
</div>
""", unsafe_allow_html=True)
    df = pd.read_csv("../preprocessing_modelos/marketing_campaign_final.csv")
    st.dataframe(df.head())
    st.markdown("""
<div style="text-align: justify;">
Las columnas de nuestro conjunto de datos describen diversas características de nuestros clientes.
En detalle, aquí proporcionamos una breve descripción de cada una de las columnas agrupadas por categorías:

1. **Variables de Datos Personales**
   - ID: Identificador único del cliente
   - Año_Nacimiento: Año de nacimiento del cliente
   - Educación: Nivel educativo del cliente
   - Estado_Civil: Estado civil del cliente
   - Ingresos: Ingresos anuales del hogar del cliente
   - Hijos_Casa: Número de hijos en el hogar del cliente
   - Adolescentes_Casa: Número de adolescentes en el hogar del cliente
   - Fecha_Inscripción: Fecha de inscripción del cliente en la empresa
   - Recencia: Número de días desde la última compra del cliente
   - Queja: 1 si el cliente se quejó en los últimos 2 años, 0 en caso contrario

2. **Variables de Compra de Productos**
   - MntVinos: Monto gastado en vino en los últimos 2 años
   - MntFrutas: Monto gastado en frutas en los últimos 2 años
   - MntProductosCarne: Monto gastado en carne en los últimos 2 años
   - MntProductosPescado: Monto gastado en pescado en los últimos 2 años
   - MntProductosDulces: Monto gastado en dulces en los últimos 2 años
   
3. **Variables de Promociones y Campañas Publicitarias**
   - NumComprasOferta: Número de compras realizadas con descuento
   - AceptoCmp1: 1 si el cliente aceptó la oferta en la 1ra campaña, 0 en caso contrario
   - AceptoCmp2: 1 si el cliente aceptó la oferta en la 2da campaña, 0 en caso contrario
   - AceptoCmp3: 1 si el cliente aceptó la oferta en la 3ra campaña, 0 en caso contrario
   - AceptoCmp4: 1 si el cliente aceptó la oferta en la 4ta campaña, 0 en caso contrario
   - AceptoCmp5: 1 si el cliente aceptó la oferta en la 5ta campaña, 0 en caso contrario
   - Respuesta: 1 si el cliente aceptó la oferta en la última campaña, 0 en caso contrario

4. **Variables de Modalidad de Compra**
   - NumComprasWeb: Número de compras realizadas a través del sitio web de la empresa
   - NumComprasCatálogo: Número de compras realizadas usando un catálogo
   - NumComprasTienda: Número de compras realizadas directamente en tiendas
   - NumVisitasWebMes: Número de visitas al sitio web de la empresa en el último mes
                
El proceso que vamos a seguir para llevar a cabo nuestro análisis exploratorio es sencillo.
Vamos a ir resolviendo preguntas concretas. 
Al final, la resolución de todas estas preguntas concretas, nos permitirán tener una visión amplia y general de los datos.
                
### ¿Cuántos valores faltantes tiene nuestro conjunto de datos?
Para resolver esta cuestión simplemente tenemos que escribir la siguiente línea de código
</div>
""", unsafe_allow_html=True)
    st.code("""
# Devuelve serie de pandas con valores nulos por columna
df.isnull().sum()""")
    st.dataframe(pd.DataFrame(df.isnull().sum()))
    st.markdown(f"""
<div style="text-align: justify;">
                
Se observa que las únicas columnas con valores nulos son **Income** y aquellas relacionadas con los **productos** consumidos por los clientes. 
Solamente tienen 24 valores nulos.
Teniendo en cuenta que nuestro DataFrame tiene {df.shape[0]} filas, no pasará nada si eliminamos dichos valores nulos.
Para eliminarlos simplemente ejecutamos la siguiente línea de código.

</div>
""", unsafe_allow_html=True)
    st.code("""
# Eliminar valores nulos y resetear el index
df = df.dropna().reset_index(drop=True)
""")
# Solo hay 24 valores nulos en Income así que los eliminamos 
    df = df.dropna().reset_index(drop=True)
# Creamos una columna de edad que es mejor que Year Birth
    df["Age"] = df["Year_Birth"].apply(lambda x : datetime.now().year - x)

    
    #EDAD
    st.markdown(f"""
    <div style="text-align: justify;">
                    
    ### Estudio de la variable edad
    En nuestro DataFrame se registra la fecha de nacimiento de los individuos en lugar de su edad.
    Sin embargo, resulta más práctico y comprensible trabajar con edades en lugar de fechas de nacimiento.
    Por ello, vamos a crear una nueva columna de edad a partir de la columna *Year_Birth* con la siguiente línea de código:
    </div>
    """, unsafe_allow_html=True)

    st.code('''
    from datetime import datetime

    # Creamos una columna de edad que es más conveniente que Year Birth
    df["Age"] = df["Year_Birth"].apply(lambda x: datetime.now().year - x)
    ''')       

    st.markdown("""
    <div style="text-align: justify;">

    Una forma visual y sencilla de estudiar la distribución de una variable numérica es representarla con un **boxplot** y un **histograma**.
    En la siguiente figura se muestran estos dos gráficos para la variable *Age* que acabamos de crear. 
    Además, podrás seleccionar un factor de Tukey para eliminar los valores atípicos
    y observar cómo cambia la distribución en función del factor elegido.

    </div>              
    """, unsafe_allow_html=True)

    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(7, 4), dpi=200)

    tukey_factor = st.slider(label="Escoge factor de Tukey (más elevado implica eliminar menos outliers)",
                            max_value=5., min_value=0.2, step=0.1, value=1.5)

    age_without_outliers = utils_frontend.apply_tuckey(numeric_col=df["Age"], tukey_factor=tukey_factor)

    utils_frontend.mostrar_boxplot(age_without_outliers, ax=axes[0])

    utils_frontend.mostrar_histograma(age_without_outliers, ax=axes[1])

    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

Una manera más análitica de analizar la distribución de una variable es usando el método ```describe()``` 
sobre una serie de pandas. Con este método obtendremos métricas estadísticas útiles sobre la variable en cuestión.
Veamos que nos dice dicho método acerca de la variable *age*
""", unsafe_allow_html=True)
    st.code("""
df["Age"].describe()
""")
    st.dataframe(df["Age"].describe().T)
    st.markdown("""
<div style="text-align: justify;">
Parece que hay individuos con edades superiores a 120.
No creemos que sean demasiado representativos. 
Lo mejor que podemos hacer es eliminarlos de nuestro conjunto de datos con las siguientes líneas de código.
""", unsafe_allow_html=True)
    
    st.code("""
                
# Calcula el z-score de la edad
age_zscore = zscore(df['Age'])

# Filtra los valores atípicos basados en el z-score
threshold = 3
df = df[(age_zscore < threshold) & (age_zscore > -threshold)]""")
# Calcula el z-score de la edad
    age_zscore = zscore(df['Age'])

# Filtra los valores atípicos basados en el z-score
    threshold = 3
    df = df[(age_zscore < threshold) & (age_zscore > - threshold)]
    st.markdown("""
<div style="text-align: justify;">
                
Tras la eliminación de valores atípicos, observamos que la distribución de la edad se concentra principalmente alrededor de los 50 años,
siendo este el valor más común en nuestra base de datos. La edad promedio es de aproximadamente 55 años, con un valor mínimo de 28 y un máximo de 84.
 </div>
""", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(df['Age'].describe().T))

    st.markdown("""
<div style="text-align: justify;">
                
Con el propósito de categorizar a nuestros individuos en distintos grupos de edad, hemos introducido la variable 'Age group', la cual divide a nuestros individuos en 5 grupos. Para lograr esto, se ha utilizado el siguiente código:
 </div>
""", unsafe_allow_html=True)
    st.code("""
# Función para crear categoría en la variable age
def category_age(age):
    if age <= 18:
        return '0-18'
    elif age <= 30:
        return '19-30'
    elif age <= 50:
        return '31-50'
    elif age <= 70:
        return '51-70'
    else:
        return '71+'

# Creamos nuestra nueva variable a partir de la función anterior
df['Age_Group'] = df["Age"].apply(category_age)
""")
    age_groups = []

# Iteramos sobre las edades y alas asignamos a la lista según su condición
    def category_age(age):
        if age <= 18:
            return '0-18'
        elif age <= 30:
            return '19-30'
        elif age <= 50:
            return '31-50'
        elif age <= 70:
            return '51-70'
        else:
            return '71+'

# Creamos nuestra nueva variable a partir de la lista anterior
    df['Age_Group'] = df['Age'].apply(category_age)

    fig,ax = plt.subplots()
    utils_frontend.mostrar_countplot(df, "Age_Group", ax)
    st.pyplot(fig)
    st.markdown("""
<div style="text-align: justify;">

### Análisis de la variable educación y su relación con la edad.
La columna *Education* de nuestro DataFrame indica el nivel de educación que tiene cada individuo.
Observemos como se distribuye esta variable categórica a través de un gráfico de barras.
 </div>
""", unsafe_allow_html=True)
    
    #Countplot de Educación
    
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    utils_frontend.mostrar_countplot(df, 'Education', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
    st.markdown("""
<div style="text-align: justify;">

El grupo mayoritorio es claramente el formado por los graduados.
Por otro lado, el minoritario está formado por aquellos de formación *Basic*.
Lo que más llama la atención es que nuestros individuos tienen un nivel de estudios
bastante elevado en general. 
                
### ¿Cómo se distribuye la educación en función de la edad? ¿Y la edad en función de la educación?

Las siguientes dos tablas resolverán ambas preguntas
En la primera tienes que escoger un grupo de edad para ver su distribución en educación.
En la segunda tienes que escoger un nivel educativo para ver su distribución de edad.
 </div>
""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        age_group = st.selectbox("Escoge un grupo de edad",
                                options=df["Age_Group"].unique()) 
        df_filter = df[df["Age_Group"]==age_group].copy()
        st.write(f"Distribución educación en {age_group}")
        st.dataframe(utils_frontend.calcular_conteo_y_porcentaje(df_filter["Education"]))
    with col2:
        education_group = st.selectbox("Escoge un nivel educativo",
                                       options=df["Education"].unique())
        df_filter = df[df["Education"]==education_group]
        st.write(f"Distribución de la edad en {education_group}")
        st.dataframe(df_filter["Age"].describe()[["mean", "std", "25%", "50%", "75%"]].T)
    
    st.markdown("""
<div style="text-align: justify;">
                              
Parece que todo se distribuye más o menos igual.
Destacar que los más jóvenes son muy pocos y, por tanto, no se tiene una distribución 
de la educación consistente en comparación con otras edades.
 </div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align: justify;">

### Análisis de la variable *Marital_Status*
                              
El recuento de la variable 'marital status' revela que la mayoría de los individuos en nuestra muestra están casados (857),
seguidos por aquellos que están en pareja pero no casados (572) y los solteros (470). Además, se observa una cantidad significativa de individuos divorciados (231).
Sin embargo, hay categorías menos frecuentes, como viudos (76), personas que viven solas (Alone, 3), casos clasificados como 'Absurd' (2) y 'YOLO' (2).
Se ha decidido eliminar las categorías 'YOLO' y 'Absurd' ya que carecen de sentido e incluir 'Soltería' dentro del grupo de los solteros. Una vez aplicados estos cambios, la variable 'Marital Status'
se distribuye de la siguiente manera. 
 </div>
""", unsafe_allow_html=True)
    
    categorias_a_eliminar = ['Absurd', 'YOLO']
    df = df[~df['Marital_Status'].isin(categorias_a_eliminar)]
    df['Marital_Status'] = df['Marital_Status'].str.replace('Alone','Single')
    df = df.reset_index()

    st.dataframe(utils_frontend.calcular_conteo_y_porcentaje(df["Marital_Status"]))

    st.markdown("""
<div style="text-align: justify;">

### ¿Cómo se distribuye la renta de nuestros clientes?.
                              
Para obtener una buena visualización, aplicaremos el mismo método que con la variable 'Age' para observar si es necesario eliminar outliers.
 </div>
""", unsafe_allow_html=True)
    
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(7, 4), dpi=200)

    tukey_factor = st.slider(label="Escoge factor de Tukey (un valor más elevado implica eliminar menos outliers)",
                            max_value=10., min_value=0.2, step=0.1, value=1.5)

    income_without_outliers = utils_frontend.apply_tuckey(numeric_col=df["Income"], tukey_factor=tukey_factor)

    utils_frontend.mostrar_boxplot(income_without_outliers, ax=axes[0])

    utils_frontend.mostrar_histograma(income_without_outliers, ax=axes[1])

    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

Tras observar detalladamente los datos, hemos decidido aplicar el mismo método de z-score que utilizamos para la variable 'Age' para filtrar la muestra y eliminar los outliers,
utilizando un umbral de 3 desviaciones estándar.
 </div>
""", unsafe_allow_html=True)
    
    zscore_income = zscore(df['Income'])
    threshold=3
    df = df[(zscore_income<threshold) & (zscore_income>-threshold)]

    st.markdown("""
<div style="text-align: justify;">

Para obtener más información sobre nuestra variable,
observemos como se distribuye la renta en función de la variable categórica que selecciones.
 </div>
""", unsafe_allow_html=True)

    variables_categoricas = ['Education', 'Marital_Status', "Age_Group"]
    variable_seleccionada = st.selectbox("Selecciona una variable categórica", options=variables_categoricas)
    st.dataframe(df.groupby(variable_seleccionada)["Income"].describe())
    st.markdown("""
<div style="text-align: justify;">

Destaca mucho las diferencias en la renta que existen en función del nivel educativo de los individuos.
 </div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align: justify;">

### Análisis de Kidhome Y Teenhome de los clientes.
                              
A través del siguiente gráfico, observamos el recuento de niños y adolescentes que tienen nuestros clientes en sus hogares.
 </div>
""", unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))


    utils_frontend.mostrar_countplot(df, "Kidhome", ax=axes[0])

    utils_frontend.mostrar_countplot(df, "Teenhome", ax=axes[1])


    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

### Análisis de la variable Dt Customer.
                              
Esta variable hace referencia a la fecha en la que nuestros clientes se unieron a la empresa. Para obtener una agrupación más específica,
nos hemos quedado únicamente con el año de las fechas en cuestión. Una vez realizados los cambios, la agrupación queda de la siguiente manera:
 </div>
""", unsafe_allow_html=True)
    
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
    df['Dt_Customer'] = df['Dt_Customer'].dt.year

    fig, ax = plt.subplots()
    utils_frontend.mostrar_countplot(df, 'Dt_Customer', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

### Análisis de la variable Recency.
                              
La variable *Recency* nos indica la media de días que hay entre las compras de un individuo.
Por ejemplo, si un individuo tiene una *Recency* de $50$ entonces, de media, hay $50$ días entre compra y compra de dicho individuo.
Observemos como se distribuye esta variable numérica a través de un histograma y un boxplot.
 </div>
""", unsafe_allow_html=True) 
   
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(7, 4), dpi=200)

    utils_frontend.mostrar_boxplot(df["Recency"], ax=axes[0])

    utils_frontend.mostrar_histograma(df["Recency"], ax=axes[1])
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

**Pregunta**: ¿Cuánto más elevado sea el Income más elevado será el Recency o al revés?
Para responder esta pregunta podemos usar un simple *scatterplot* y observar la correlación entre ambas variables.
 </div>
""", unsafe_allow_html=True) 
    fig,ax = plt.subplots(figsize=(7, 5), dpi=200)
    utils_frontend.mostrar_scatterplot(x=df["Income"], y=df["Recency"], ax=ax)
    st.pyplot(fig)
    st.markdown("""
<div style="text-align: justify;">

Observando el gráfico de arriba queda claro que no existe ninguna **relación lineal** entre el *income* y el *recency*. 
¿Habrá relaciones entre Recency y las variables categóricas que ya hemos estudiado? 
Con la siguiente tabla y gráfico dinámicos podremos encontrar la respuesta a esta pregunta de forma sencilla.

 </div>
""", unsafe_allow_html=True) 
    variable_categorica = st.selectbox("Selecciona una variable categórica",
                                       options=["Age_Group", "Marital_Status", "Education"])
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df.groupby(variable_categorica)["Recency"].describe()[["mean", "25%", "50%", "75%"]]) 
    with col2:
        means = df.groupby(variable_categorica)["Recency"].mean().sort_values(ascending=False)
        fig,ax = plt.subplots(figsize=(5, 5))
        sns.barplot(x=means.index, y=means.values, ax=ax)
        ax.set_xlabel(f"Categorías de {variable_categorica}")
        ax.set_ylabel("Media en Recency")
        st.pyplot(fig)
    st.markdown("""
<div style="text-align: justify;">

Es realmente interesante. Parece que la Recency es igual para cualquier categoría de clientes.

 </div>
""", unsafe_allow_html=True) 
    
    st.markdown("""
<div style="text-align: justify;">

### Análisis de la variable Complain.
                              
La variable complain es una variable dummy que toma el valor 1 si el cliente ha presentado alguna queja en los últimos dos años y 0 en caso contrario.
A continuación, presentamos la distribución de esta variable a través de la siguiente tabla, 
la cual permite filtrar por diferentes variables categóricas para profundizar en el análisis de complain.
 </div>
""", unsafe_allow_html=True)
    
    variable_categorica = st.selectbox("Selecciona una categoría", options=["Age_Group", "Marital_Status", "Education"])
    complain_counts = df.groupby(variable_categorica)['Complain'].value_counts().unstack().fillna(0)
    complain_counts.columns = ['0', '1']

    complain_percentages = complain_counts.div(complain_counts.sum(axis=1), axis=0) * 100
    complain_percentages = complain_percentages.round(2).astype(str) + '%'
    complain_percentages.columns = ['% 0', '% 1']

    complain_table = pd.concat([complain_counts, complain_percentages], axis=1)

    st.dataframe(complain_table)

    st.markdown("""
<div style="text-align: justify;">

Se observa que el número de quejas de nuestros clientes es muy reducido en todas las categorías,
con un número muy pequeño de quejas en cada una de ellas. 
 </div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align: justify;">

### Análisis de las variables relacionadas con los productos.
                              
Las variables asociadas con nuestros productos representan la cantidad comprada por cada cliente para cada uno de nuestros distintos productos.
Para profundizar en el análisis del consumo de nuestros clientes, comenzaremos observando la cantidad total consumida de cada producto.
 </div>
""", unsafe_allow_html=True) 
    
    productos = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts']
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    utils_frontend.mostrar_acumulado(df,productos,ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">
                              
Se observa claramente que el producto más consumido por nuestros clientes es el vino, seguido de los productos cárnicos. 
Posteriormente, el consumo de los demás productos es más homogéneo. Sin embargo, para comprender más profundamente la relación entre el consumo de cada producto y las
características de los clientes, utilizaremos gráficos interactivos.Estos nos permitirán explorar las relaciones de cada producto seleccionado
con cualquier variable categórica que divida a nuestros clientes según sus características.
 </div>
""", unsafe_allow_html=True)

    variable_categorica = st.selectbox("Selecciona la variable categórica",
                                   options=["Age_Group", "Marital_Status", "Education"])
    producto = st.selectbox("Selecciona un producto",
                        options=['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts'])  

    col1, col2 = st.columns(2)

    with col1:
        filtered_means = df.groupby(variable_categorica)[producto].mean()
        st.dataframe(filtered_means)
#print("hola, gracias por leer hasta aquí :)")
    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=filtered_means.index, y=filtered_means.values, ax=ax)
        ax.set_xlabel(f"Categorías de {variable_categorica}")
        ax.set_ylabel(f"Media del consumo de {producto}")
        st.pyplot(fig)  

    st.markdown("""
<div style="text-align: justify;">

### ¿Han sido efectivas nuestras campañas publicitarias?
                              
En el siguiente gráfico, se presentan las variables relacionadas con nuestras campañas publicitarias.
Un valor de 1 indica que el cliente ha realizado una compra después de esa campaña, mientras que un valor de 0 indica lo contrario.
La variable 'response' se refiere a la última campaña.
 </div>
""", unsafe_allow_html=True)
    
    campañas = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    utils_frontend.mostrar_acumulado(df,campañas,ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">

### ¿Qué canales prefieren nuestros clientes para realizar sus compras?
                              
 El análisis de estas variables nos permite comprender cómo los clientes interactúan con la empresa a través de diferentes canales de compra,
 lo que nos ayuda a identificar patrones de comportamiento, preferencias y oportunidades de mejora en las estrategias de ventas y marketing.
 Al igual que para el caso de los productos comenzaremos observando el número total de compras realizadas a través de cada canal.
 </div>
""", unsafe_allow_html=True)
    
    canales = [ 'NumDealsPurchases', 'NumWebPurchases','NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth']
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    utils_frontend.mostrar_acumulado(df,canales,ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify;">
                              
Como se puede observar, la mayoría de las compras se realizan en tiendas físicas, seguidas por las compras en línea.
Sin embargo, es crucial comprender las características de nuestros clientes que están asociadas con estos tipos de compras.
Esto es lo que exploraremos en nuestro próximo gráfico interactivo.
 </div>
""", unsafe_allow_html=True)
    
    variable_categorica = st.selectbox("Seleccionar variable categórica",
                                   options=["Age_Group", "Marital_Status", "Education"])
    canales = st.selectbox("Selecciona un canal de compra",
                        options=['NumDealsPurchases', 'NumWebPurchases','NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth'])  

    col1, col2 = st.columns(2)

    with col1:
        filtered_means = df.groupby(variable_categorica)[canales].sum()
        st.dataframe(filtered_means)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=filtered_means.index, y=filtered_means.values, ax=ax)
        ax.set_xlabel(f"Categorías de {variable_categorica}")
        ax.set_ylabel(f"Total de compras a través de {canales}")
        st.pyplot(fig)  


    st.markdown("""
<div style="text-align: justify;">
                              
Debido a la limitada muestra de datos que tenemos, el grupo de edad más joven apenas muestra significancia en cualquier canal de compra.
Por otro lado, los demás grupos de edad comparten una distribución similar, siendo el grupo de edad de 51 a 70 años el que realiza más compras a través de todos los canales.
                
En cuanto al estado civil, los casados y los que tienen pareja son los que lideran en todos los canales de compra, seguidos por los solteros.
Por otro lado, aquellos que menos compras realizan son los divorciados y los viudos.
                
Los graduados son los que realizan más compras a través de todos los canales,
marcando una clara diferencia con respecto a los demás niveles educativos.
Esta tendencia tiene sentido, dado que la categoría de graduados es la más representativa en nuestra muestra.
 </div>
""", unsafe_allow_html=True)
    

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
                default=[]
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
                default=[]
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
                default=[]
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
                default=[]
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

URL_BACKEND = "http://127.0.0.1:8000/"
URL_BACKEND = "https://tfm-z7o5.onrender.com/"
def make_prediction_vino(input_data):
    # Check if the request was successful
    if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
    else:
            headers = {"Authorization": st.session_state.token}
            response = requests.post(url=f"{URL_BACKEND}predictions/best_model_wines", json=input_data, headers=headers)
            # Obtener el valor del JSON y convertirlo a un número de punto flotante
            predicted_quantity = float(response.json()["prediction_output"]["1"]["predicted_quantity"])

            # Redondear el valor a un número entero
            rounded_prediction = round(predicted_quantity)

            st.success(f"Se espera que la cantidad de vino comprada por este individuo es de : {rounded_prediction}")

def make_prediction_fish(input_data):
    # Check if the request was successful
    if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
    else:
            headers = {"Authorization": st.session_state.token}
            response = requests.post(url=f"{URL_BACKEND}predictions/best_model_fish", json=input_data, headers=headers)
            # Obtener el valor del JSON y convertirlo a un número de punto flotante
            predicted_quantity = float(response.json()["prediction_output"]["1"]["predicted_quantity"])

            # Redondear el valor a un número entero
            rounded_prediction = round(predicted_quantity)

            st.success(f"Se espera que la cantidad de pescado comprada por este individuo es de : {rounded_prediction}")

def make_prediction_meat(input_data):
    # Check if the request was successful
    if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
    else:
            headers = {"Authorization": st.session_state.token}
            response = requests.post(url=f"{URL_BACKEND}predictions/best_model_meat", json=input_data, headers=headers)
            # Obtener el valor del JSON y convertirlo a un número de punto flotante
            predicted_quantity = float(response.json()["prediction_output"]["1"]["predicted_quantity"])

            # Redondear el valor a un número entero
            rounded_prediction = round(predicted_quantity)

            st.success(f"Se espera que la cantidad de carne comprada por este individuo es de : {rounded_prediction}")

def make_prediction_sweet(input_data):
    # Check if the request was successful
    if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
    else:
            headers = {"Authorization": st.session_state.token}
            response = requests.post(url=f"{URL_BACKEND}predictions/best_model_sweet", json=input_data, headers=headers)
            # Obtener el valor del JSON y convertirlo a un número de punto flotante
            predicted_quantity = float(response.json()["prediction_output"]["1"]["predicted_quantity"])

            # Redondear el valor a un número entero
            rounded_prediction = round(predicted_quantity)

            st.success(f"Se espera que la cantidad de dulces comprada por este individuo es de : {rounded_prediction}")
def make_prediction_fruit(input_data):
    # Check if the request was successful
    if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
    else:
            headers = {"Authorization": st.session_state.token}
            response = requests.post(url=f"{URL_BACKEND}predictions/best_model_fruits", json=input_data, headers=headers)
            # Obtener el valor del JSON y convertirlo a un número de punto flotante
            predicted_quantity = float(response.json()["prediction_output"]["1"]["predicted_quantity"])

            # Redondear el valor a un número entero
            rounded_prediction = round(predicted_quantity)

            st.success(f"Se espera que la cantidad de fruta comprada por este individuo es de : {rounded_prediction}")

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
    year_customer_entered = st.text_input("Año de Ingreso del Cliente", "2013")
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
            1: {"age": age,
            "education": education,
            "marital_status": marital_status,
            "income": income,
            "kidhome": kidhome,
            "teenhome": teenhome,
            "year_customer_entered": year_customer_entered,
            "recency": recency,
            "complain": 1 if complain == "Sí" else 0}
        }
        
        # Make prediction
        if option == "Vino":
            prediction = make_prediction_vino(input_data)
        elif option == "Fruit":
            prediction = make_prediction_fruit(input_data)
        elif option == "Meat":
            prediction = make_prediction_meat(input_data)
        elif option == "Fish":
            prediction = make_prediction_fish(input_data)
        elif option == "Sweet":
            prediction = make_prediction_sweet(input_data)

  
        if prediction is not None:
            st.write(f"Predicción realizada: {prediction}")

def excel_prediction_fish(input_data, df_pred ):
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión")
        return df_pred

    headers = {"Authorization": st.session_state.token}
    response = requests.post(url=f"{URL_BACKEND}predictions/best_model_fish", json=input_data, headers=headers)
    
    if response.status_code == 200:
        prediction_output = response.json()["prediction_output"]
        
        def create_predicted_amount(row):
            return prediction_output[f"{row.name}"]["predicted_quantity"]
        
        df_pred["predicted_fish"] = df_pred.apply(create_predicted_amount, axis=1)
    else:
        st.error(f"Error al obtener las predicciones del servidor")
    
    return df_pred

def excel_prediction_vino(input_data, df_pred ):
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión")
        return df_pred

    headers = {"Authorization": st.session_state.token}
    response = requests.post(url=f"{URL_BACKEND}predictions/best_model_wines", json=input_data, headers=headers)
    
    if response.status_code == 200:
        prediction_output = response.json()["prediction_output"]
        
        def create_predicted_amount(row):
            return prediction_output[f"{row.name}"]["predicted_quantity"]
        
        df_pred["predicted_vino"] = df_pred.apply(create_predicted_amount, axis=1)
    else:
        st.error(f"Error al obtener las predicciones del servidor")
    
    return df_pred

def excel_prediction_meat(input_data, df_pred ):
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión")
        return df_pred

    headers = {"Authorization": st.session_state.token}
    response = requests.post(url=f"{URL_BACKEND}predictions/best_model_meat", json=input_data, headers=headers)
    
    if response.status_code == 200:
        prediction_output = response.json()["prediction_output"]
        
        def create_predicted_amount(row):
            return prediction_output[f"{row.name}"]["predicted_quantity"]
        
        df_pred["predicted_meat"] = df_pred.apply(create_predicted_amount, axis=1)
    else:
        st.error(f"Error al obtener las predicciones del servidor")
    
    return df_pred

def excel_prediction_sweet(input_data, df_pred ):
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión")
        return df_pred

    headers = {"Authorization": st.session_state.token}
    response = requests.post(url=f"{URL_BACKEND}predictions/best_model_sweet", json=input_data, headers=headers)
    
    if response.status_code == 200:
        prediction_output = response.json()["prediction_output"]
        
        def create_predicted_amount(row):
            return prediction_output[f"{row.name}"]["predicted_quantity"]
        
        df_pred["predicted_sweet"] = df_pred.apply(create_predicted_amount, axis=1)
    else:
        st.error(f"Error al obtener las predicciones del servidor")
    
    return df_pred

def excel_prediction_fruit(input_data, df_pred ):
    if "token" not in st.session_state.keys():
        st.warning("Tienes que iniciar sesión")
        return df_pred

    headers = {"Authorization": st.session_state.token}
    response = requests.post(url=f"{URL_BACKEND}predictions/best_model_fruits", json=input_data, headers=headers)
    
    if response.status_code == 200:
        prediction_output = response.json()["prediction_output"]
        
        def create_predicted_amount(row):
            return prediction_output[f"{row.name}"]["predicted_quantity"]
        
        df_pred["predicted_fruit"] = df_pred.apply(create_predicted_amount, axis=1)
    else:
        st.error(f"Error al obtener las predicciones del servidor")
    
    return df_pred


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
        "Income": [58138.0, 46344.0, 71613.5, 26646.0, 58293.0],
        "Kidhome": [0, 1, 0, 1, 1],
        "Teenhome": [0, 1, 0, 0, 0],
        "Dt_Customer": ['04-09-2012', '08-03-2014', '21-08-2013', '10-02-2014', '19-01-2014'],
        "Recency": [58, 38, 26, 26, 94],
        "Complain": [0, 0, 1, 0, 0]
    })
    
    # Mostrar el DataFrame de ejemplo
    st.dataframe(df_plantilla)

    excel_upload = st.file_uploader("Elige un archivo Excel")

    # Place select box at the top of the page
    option = st.selectbox("Selecciona una predicción", ["Vino", "Fruit", "Meat", "Fish", "Sweet"])

    if st.button("Make Prediction"):
            try:
                df_pred = pd.read_excel(excel_upload, thousands=',')
                if "Unnamed: 0" in df_pred.columns:
                    df_pred = df_pred.drop("Unnamed: 0", axis="columns")
                st.markdown("Aquí puedes ver los primeros elementos de tu dataframe:")
                st.dataframe(df_pred)

            except ValueError:
                df_pred = pd.read_csv(excel_upload)
                if "Unnamed: 0" in df_pred.columns:
                    df_pred = df_pred.drop("Unnamed: 0", axis="columns")
                st.markdown("Aquí puedes ver tu dataframe:")
                st.dataframe(df_pred)
            except:
                st.warning("Archivo no válido")

            
            df_pred.columns = [col.lower() for col in df_pred.columns]
            df_plantilla.columns = [col.lower() for col in df_plantilla.columns]

            df_pred["income"] = df_pred["income"].apply(lambda x: float(x))


            if set(df_pred.columns) != set(df_plantilla.columns):
                st.warning("El excel tiene que tener las columnas en el mismo formato que la plantilla")
            df_pred = df_pred[df_plantilla.columns]
            dtype_correct = True
            for col in df_plantilla:
                if str(df_plantilla[col].dtype) != str(df_pred[col].dtype):
                    st.warning(f"La columna {col} no está en el formato requerido.")
                    dtype_correct = False 
                    break 

            df_pred["year_customer_entered"] = df_pred["dt_customer"].apply(lambda x: str(x).split("-")[2])
            
            if dtype_correct:
                input_data = {}
                def save_data(row):
                    data = {"age": row["age"],"education": row["education"],"marital_Status": row["marital_status"],
                        "income": row["income"],"kidhome": row["kidhome"],"teenhome": row["teenhome"],
                        "year_customer_entered": row["year_customer_entered"],"recency": row["recency"], "complain": row["complain"]}
                    input_data[row.name] = data
                df_pred.apply(save_data, axis=1)

                if option == "Vino":
                    df_pred = excel_prediction_vino(input_data, df_pred)
                elif option == "Fruit":
                    df_pred = excel_prediction_fruit(input_data, df_pred)
                elif option == "Meat":
                    df_pred = excel_prediction_meat(input_data, df_pred)
                elif option == "Fish":
                    df_pred = excel_prediction_fish(input_data, df_pred)
                elif option == "Sweet":
                    df_pred = excel_prediction_sweet(input_data, df_pred)

                st.markdown("Aquí tienes tu DataFrame con la predicción")
                st.dataframe(df_pred.drop(columns=["year_customer_entered"]))

def prediccion_cantidad():
    if "input_data_cantidad" not in st.session_state:
        st.session_state.input_data_cantidad = []

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Edad del individuo.", min_value=20, max_value=80)
        education = st.selectbox("Education", options=["Graduation", "PhD", "Master", "2n Cycle", "Basic"])
        marital_status = st.selectbox("Marital Status", options=["Single", "Together", "Married", "Widow", "Divorced"])
    
    with col2:
        income = st.number_input(label="Income", min_value=5000)
        kidhome = st.number_input(label="kidhome", min_value=0)
        teenhome = st.number_input(label="Teenhome", min_value=0)
    
    with col3:
        recency = st.number_input(label="Recency", min_value=1, max_value=200)
        year_customer_entered = st.number_input(label="Year customer entered", min_value=2010, max_value=2020)
        complain = st.selectbox(label="Complain", options=["0", "1"])
    
    if st.button(label="Save info customer"):
        row = {
            "age": age, "education": education, "marital_status": marital_status,
            "income": income, "kidhome": kidhome, "teenhome": teenhome, 
            "year_customer_entered": str(year_customer_entered), "recency": recency,
            "complain": int(complain)
        }
        st.session_state.input_data_cantidad.append(row)
    
    if len(st.session_state.input_data_cantidad) != 0:
        st.dataframe(pd.DataFrame(st.session_state.input_data_cantidad))
    
    if st.button(label="Delete DataFrame", type="primary"):
        st.session_state.input_data_cantidad = []
        st.rerun()
    
    model_pred = st.selectbox("Escoge el modelo", options=["fish", "meat", "sweet", "wines", "fruits"])
    
    if st.button("Hacer predicción"):
        if "token" not in st.session_state.keys():
            st.warning("Tienes que iniciar sesión")
        else:
            headers = {"Authorization": st.session_state.token}
            dict_input_data = {index: row for index, row in enumerate(st.session_state.input_data_cantidad)}
            response = requests.post(f"{URL_BACKEND}predictions/best_model_{model_pred}", headers=headers, json=dict_input_data)

            if response.status_code == 401:
                st.warning("La sesión ha caducado")
            else:
                predictions = response.json()
                predicted_quantities = [pred[f"predicted_quantity"] for pred in predictions["prediction_output"].values()]
                df = pd.DataFrame(st.session_state.input_data_cantidad)
                alimento = (model_pred.split("_")[-1:][0])
                df[f"Predicted_{alimento}"] = predicted_quantities
                st.dataframe(df)



def prediccion_consumo():
    indice = st.radio("¿Qué quieres ver aquí?", options=["Exploratory Data Analysis", "Descripción del proyecto", "¿Quiéres entender tus datos?", "¿Quiéres realizar una predicción única?", "¿Quiéres realizar una predicción sobre un EXCEL?", "¿Quiéres realizar una única predicción?"])
    if indice=="Exploratory Data Analysis":
        exploratory_data_analysis()
    elif indice == "Descripción del proyecto":
        descripcion_del_proyecto()
    elif indice == "¿Quiéres entender tus datos?":
        run_eda()
    elif indice == "¿Quiéres realizar una predicción única?":
        prediccion_unica()
    elif indice == "¿Quiéres realizar una predicción sobre un EXCEL?":
        prediccion_excel()
    elif indice == "¿Quiéres realizar una única predicción?":
        prediccion_cantidad()