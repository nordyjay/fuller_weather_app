import streamlit as st
import pandas as pd 
import numpy as np
import webbrowser
from weather_data_processor import CSVReader
from weather_data_analyzer import OttawaWeatherAnalytics 
import os



class ConstructionProductivityVisualizer(): 
	'''
	A class that builds the visualization dashboard for construvtion worker productivity vs temperature
	'''
	def __init__(self): 
		self.df = CSVReader().df
		self.ana = OttawaWeatherAnalytics(self.df)
		st.set_page_config(layout="wide") 
		st.image('app/fuller_logo.jpg', width = 200)
		st.title('Construction Worker Productivity and Temperature')

		st.subheader('Thomas Fuller Construction')
		self.productivity_list = ['productive', 'less productive']
		self.nrc_paper_url = 'https://publications-cnrc.canada.ca/eng/view/ft/?id=52dc96d5-4ba0-40e6-98d2-8d388cba30cd'
		self.month_selector()
		self.side_bar_information()
	
	def month_selector(self): 
		self.month = st.select_slider('Select the month for productivity you wish to analyze',
										options = list(self.ana.month_dict.values()))
		for self.number_list, self.month_list in self.ana.month_dict.items():
			if self.month_list == self.month: 
				
				st.write(f'For the month of {self.month} we see an average temperature productivity of \
				{self.ana.temp_productivity_frames[self.number_list].iloc[:,1].mean().round(3) *100}%. \
				With {np.sum(self.ana.temp_productivity_frames[self.number_list].iloc[:,1] < .5)} days below 50% productivity.  \
				It stands that {self.month} is a \
				{np.where(self.ana.temp_productivity_frames[self.number_list].iloc[:,1].mean() > .5 ,self.productivity_list[0], self.productivity_list[1])} \
				month when it comes to outdoor construction.')
				self.ana.plot_productivity_by_month(i = self.number_list)
				st.plotly_chart(self.ana.plot_productivity_plot)


	
	def side_bar_information(self): 
		self.choice = st.sidebar.selectbox('Learn more about the methodology used for this tool', 
			('Method', 'Research', 'Assumptions', 'Data'))
		if self.choice == 'Method':
			st.sidebar.markdown(f'The method we used to assemble this tool was by aggregating hourly weather data from the \
			 Ottawa airport from the last ten years.  With this we are able to see clear seasonality and assign monthly productivity \
			  using this function represented by this curve') 
			st.sidebar.plotly_chart(self.ana.prductivity_figure)
		elif self.choice == 'Research': 
			st.sidebar.markdown( f'The majority of findings used for this analysis was based of the Natioanl Research Council of Canada \
			pulication "Productivity in Construction"  which can be found here: {self.nrc_paper_url}. \
			It serves as a great guide of overall construction productivty and has a candian perspective on the matter.')
		elif self.choice == 'Assumptions': 
			st.sidebar.markdown(f'This tool only considers temerature as it realtes to worker productivity. \
			It takes into account extremes such as wind chill and humidity into the plots and insights you see.\
			However, it does not include other factors such as precipitation and wind strength that are important factors in work site productivity.')
		else: 
			st.sidebar.markdown(f'The data was collected from Government of Canada data site')

	




if __name__ == "__main__":
    # execute only if run as a script
    ConstructionProductivityVisualizer()













#st.title('Construction Worker Productivity and Temperature')
#st.subheader('Thomas Fuller Construction')

#select month, plot, and derive  functionality 
#productivity_list = ['productive', 'less productive']
#month = st.select_slider('Select the month for productivity you wish to analyze',
#	options = list(ana.month_dict.values()))
#for number_list, month_list in ana.month_dict.items():
	#if# month_list == month: 
		#st.write(f'For the month of {month} we see an average temperature productivity of {ana.temp_productivity_frames[number_list].iloc[:,1].mean().round(3) * 100}%. \
		#	With {np.sum(ana.temp_productivity_frames[number_list].iloc[:,1] < .5)} days below 50% productivity.  \
		#	It stands that {month} is a {np.where(ana.temp_productivity_frames[number_list].iloc[:,1].mean() > .6 ,productivity_list[0], productivity_list[1] )} \
		#	month when it comes to outdoor construction.')
		#ana.plot_productivity_by_month(i = number_list)
		#st.plotly_chart(ana.plot_productivity_plot)
		
