from re import I
import pandas as pd
import datetime
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import pyodbc
from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from PIL import Image
import folium
from streamlit_folium import st_folium
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas_gbq
import pydata_google_auth

credentials = service_account.Credentials.from_service_account_file(
    'onlimo-794bae89654f.json'
)
client = bigquery.Client(credentials=credentials)


files_id = pd.read_csv('id_stasiun.csv')

conn_str = 'DRIVER={SQL Server};server=DESKTOP-ECB4MMH\SQLEXPRESS;Database=awrl;Trusted_Connection=yes;'
con_url = URL.create('mssql+pyodbc', query={'odbc_connect': conn_str})
engine = create_engine(con_url)

id_list = files_id['CODE'].tolist()




def calculate_norm_anomali(x, y):
    for i,df in zip(x, y):
        i['logDate'] = pd.to_datetime(i['logDate']).dt.date
        
        globals() [f'pH_{df}'] = [x for x in i[-24:]['pH']]
        globals() [f'ab_pH_{df}'] = sum(map(lambda x : x<5 and x>9, globals()[f'pH_{df}']))
        globals() [f'DO_{df}'] = [x for x in i[-24:]['DO']]
        globals() [f'ab_DO_{df}'] = sum(map(lambda x : x<1, globals()[f'DO_{df}']))
        globals() [f'NH4_{df}'] = [x for x in i[-24:]['NH4']]
        globals() [f'ab_NH4_{df}'] = sum(map(lambda x : x>100, globals()[f'NH4_{df}']))
        globals() [f'NO3_{df}'] = [x for x in i[-24:]['NO3']]
        globals() [f'ab_NO3_{df}'] = sum(map(lambda x : x>100, globals()[f'NO3_{df}']))
        globals() [f'tgl_{df}'] = i['logDate'].max()


def status_onlimo(id_ol):
    
    st.header(id_ol)
    globals()[f'header_a_{id_ol}'], globals()[f'header_b_{id_ol}'] = st.columns(2)
    
    if globals()[f'tgl_{id_ol}'] == datetime.today().date(): 
        
        globals()[f'header_a_{id_ol}'].button(globals() [f'tgl_{id_ol}'], key=f'{id_ol}_a')
        globals()[f'header_b_{id_ol}'].success('ONLINE')

    elif globals()[f'tgl_{id_ol}'] < datetime.today().date():
        globals()[f'header_a_{id_ol}'].button(globals() [f'tgl_{id_ol}'].strftime('%Y-%m-%d'), key=f'{id_ol}_b')
        globals()[f'header_b_{id_ol}'].warning('OFFLINE')

    else:
        globals()[f'header_a_{id_ol}'].button(globals() [f'tgl_{id_ol}'], key=f'{id_ol}_b')                  
        globals()[f'header_b_{id_ol}'].error('ERROR')   

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('pH', globals() [f'ab_pH_{id_ol}'], '{0:.2f}'. format(globals() [f'pH_{id_ol}'][-1]))
    col2.metric('DO', globals() [f'ab_DO_{id_ol}'], '{0:.2f}'. format(globals() [f'DO_{id_ol}'][-1]))
    col3.metric('NH', globals() [f'ab_NH4_{id_ol}'], '{0:.2f}'. format(globals() [f'NH4_{id_ol}'][-1]))
    col4.metric('NO', globals() [f'ab_NO3_{id_ol}'], '{0:.2f}'. format(globals() [f'NO3_{id_ol}'][-1]))

    st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
df_21 = []
df_12 = []
df_16 = []
df_dlh = []

for dfx in id_list[:15]:
    ID = files_id[files_id['CODE'] == dfx].index.values + 11
    globals() [f'query_{dfx}'] = f"""select pH, DO, Cond, Turb, Temp, NH4,NO3,ORP,COD,BOD,TSS,logTime as NH3_N,logDate, datepart(hour, logTime) as logTime from data where Station={int(ID)} order by logDate,logTime"""
    globals() [f'{dfx}'] = pd.read_sql(globals() [f'query_{dfx}'], engine)
    df_21.append(globals() [f'{dfx}'])

for df1 in id_list[10:21]:
    ID = files_id[files_id['CODE']==df1].index.values+11
    globals()[f'{df1}']=pandas_gbq.read_gbq(f'SELECT * FROM Ma.Sensor where Station={int(ID)} LIMIT 10', credentials=credentials)
    globals() [f"{df1}['logDate']"] = pd.to_datetime(globals() [f'{df1}']['logDate']).dt.date
    df_12.append(globals() [f'{df1}'])

calculate_norm_anomali(df_21, id_list[:10])
calculate_norm_anomali(df_12, id_list[10:21])


image = Image.open('frame.PNG')
st.image(image) 

ol_16, ol_21, ol_12, ol_dlh = st.tabs(['ONLIMO 16 🌐', 'ONLIMO 21 💠', 'ONLIMO 12 🌀', 'ONLIMO DLH 📮'])   
with ol_21:
    
    for i in id_list[:15]:
        status_onlimo(i)

with ol_12:

    for y in id_list[10:21]:
        status_onlimo(y)

