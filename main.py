"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.read_csv("primer_dataset/Train.csv")

st.write(f"""
# TFM
Bienvenidos a nuestro pedazo de TFM

Aquí tenemos las 5 primeras filas de nuestro conjunto de datos.    
""")

st.write(df)
