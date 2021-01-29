import streamlit as st
import pandas as pd 
from weather_data_processor import CSVReader
from weather_data_analyzer import OttawaWeatherAnalytics 
import os
cwd = os.getcwd()
cwd

df = CSVReader().df
df




st.title(f'{cwd}')
st.write("looks like this works properly.")
st.write("What happens if you change the file?")