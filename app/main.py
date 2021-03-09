import streamlit as st 
import numpy as np 
import pandas as pd 
import sys 
from pathlib import Path 
from  combined_weather_insights import OttawaCombinedProductivity
import os


np.random.seed(100)
dir = Path('/usr/src/app/')
file = 'daily_combined_data.csv'


cwi = OttawaCombinedProductivity(file = file)

class ConstructionProductivityVisualizer(): 
	'''
	A class that builds the visualization dashboard for construvtion worker productivity vs temperature
	'''
	def __init__(self): 
		self.cwi = cwi
		st.set_page_config(layout="wide") 
		st.image('app/fuller_logo.jpg', width = 200)
		st.title('Climate Factors on Construction Worker Productivity')
		
		st.subheader('Thomas Fuller Construction')
		#self.productivity_list = ['productive', 'less productive']
		self.nrc_paper_url = 'https://publications-cnrc.canada.ca/eng/view/ft/?id=52dc96d5-4ba0-40e6-98d2-8d388cba30cd'
		self.month_selector()
		self.side_bar_information()
		self.derive_monthly_work_capacity_insight()

	
	def month_selector(self): 
		self.month = st.select_slider('Select the month for productivity you wish to analyze',
										options = list(self.cwi.month_list))
		fig = self.cwi.plot_productivity_by_month(i = self.cwi.swap_dict[self.month])
		
		st.plotly_chart(fig)

	def derive_monthly_work_capacity_insight(self): 
		worker_rules = {0 : 8, 
						75 : 7.5, 
               			55 : 7.3, 
               			40 : 6.6}
		if st.button(f'Derive Worker Capacities for {self.month}'):
			st.markdown('Based on 4 hour work period we can say with 95 confidence to expect:')
			self.sort_dict = (self.cwi.generate_work_capacity_insights(i = self.cwi.swap_dict[self.month]))
			#self.sort_dict['0'] = 
			for key, value in self.sort_dict.items():
				if key == '0': 
					st.markdown(f'* {value} working af full capacity. (A typical 8 hour workday will have  {worker_rules[int(key[0:2])]} productive hours in it.)')
				else:
					st.markdown(f'* {value} days working at {key}. (A typical 8 hour workday will have  {worker_rules[int(key[0:2])]} productive hours in it.)')
					

	
	def side_bar_information(self): 
		st.sidebar.title('More About This Tool')
		self.choice = st.sidebar.selectbox('Learn more about the methodology used for this tool', 
			('Method', 'Research', 'Assumptions', 'Data'))
		if self.choice == 'Method':
			st.sidebar.markdown(f'The method we used to assemble this tool was by aggregating hourly weather data from the \
			 Ottawa airport from the last ten years.  With this we are able to see clear seasonality and assign monthly productivity \
			  using this function represented by this curve') 
			st.sidebar.plotly_chart(self.cwi.prductivity_figure)
		elif self.choice == 'Research': 
			st.sidebar.markdown( f'The majority of findings used for this analysis was based of the Natioanl Research Council of Canada \
			pulication "Productivity in Construction"  which can be found here: {self.nrc_paper_url}. \
			It serves as a great guide of overall construction productivty and has a candian perspective on the matter.')
		elif self.choice == 'Assumptions': 
			st.sidebar.markdown(f'This tool only considers temerature as it realtes to worker productivity. \
			It takes into account extremes such as wind chill and humidity into the plots and insights you see.\
			However, it does not include other factors such as precipitation and wind strength that are important factors in work site productivity.')
		else: 
			st.sidebar.markdown(f'The data was collected from Government of Canada webside site from the Ottawa airport location\
				and includes a forecasting bounday outlined in the map below')

			df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [45.38, -75.72],columns=['lat', 'lon'])
			st.sidebar.map(df)

if __name__ == "__main__":
    # execute only if run as a script
    ConstructionProductivityVisualizer()