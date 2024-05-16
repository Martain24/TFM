import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st
sns.set_style("whitegrid")


def apply_tuckey(numeric_col: pd.Series, tukey_factor: float = 1.5):
    # Calcular los cuartiles Q1 y Q3
    q1, q3 = numeric_col.describe()["25%"], numeric_col.describe()["75%"]
    # Calcular el rango intercuartílico (IQR)
    iqr = q3 - q1
    # Calcular los límites superior e inferior según el factor de Tukey
    ceiling, floor = q3 + tukey_factor * iqr, q1 - tukey_factor * iqr 
    # Devolver solo los valores que están dentro de los límites
    return numeric_col[(floor <= numeric_col) & (numeric_col <= ceiling)]

def mostrar_boxplot(numeric_col: pd.Series, ax):
    sns.boxplot(numeric_col, ax=ax, color="skyblue")  
    ax.set_title(f'Boxplot de {numeric_col.name}')
    ax.set_ylabel(numeric_col.name)
    ax.spines[['right', 'top']].set_visible(False)

def mostrar_histograma(numeric_col: pd.Series, ax):
    # Obtener los cuartiles Q1, Q2 (mediana) y Q3
    q1, q2, q3 = numeric_col.describe()["25%"], numeric_col.describe()["50%"], numeric_col.describe()["75%"]
    # Dibujar el histograma
    sns.histplot(numeric_col, bins=10, color='skyblue', edgecolor='black', ax=ax) 
    # Añadir líneas verticales para los cuartiles
    ax.axvline(q1, c="red", ls="--", label=f"Q1 = {q1:.2f}")
    ax.axvline(q2, c="green", ls="--", label=f"Q2 = {q2:.2f}")
    ax.axvline(q3, c="black", ls="--", label=f"Q3 = {q3:.2f}")
    ax.set_title(f'Histograma de {numeric_col.name}')
    ax.set_xlabel(numeric_col.name)
    ax.set_ylabel('Frecuencia')
    ax.spines[['right', 'top']].set_visible(False)
    ax.legend()

def mostrar_countplot(df, variable, ax):
    sns.countplot(data=df, x=variable, ax=ax)
    ax.set_xlabel(variable)
    ax.set_ylabel('Count')
    ax.set_title(f'Countplot de {variable}')
    ax.spines[['right', 'top']].set_visible(False)

def contar_valores_por_grupo(df, variable_grupo, variable_contar):
    choose_grupo = st.selectbox("Escoge un grupo", options=df[variable_grupo].unique())
    df_filtrado = df[df[variable_grupo] == choose_grupo]
    count_df = pd.DataFrame()
    count_df.index = df_filtrado[variable_contar].value_counts().index 
    count_df[f"Conteo de {variable_contar} en grupo {choose_grupo}"] = df_filtrado[variable_contar].value_counts().values 
    count_df[f"En porcentajes"] = df_filtrado[variable_contar].value_counts(normalize=True).values * 100
    st.dataframe(count_df)

def calcular_conteo_y_porcentaje(columna_categorica: pd.Series):
    
    conteo = columna_categorica.value_counts()
    porcentaje = (columna_categorica.value_counts(normalize=True)*100).round(1)
    porcentaje_str = porcentaje.astype(str) + '%'
    return pd.DataFrame({'Conteo': conteo, 'Porcentaje': porcentaje_str})

def mostrar_scatterplot(x:pd.Series, y:pd.Series, ax, hue=None):
    df_variables = pd.DataFrame({x.name: x, y.name: y})
    correlacion = df_variables.corr()[x.name][y.name]
    sns.scatterplot(x=df_variables[x.name], y=df_variables[y.name], hue=hue)
    ax.set_title(f"Correlación = {correlacion:.2f}")
    ax.spines[['right', 'top']].set_visible(False)

def mostrar_acumulado(df: pd.DataFrame, variables: list, ax):
    suma_gastos = df[variables].sum()
    ax.bar(suma_gastos.index, suma_gastos)
    ax.set_ylabel('Total')
    ax.tick_params(axis='x', rotation=45)
    
def calcular_conteo_y_porcentaje_2(df, variables_categoricas, variable_contar):
    variable_categorica_elegida = st.selectbox("Selecciona tu variable categórica", options=variables_categoricas)
    df_filtrado = df[df[variable_contar] == 1]
    conteo_por_categoria = df_filtrado.groupby(variable_categorica_elegida)[variable_contar].sum()
    total_por_categoria = df.groupby(variable_categorica_elegida)[variable_contar].sum()
    porcentaje_por_categoria = (conteo_por_categoria.div(total_por_categoria, axis=0) * 100).round(1)
    result = pd.concat([conteo_por_categoria, porcentaje_por_categoria], axis=1, keys=['Conteo', 'Porcentaje'])
    result = result[(result['Conteo'] != 0) | (result['Porcentaje'] != 0)]
    
    return result