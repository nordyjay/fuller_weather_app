import numpy as np 
import pandas as pd
from pylab import mpl, plt
import datetime as dt
import plotly.graph_objects as go




class OttawaCombinedProductivity(): 
    def __init__(self, file ): 
        self.data = pd.read_csv('daily_combined_data.csv', index_col = 0)
        self.data = self.data.set_index(pd.DatetimeIndex(self.data.index))
        self.month_list = ['january', 'february', 'march', 'april', 'may', 
                           'june', 'july', 'august', 'september', 'october', 
                           'november', 'december'] 
        
        self.month_dict = {1: 'january',2: 'february',3: 'march',4: 'april',5: 'may',
                           6: 'june', 7: 'july', 8: 'august', 9: 'september',
                           10: 'october', 11: 'november', 12: 'december'}
        self.swap_dict = {'january':1,'february':2,'march':3, 'april': 4,'may': 5,
                           'june': 6,'july': 7,'august': 8,'september' : 9,
                            'october': 9, 'november': 11, 'december': 12}

        self.productivity_curve()
        self.make_monthly_data()
        self.make_productivity_curve()
        self.plot_productivity_by_month()
        
        
    def productivity_curve(self): 
        self.x = np.linspace(-30, 30, 10000)
        self.y = (- .001 *self.x ** 2 + .001 * self.x + 1.) 
        self.polyfit = np.polyfit(self.x, self.y,deg =5)
        self.polyval = np.polyval(self.polyfit, self.x)
        
        return self.polyfit
    
    
    def make_monthly_data(self): 
        self.monthly_data = self.data
        self.monthly_data['productivity'] = self.data['Mean Temp (°C)'].apply(lambda x: np.polyval(self.polyfit, x))
        self.monthly_data = self.data.groupby([self.data.index.month, self.data.index.day]).agg('mean')
        
        return self.monthly_data
    
    def generate_work_capacity_insights(self, i =1): 
        if i in [11, 12, 1, 2, 3, 4]: 
            wind_chill_rules = {
            # wind chill temperatures
            #'normal break required': (monthly_data['extremes'].between(-26, -20)  & monthly_data['Wind Spd (km/h)'].between(0, 8)), 
            '75m work period with 2 breaks / 4hr work block' : (self.monthly_data['extremes'].between(-26, -20) & self.monthly_data['Wind Spd (km/h)'].between(16,24)),
            '55m work period with 3 breaks / 4hr work block' : (self.monthly_data['extremes'].between(-26, -20) & self.monthly_data['Wind Spd (km/h)'].between(24,32)),
            '40m work period with 4 breaks / 4hr work block' : (self.monthly_data['extremes'].between(-26, -20) & self.monthly_data['Wind Spd (km/h)'].round() > 32), 
            }
            self.monthly_data['cool_conditions'] = np.select(wind_chill_rules.values(), wind_chill_rules.keys())
            self.work_capacity_dict = self.monthly_data['cool_conditions'].loc[i,:].value_counts().to_dict()
            return self.work_capacity_dict
            
        else: 
            humidity_rules = {
            '75m work period with 2 breaks / 4hr work block' : (self.monthly_data['extremes'].between(25, 30)) ,
            '55m work period with 3 breaks / 4hr work block' : (self.monthly_data['extremes'].between(30, 35)) ,
            '40m work period with 4 breaks / 4hr work block' : (self.monthly_data['extremes'] > 35)
        }

            self.monthly_data['humid_conditions'] = np.select(humidity_rules.values(), humidity_rules.keys())
            self.work_capacity_dict = self.monthly_data['humid_conditions'].loc[i,:].value_counts().to_dict()
            return self.work_capacity_dict 
    
   
    
    
    
    def make_productivity_curve(self): 
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=self.x, y=self.polyval, fill='tozeroy')) 
        fig_p.update_layout(
            title={
                'text': "Worker productivity vs Temperature",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Worker Productivity",
            yaxis_title="Ambient Temperature",
            legend_title="Legend Title",
            font=dict(
                family="Franklin Gothic",
                size=12,
                color="Black"), 
            height = 350, 
            width = 350)
        
        self.prductivity_figure = fig_p
    
    def plot_productivity_by_month(self, i = 1):
        '''
        Function that generates monthly productivity vs temperature
        '''
        self.tdi = self.month_dict
        self.tdi[i] = self.tdi[i]
        fit_x = self.monthly_data.loc[i, :].index
        fit_y = self.monthly_data['productivity'].loc[i, :]
        y_poly_fit = np.polyfit(fit_x, fit_y, deg = 10)
        x_poly_val = np.polyval(y_poly_fit, fit_x)
         
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.monthly_data.loc[i, :].index,
                                 y = x_poly_val,
                                 #y=self.monthly_data['productivity'].loc[i,:], #.loc[i,:].values, 
                                 fill='tonexty', line_color = 'MediumPurple',))
        fig.update_layout(
            title={
                'text': f"{self.tdi[i]} productivity",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            yaxis_range=[0,1],
            xaxis_title="Days Of the Month",
            yaxis_title="Productivity",
            legend_title="Legend Title",
            font=dict(
                family="Franklin Gothic",
                size=18,
                color="Black"
            ), 
            height = 700, 
            width = 1200,
        )
        
        
        self.plot_productivity_plot = fig
        return self.plot_productivity_plot
    
    
        
    
