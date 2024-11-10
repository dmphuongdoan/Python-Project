import pandas as pd

guests_df = pd.read_excel('dataset/guests.xlsx')
hotels_df = pd.read_excel('dataset/hotels.xlsx')
preferences_df = pd.read_excel('dataset/preferences.xlsx')

print(guests_df.head())
print(hotels_df.head())
print(preferences_df.head())