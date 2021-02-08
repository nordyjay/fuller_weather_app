import numpy as np
import pandas as pd
import datetime as dt
import plotly.graph_objects as go


class OttawaWeatherAnalytics:
    def __init__(self, data, smoothing_amount=1):
        self.data = data
        self.month_list = [
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ]
        self.month_dict = {
            0: "january",
            1: "february",
            2: "march",
            3: "april",
            4: "may",
            5: "june",
            6: "july",
            7: "august",
            8: "september",
            9: "october",
            10: "november",
            11: "december",
        }
        self.smoothing_amount = smoothing_amount
        self.month_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.monthly_productivity_df = pd.DataFrame()
        self.daily_master_drop_columns = []
        self.temperature_bins = [-40, -30, -25, -20, -10, 25, 30, 35, 40]
        self.temperature_labels = [1, 2, 3, 4, 5, 6, 7, 8]
        self.productivity_labels = [0.25, 0.4, 0.56, 0.8, 1, 0.37, 0.35, 0.2]
        self.month_dictionary = dict(zip(self.month_number, self.month_list))
        self.temp_productivity_frames = []
        self.productivity_curve()
        self.daily_data = self.data.resample("24H")
        self.prepare_daily_temp_stats()
        self.prepare_daily_wind_chill_stats()
        self.prepare_daily_humidity_stats()
        self.daily_master_stats()
        self.prepare_monthly_master_stats()
        self.make_productivity_curve()
        self.make_monthly_productivity_plot()
        self.plot_productivity_by_month()

    def productivity_curve(self):
        self.x = np.linspace(-30, 30, 10000)
        self.y = -0.001 * self.x ** 2 + 0.001 * self.x + 1.0
        self.polyfit = np.polyfit(self.x, self.y, deg=5)
        self.polyval = np.polyval(self.polyfit, self.x)

        return self.polyfit

    def prepare_daily_temp_stats(self):
        self.daily_temp_stats = self.daily_data.agg(
            {"Temp (°C)": ["mean", "max", "min", "sem"]}
        )
        self.daily_temp_stats = self.daily_temp_stats.droplevel(0, axis=1)
        self.daily_temp_stats = self.daily_temp_stats.rename(
            columns={
                "mean": "temp_mean",
                "max": "temp_max",
                "min": "temp_min",
                "sem": "temp_standard_error",
            }
        )

        return self.daily_temp_stats

    def prepare_daily_wind_chill_stats(self):
        self.daily_wind_chill_stats = self.daily_data.agg(
            {"Wind Chill": ["mean", "min", "sem"]}
        )
        self.daily_wind_chill_stats = self.daily_wind_chill_stats.droplevel(0, axis=1)
        self.daily_wind_chill_stats = self.daily_wind_chill_stats.rename(
            columns={
                "mean": "wind_chill_mean",
                "min": "wind_chill_max",
                "sem": "wind_chill_standard_error",
            }
        )

        return self.daily_wind_chill_stats

    def prepare_daily_humidity_stats(self):
        self.daily_humidity_stats = self.daily_data.agg(
            {"Hmdx": ["mean", "max", "sem"]}
        )
        self.daily_humidity_stats = self.daily_humidity_stats.droplevel(0, axis=1)
        self.daily_humidity_stats = self.daily_humidity_stats.rename(
            columns={
                "mean": "humidity_mean",
                "max": "humidity_max",
                "sem": "humidity_standard_error",
            }
        )

        return self.daily_humidity_stats

    def daily_master_stats(self):
        self.daily_master_stats = self.daily_temp_stats.join(
            self.daily_wind_chill_stats, how="left"
        ).join(self.daily_humidity_stats, how="left")
        self.daily_master_stats["extremes"] = (
            self.daily_master_stats["wind_chill_max"]
            + self.daily_master_stats["humidity_max"]
        )
        self.daily_master_stats["extremes_smoothing"] = (
            self.daily_master_stats["extremes"]
            .ewm(halflife=self.smoothing_amount)
            .mean()
        )
        self.daily_master_stats["cutting"] = pd.to_numeric(
            pd.cut(
                self.daily_master_stats["extremes_smoothing"],
                bins=self.temperature_bins,
                labels=self.productivity_labels,
            )
        )
        self.productivity_value_counts = pd.DataFrame(
            self.daily_master_stats["cutting"].value_counts()
            / len(self.daily_master_stats.index.year)
        )

        return self.daily_master_stats, self.productivity_value_counts

    def prepare_monthly_master_stats(self):
        self.master_monthly_stats = (
            self.daily_master_stats[["extremes"]]
            .groupby(
                [self.daily_master_stats.index.month, self.daily_master_stats.index.day]
            )
            .agg("mean")
        )
        self.master_monthly_stats = self.master_monthly_stats.unstack(
            level=0
        ).droplevel(1, axis=1)
        self.master_monthly_stats.columns = self.month_list
        for m in self.master_monthly_stats:
            self.monthly_productivity_df[m] = self.master_monthly_stats[m].apply(
                lambda x: np.polyval(self.polyfit, x)
            )
        for m in self.month_list:
            df = pd.concat(
                [
                    self.master_monthly_stats[[m]],
                    self.monthly_productivity_df.ewm(halflife=10).mean()[[m]],
                ],
                axis=1,
            )
            df.columns = [f"{m}_temp", f"{m}_productivity"]
            self.temp_productivity_frames.append(df)

        return (
            self.master_monthly_stats,
            self.monthly_productivity_df,
            self.temp_productivity_frames,
        )

    def make_productivity_curve(self):
        self.fig1 = go.Figure()
        self.fig1.add_trace(go.Scatter(x=self.x, y=self.polyval, fill="tozeroy"))
        self.fig1.update_layout(
            title={
                "text": "Worker productivity vs Temperature",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            height = 400,
            width = 400,
            xaxis_title="Worker Productivity",
            yaxis_title="Ambient Temperature",
            legend_title="Legend Title",
            font=dict(family="Franklin Gothic", size=18, color="Black"),
        )

        self.prductivity_figure = self.fig1

    def make_monthly_productivity_plot(self):
        self.fig2 = go.Figure()
        self.fig2.add_trace(
            go.Scatter(
                x=self.month_list, y=self.monthly_productivity_df.mean(), fill="tozeroy"
            )
        )
        self.fig2.update_layout(
            title={
                "text": "Worker productivity vs Temperature",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            xaxis_title="Worker Productivity",
            yaxis_title="Ambient Temperature",
            legend_title="Legend Title",
            font=dict(family="Franklin Gothic", size=18, color="Black"),
        )

        self.monthly_productivity_plot = self.fig2
        return self.monthly_productivity_plot

    def plot_productivity_by_month(self, i=1):
        self.tdi = list(self.month_dict.items())
        self.tdi[i] = list(self.tdi[i])
        self.fig3 = go.Figure()
        self.fig3.add_trace(
            go.Scatter(
                x=self.temp_productivity_frames[self.tdi[i][0]].index,
                y=self.temp_productivity_frames[self.tdi[i][0]].iloc[:, 1],
                fill="tonexty",
                line_color="hotpink",
            )
        )
        self.fig3.update_layout(
            title={
                "text": f"{self.tdi[i][1]} productivity",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            yaxis_range=[0, 1],
            xaxis_title="Day Of the Month",
            yaxis_title="Productivity",
            legend_title="Legend Title",
            font=dict(family="Franklin Gothic", size=18, color="Black"),
        )

        self.plot_productivity_plot = self.fig3
        return self.plot_productivity_plot
