import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class WeatherAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, skipinitialspace=True)
        self.df['date'] = pd.to_datetime(self.df['date'])
        
    def analyze_temperature(self):
        # Calculate basic temperature statistics
        avg_temp = self.df['temperature'].mean()
        max_temp = self.df['temperature'].max()
        min_temp = self.df['temperature'].min()
        
        print(f"Average temperature: {avg_temp:.1f}°C")
        print(f"Maximum temperature: {max_temp:.1f}°C")
        print(f"Minimum temperature: {min_temp:.1f}°C")
        
    def plot_monthly_averages(self):
        # Calculate monthly averages
        monthly_avg = self.df.groupby(self.df['date'].dt.month).agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'precipitation': 'mean'
        })
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        # Plot temperature
        monthly_avg['temperature'].plot(kind='bar', ax=ax1, color='red')
        ax1.set_title('Average Monthly Temperature')
        ax1.set_ylabel('Temperature (°C)')
        
        # Plot humidity
        monthly_avg['humidity'].plot(kind='bar', ax=ax2, color='blue')
        ax2.set_title('Average Monthly Humidity')
        ax2.set_ylabel('Humidity (%)')
        
        # Plot precipitation
        monthly_avg['precipitation'].plot(kind='bar', ax=ax3, color='green')
        ax3.set_title('Average Monthly Precipitation')
        ax3.set_ylabel('Precipitation (mm)')
        
        plt.tight_layout()
        plt.show()
        
    def find_extreme_weather_days(self):
        # Find days with extreme weather conditions
        hottest_day = self.df.loc[self.df['temperature'].idxmax()]
        coldest_day = self.df.loc[self.df['temperature'].idxmin()]
        wettest_day = self.df.loc[self.df['precipitation'].idxmax()]
        
        print("\nExtreme Weather Days:")
        print(f"Hottest day: {hottest_day['date'].strftime('%Y-%m-%d')} ({hottest_day['temperature']:.1f}°C)")
        print(f"Coldest day: {coldest_day['date'].strftime('%Y-%m-%d')} ({coldest_day['temperature']:.1f}°C)")
        print(f"Wettest day: {wettest_day['date'].strftime('%Y-%m-%d')} ({wettest_day['precipitation']:.1f}mm)")

def main():
    analyzer = WeatherAnalyzer('weather_2024.csv')
    
    print("Weather Data Analysis for 2024")
    print("=" * 30)
    
    analyzer.analyze_temperature()
    analyzer.find_extreme_weather_days()
    analyzer.plot_monthly_averages()

if __name__ == "__main__":
    main()