import streamlit as st
import streamlit_folium as st_folium
import folium 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('coor.csv')

st.map(df)
