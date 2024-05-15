import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import zscore
import seaborn as sns
sns.set_style("whitegrid")
import utils_frontend

def descripcion_del_proyecto():
    st.markdown("""
## Customer segmentation
Aquí escribimos una pequeña descripción/introducción al proyecto
""")
def exploratory_data_analysis():
    st.markdown("""
<div style="text-align: justify;">
                
## Análisis Exploratorio de Datos
Antes de abordar cualquier problema relacionado con los datos, resulta fundamental comprender la naturaleza de los mismos.
Para ello necesitamos sumergirnos en un proceso conocido como análisis exploratorio de datos.
Aquí, presentamos las primeras 5 filas de nuestro DataFrame, un paso inicial en la comprensión de su estructura y contenido.
</div>
""", unsafe_allow_html=True)
    df = pd.read_csv("../primer_dataset/marketing_campaign.csv", sep="\t")
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
   - MntProductosOro: Monto gastado en oro en los últimos 2 años

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
                
Se observa que la única columna con valores nulos es **Income**. 
Solamente tiene 24 valores nulos.
Teniendo en cuenta que nuestro DataFrame tiene {df.shape[0]} filas, no pasará nada si eliminamos dichos valores nulos.
Para eliminarlos simplemente ejecutamos la siguiente línea de código

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

    # Crear una figura con dos subplots (boxplot e histograma)
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(7, 4), dpi=200)

    # Solicitar al usuario que elija el factor de Tukey mediante un slider
    tukey_factor = st.slider(label="Escoge factor de Tukey (más elevado implica eliminar menos outliers)",
                            max_value=5., min_value=0.2, step=0.1, value=1.5)

    # Aplicar el método de Tukey para eliminar outliers en la columna "Age"
    age_without_outliers = utils_frontend.apply_tuckey(numeric_col=df["Age"], tukey_factor=tukey_factor)

    # Mostrar el boxplot de la columna "Age" sin outliers en el primer subplot
    utils_frontend.mostrar_boxplot(age_without_outliers, ax=axes[0])

    # Mostrar el histograma de la columna "Age" sin outliers en el segundo subplot
    utils_frontend.mostrar_histograma(age_without_outliers, ax=axes[1])

    # Ajustar el diseño de la figura y mostrarla en Streamlit
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
    for age in df['Age']:
        if age <= 18:
            age_groups.append('0-18')
        elif age <= 30:
            age_groups.append('19-30')
        elif age <= 50:
            age_groups.append('31-50')
        elif age <= 70:
            age_groups.append('51-70')
        else:
            age_groups.append('71+')

# Creamos nuestra nueva variable a partir de la lista anterior
    df['Age_Group'] = age_groups

    fig,ax = plt.subplots()
    utils_frontend.mostrar_countplot(df, "Age_Group", ax)
    st.pyplot(fig)
    st.markdown("""
<div style="text-align: justify;">

### Analisis de la variable Educación y su realción con la edad.
                              
En el gráfico siguiente, se destaca que el nivel de educación más común entre los individuos de nuestra muestra es el de graduado, 
abarcando más de la mitad de la población estudiada, seguido por doctorados y máster, y en menor medida, los de 2º ciclo y nuestra categoría minoritaria, Basic.
Además, este gráfico ofrece la opción de visualizar los datos segmentados por grupos de edad, facilitando un análisis más detallado mediante un botón interactivo integrado en la visualización.
 </div>
""", unsafe_allow_html=True)
    
    #Countplot de Educación
    
    fig, ax = plt.subplots()
    utils_frontend.mostrar_countplot(df, 'Education', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
    
    # Countplot de Educación por grupos de edad
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Age_Group', hue='Education', ax=ax)
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Count')
    ax.set_title('Countplot de Age Group y Education')
    plt.xticks(rotation=45)
    plt.legend(title='Education', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)

    choose_age_group = st.selectbox("Escoge un grupo de edad",
                                    options=df["Age_Group"].unique())
    df_filter = df[df["Age_Group"] == choose_age_group]
    count_df = pd.DataFrame()
    count_df.index = df_filter["Education"].value_counts().index 
    count_df[f"Conteo Educación en grupo de edad {choose_age_group}"] = df_filter["Education"].value_counts().values 
    count_df[f"En porcentajes"] = df_filter["Education"].value_counts(normalize=True).values * 100
    st.dataframe(count_df)
    st.markdown("""
<div style="text-align: justify;">
                              
Podemos observar que la distribución es consistente en cada grupo de edad, con una excepción notoria en el grupo más joven, donde tenemos una cantidad limitada de observaciones.
 </div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align: justify;">

### Tipos de marital status de nuestros clientes.
                              
El recuento de la variable 'marital status' revela que la mayoría de los individuos en nuestra muestra están casados (857),
seguidos por aquellos que están en pareja pero no casados (572) y los solteros (470). Además, se observa una cantidad significativa de individuos divorciados (231).
Sin embargo, hay categorías menos frecuentes, como viudos (76), personas que viven solas (Alone, 3), casos clasificados como 'Absurd' (2) y 'YOLO' (2).
Se ha decidido eliminar las categorías con recuentos menores a 5 por considerarse poco representativas.
 </div>
""", unsafe_allow_html=True)