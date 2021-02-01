import streamlit as st
import pandas as pd 
import numpy as np
from weather_data_processor import CSVReader
from weather_data_analyzer import OttawaWeatherAnalytics 
import os

#df = CSVReader().df
df = pd.read_csv('ottawa hourly_weather.csv', index_col = 0)
ana = OttawaWeatherAnalytics(df)

st.title('Construction Worker Productivity and Temperature')
st.subheader('Thomas Fuller Construction')

#select month, plot, and derive  functionality 
productivity_list = ['productive', 'less productive']
month = st.select_slider('Select the month for productivity you wish to analyze',
	options = list(ana.month_dict.values()))
for number_list, month_list in ana.month_dict.items():
	if month_list == month: 
		st.write(f'For the month of {month} we see an average temperature productivity of {ana.temp_productivity_frames[number_list].iloc[:,1].mean().round(1) * 100}%. \
			With {np.sum(ana.temp_productivity_frames[number_list].iloc[:,1] < .5)} days below 50% productivity.  \
			It stands that {month} is a {np.where(ana.temp_productivity_frames[number_list].iloc[:,1].mean() > .6 ,productivity_list[0], productivity_list[1] )} \
			month when it comes to outdoor construction.  ')
		ana.plot_productivity_by_month(i = number_list)
		st.plotly_chart(ana.plot_productivity_plot)
		
