import pandas as pd
import datetime
from datetime import datetime as dt
import streamlit as st
        
@st.cache(allow_output_mutation=True)
def kunjungan():
    return[]

@st.cache(allow_output_mutation=True)
def kalibrasi():
    return[]

st.title('Laporan Kunjungan Stasiun ONLIMO')
files_id = pd.read_csv('id_stasiun.csv')

st.header('Form pengisian hasil kunjungan')
with st.form("Form Pengisian Hasil Kunjungan "):
    st.write("Form Pengisian Hasil Kunjungan 😀")
    nama = st.text_input("Nama: ")
    stasiun = st.selectbox('Stasiun: ', files_id['CODE'])
    tgl_in = st.date_input('Tanggal masalah terjadi: ')
    masalah = st.text_area('Apa masalahnya? ')
    tgl_out = st.date_input('Tanggal kunjungan: ?')
    tindakan = st.text_area('Apa tindakannya? ')

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write('Terimakasih 👌')
        kunjungan().append({'Nama': nama, 'Stasiun': stasiun, 'Tgl_in': tgl_in, 'Masalah': masalah, 'Tgl_out': tgl_out, 'Tindakan':tindakan})
        lap_kunjungan = pd.DataFrame(kunjungan())
        lap_kunjungan.tail(1).to_csv(f'kunjungan_{stasiun}.csv', mode='a', index = False, header = False)
             
params = ['pH', 'DO', 'NH4', 'NO3', 'COD', 'BOD', 'TSS']

st.header('Form pengisian hasil kalibrasi')
with st.form("Form Kalibrasi"):
    st.write("Form Hasil Kalibrasi 😄")
    name = st.text_input("Nama: ")
    tgl = st.date_input('Tanggal kalibrasi: ')
    station = st.selectbox('Stasiun: ', files_id['CODE'])
    for pr in params[:4]:
        globals() [f'{pr}'] = st.multiselect(f'Sensor {pr}', ['Kalibrasi ulang', 'Ganti electrode', 'Ganti tip'], key=f'{pr}')
    opm = st.multiselect('Tindakan OPM', ['Kalibrasi ulang', 'Ganti UV-Lamp', 'Ganti board'])
    kendala = st.text_area('Apakah ada kendala? ')


   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write('Terimakasih 👌')
        kalibrasi().append({'Nama': name, 'Stasiun': station, 'Tgl': tgl, 'pH': pH, 'DO': DO, 'NH4': NH4, 'NO3': NO3, 'OPM': opm, 'Kendala':kendala})
        lap_kalibrasi = pd.DataFrame(kalibrasi())
        lap_kalibrasi.tail(1).to_csv(f'kalibrasi_{stasiun}.csv', mode='a', index = False, header = False)
        
        
        
        
        
        
        
        
        
        
        
        