import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import zscore
import seaborn as sns

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
    st.markdown("""
<div style="text-align: justify;">
                
### Distribución y preprocesado de la edad de los individuos.
Tras realizar un análisis exploratorio de la variable 'age', 
que incluye la creación de un boxplot y un histograma para entender su distribución y posibles valores atípicos.
Se identificaron valores atípicos en la variable de edad, los cuales podrían ser resultado de errores o datos inusuales.
</div>
""", unsafe_allow_html=True)
    

      
    def mostrar_boxplot(variable):
        fig, ax = plt.subplots()
        plt.boxplot(df[variable])  
        ax.set_title(f'Boxplot de {variable}')
        ax.set_xlabel(variable)
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)


    def mostrar_histograma(variable):
        fig, ax = plt.subplots()
        plt.hist(df[variable], bins=10, color='skyblue', edgecolor='black') 
        ax.set_title(f'Histograma de {variable}')
        ax.set_xlabel(variable)
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

#Cambiamos entre gráficos con este botón
    if st.button('Mostrar boxplot de Edad'):
        mostrar_boxplot("Age")

    if st.button('Mostrar histograma de Edad'):
        mostrar_histograma("Age")

    st.markdown("""
<div style="text-align: justify;">
                
Para abordar esta situación, a continuación se muestra el código utilizado para aplicar el método z-score con el fin de detectar y tratar estos outliers:
 </div>
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
    st.dataframe(pd.DataFrame(df['Age'].describe()))
    if st.button('Mostrar boxplot de Edad 2'):
        mostrar_boxplot("Age")

    if st.button('Mostrar histograma de Edad 2'):
        mostrar_histograma("Age")

    st.markdown("""
<div style="text-align: justify;">
                
Con el propósito de categorizar a nuestros individuos en distintos grupos de edad, hemos introducido la variable 'Age group', la cual divide a nuestros individuos en 5 grupos. Para lograr esto, se ha utilizado el siguiente código:
 </div>
""", unsafe_allow_html=True)
    st.code("""
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
    
    st.markdown("""
<div style="text-align: justify;">

### Analisis de la variable Educación y su realción con la edad.
                              
En el gráfico siguiente, se destaca que el nivel de educación más común entre los individuos de nuestra muestra es el de graduado, 
abarcando más de la mitad de la población estudiada, seguido por doctorados y máster, y en menor medida, los de 2º ciclo y nuestra categoría minoritaria, Basic.
Además, este gráfico ofrece la opción de visualizar los datos segmentados por grupos de edad, facilitando un análisis más detallado mediante un botón interactivo integrado en la visualización.
 </div>
""", unsafe_allow_html=True)
    
    #Countplot de Educación
    def mostrar_countplot(variable):
        fig, ax = plt.subplots()
        sns.countplot(data=df, x=variable, ax=ax)
        ax.set_xlabel(variable)
        ax.set_ylabel('Count')
        ax.set_title(f'Countplot de {variable}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig, ax

    fig, ax = mostrar_countplot('Education')
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