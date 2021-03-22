import streamlit as st
import numpy as np
import pandas as pd
import sys
from pathlib import Path
from combined_weather_insights import OttawaCombinedProductivity
import os

np.random.seed(100)
dir = Path('/usr/src/app/')
file = 'daily_combined_data.csv'

cwi = OttawaCombinedProductivity(file=file)


class ConstructionProductivityVisualizer():
    '''
    A class that builds the visualization dashboard for construction worker productivity vs temperature
    '''

    def __init__(self):
        self.cwi = cwi
        st.set_page_config(layout="wide")
        st.image('app/fuller_logo.jpg', width=200)
        st.title('Climate Factors on Construction Worker Productivity')

        st.subheader('Thomas Fuller Construction')
        # self.productivity_list = ['productive', 'less productive']
        self.nrc_paper_url = 'https://publications-cnrc.canada.ca/eng/view/ft/?id=52dc96d5-4ba0-40e6-98d2-8d388cba30cd'
        self.month_selector()
        self.side_bar_information()

    # self.derive_monthly_work_capacity_insight()

    def month_selector(self):
        '''
        Method that generates a month selector.
        '''
        self.month = st.select_slider('Select the month for productivity you wish to analyze',
                                      options=list(self.cwi.month_list))
        fig, x_poly_mean = self.cwi.plot_productivity_by_month(i=self.cwi.swap_dict[self.month])

        st.markdown(
            f'For the month of {self.month.capitalize()} looking at the typical 44 hour work week only {44 * x_poly_mean} \
                    project specific working hours in it.')
        if self.month in cwi.month_list[0:4]:
            st.markdown('This may be attributed to taking breaks due to extreme cold and windchill, removing snow, covering worksites \
            to prevent snow accumulation, or setting up infrastructure to work outside.')
        elif self.month in cwi.month_list[10:11]:
            st.markdown('This may be attributed to taking breaks due to extreme cold and windchill, removing snow, covering worksites \
                        to prevent snow accumulation, or setting up infrastructure to work outside.')
        elif self.month in cwi.month_list[5:9]:
            st.markdown(f"This may be attributed to extreme humidity and precipitation preventing certain trades \
			to complete work ")
        else:
            st.markdown(f"This may be attributed to extreme humidity and precipitation preventing certain trades \
            			to complete work.")

        self.derive_monthly_work_capacity_insight()

        st.plotly_chart(fig)

    def derive_monthly_work_capacity_insight(self):
        worker_rules = {0: 8,
                        75: 7.5,
                        55: 7.3,
                        40: 6.6}
        if st.button(f'Derive Worker Capacities for {self.month.capitalize()}'):
            st.markdown('Based on 4 hour work period working outdoors a worker should expect to have:')
            self.sort_dict = (self.cwi.generate_work_capacity_insights(i=self.cwi.swap_dict[self.month]))
            # self.sort_dict['0'] =
            for key, value in self.sort_dict.items():
                if key == '0':
                    st.markdown(
                        f'* {value} days working af full capacity. (A typical 8 hour workday will have  {worker_rules[int(key[0:2])]} full capacity hours in it.)')
                else:
                    st.markdown(
                        f'* {value} days working at {key}. (A typical 8 hour workday will have  {worker_rules[int(key[0:2])]} full capacity hours in it.)')

    def side_bar_information(self):
        st.sidebar.title('More About This Tool')
        self.choice = st.sidebar.selectbox('Learn more about the methodology used for this tool',
                                           ('Data', 'Research', 'Method'))
        if self.choice == "Data":
            st.sidebar.markdown(f'The data was collected from Government of Canada webside site from the Ottawa airport location\
                    and includes a forecasting bounday outlined in the map below')
            df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [45.38, -75.72], columns=['lat', 'lon'])
            st.sidebar.map(df)
        if self.choice == 'Method':
            st.sidebar.markdown(f'The method we used to assemble this tool was by aggregating hourly weather data '
                                f'from the  Ottawa airport weather station from the last ten years.  Building on top '
                                f'of the NRC paper we build functions that are able to calculate outdoor worker '
                                f'productivity as it relates temperature, windchill, humidity, precipitation, '
                                f'and accumulated precipitation.  The original function is given below.')
            st.sidebar.plotly_chart(self.cwi.prductivity_figure)
        elif self.choice == 'Research':
            st.sidebar.markdown(f"Findings used for this analysis was based of the Natioanl Research Council of Canada \
            pulication 'Productivity in Construction'  which can be found here: {self.nrc_paper_url}. \
            It serves as a great guide of overall construction productivity and has a Canadian perspective on the matter.\
            The worker capacities were derived Fuller's proprietary workplace research. ")


if __name__ == "__main__":
    # execute only if run as a script
    ConstructionProductivityVisualizer()
