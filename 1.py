import pandas as pd
import numpy as np
import random

guests_df = pd.read_excel('dataset/guests.xlsx')
hotels_df = pd.read_excel('dataset/hotels.xlsx')
preferences_df = pd.read_excel('dataset/preferences.xlsx')

guests_df.head()
hotels_df.head()
preferences_df.head()

guests_df = guests_df.rename(columns={'Unnamed: 0': 'index', 'guest': 'guest_id', 'discount': 'discount_rate'})
hotels_df = hotels_df.rename(columns={'Unnamed: 0' : 'index', 'hotel': 'hotel_id','rooms' : 'rooms_available' , 'price': 'unit_price'})
preferences_df = preferences_df.rename(columns={'Unnamed: 0': 'index', 'guest': 'guest_id', 'hotel': 'hotel_id', 'priority': 'preference_priority'})


"""
Random Allocation
"""
def random_allocation(guests_df, hotels_df):
    allocation = []
    hotel_rooms = hotels_df.set_index('hotel_id')['rooms_available'].to_dict()
    hotel_prices = hotels_df.set_index('hotel_id')['unit_price'].to_dict()

    all_hotels = list(hotel_rooms.keys())

    for guest_id in guests_df['guest_id']:
       assigned = False
       random.shuffle(all_hotels) 
       for hotel_id in all_hotels: 
          if hotel_rooms.get(hotel_id, 0) > 0: 
             hotel_rooms[hotel_id] -= 1
             discount = guests_df.loc[guests_df['guest_id'] == guest_id, 'discount_rate'].values[0]
             final_price = hotel_prices[hotel_id] * (1 - discount)
             allocation.append({
                'guest_id': guest_id,
                'hotel_id': hotel_id,
                'final_price': final_price,
                'satisfaction_score': None #satisfaction score is irrelevant for random allocation
             })
             assigned = True
             break
    if not assigned: # if no room was assigned
       allocation.append({
          'guest_id': guest_id,
          'hotel_id': None,
          'final_price': None,
          'satisfaction_score': None
       })
    allocation_df = pd.DataFrame(allocation)
    return allocation_df, hotel_rooms 

random_allocation_df, remaining_room_randoms = random_allocation(guests_df, hotels_df)

customers_accommodated_random = random_allocation_df[random_allocation_df['hotel_id'].notna()].shape[0]
rooms_occupied_random = random_allocation_df[random_allocation_df['hotel_id'].notna()].shape[0]
different_hotels_occupied_random = random_allocation_df['hotel_id'].nunique()
total_business_random = random_allocation_df['final_price'].dropna().sum()

results_random = {
   "Customer accommodated": customers_accommodated_random,
   "Rooms Occupied": rooms_occupied_random,
   "Different Hotels Occupied": different_hotels_occupied_random,
   "Total business volume": total_business_random

}



"""
Preference Allocation
"""
def preference_allocation (guests_df, hotels_df, preferences_df):
    allocation = []

    hotel_rooms = hotels_df.set_index('hotel_id')['rooms_available'].to_dict()
    hotel_prices = hotels_df.set_index('hotel_id')['unit_price'].to_dict()

    satisfaction_score = {guest: [] for guest in guests_df['guest_id']}

    for guest_id in guests_df['guest_id']:
        preferences = preferences_df[preferences_df['guest_id']== guest_id].sort_values('preference_priority')
        assigned = False
        for _, row in preferences.iterrows():
            hotel_id = row['hotel_id']
            if hotel_rooms.get(hotel_id, 0) > 0:
                hotel_rooms[hotel_id] -= 1
                discount = guests_df.loc[guests_df['guest_id'] == guest_id,'discount_rate'].values[0]
                final_price = hotel_prices[hotel_id] * (1 - discount)
                satisfaction_score = row['preference_priority']
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': hotel_id,
                    'final_price': final_price,
                    'satisfaction_score': satisfaction_score
                })
                assigned = True
                break
        
        if not assigned:
            allocation.append({
                'guest_id': guest_id,
                'hotel_id': None,
                'final_price': None,
                'satisfaction_score': None
            })
    allocation_df = pd.DataFrame(allocation)
    return allocation_df, hotel_rooms

preference_allocation_df, remaining_rooms = preference_allocation(guests_df, hotels_df, preferences_df)

customers_accommodated_prefer = int(allocation_df[allocation_df['hotel_id'].notna()].shape[0])
rooms_occupied_prefer = int(allocation_df[allocation_df['hotel_id'].notna()]['hotel_id'].count())
different_hotels_occupied_prefer = allocation_df['hotel_id'].nunique()
total_business_prefer = allocation_df['final_price'].dropna().sum()
customer_satisfaction_prefer = allocation_df['satisfaction_score'].mean()


#total_business = allocation_df.groupby('hotel_id')['final_price'].sum()
#customer_satisfaction = allocation_df.groupby('hotel_id')['satisfaction_score'].mean()

results_prefer = {
    "Customer Preference Allocation": preference_allocation,
    "Customers Accommodated Preference-based": customers_accommodated_prefer,
    "Rooms Occupied Preference-based": rooms_occupied_prefer,
    "Different Hotels Occupied Preference-based": different_hotels_occupied_prefer, 
    "Total Business Volume Preference-based": float(total_business_prefer),
    "Average Customer Satisfaction Score Preference-based": float(customer_satisfaction_prefer.mean())
}

#print(results)


"""
Price Allocation
"""
def price_allocation(guests_df, hotels_df, prefernces_df);
    allocation = []
    hotel_rooms = hotels_df.set_index('hotel_id')['rooms_available'].to_dict()
    hotel_prices = hotels_df.set_index('hotel_id')['unit_price'].to_dict()

    sorted_hotels = hotels_df.sort_values('unit_price')['hotel_id'].tolist()
    hotel_rank = {hotel: idx for idx, hotel in enumerate(sorted_hotels)}

    preferences_df = preferences_df.assign(hotel_rank=preferences_df['hotel_id'].map(hotel_rank))
    preferences_df = preferences_df.sort_value(['guest_id', 'hotel_rank', 'preference_priority'])

    for guest_id, group in preferences_df.groupby('guest_id'):
        assigned = False
        for _, row in group.iterrows():
            hotel_id = row['hotel_id']
            if hotel_rooms.get(hotel_id, 0) > 0:
                hotel_rooms[hotel_id] -= 1
                discount = guests_df.loc[guests_df['guest_id'] == guest_id, 'discount_rate'].values[0]
                final_price = hotel_prices[hotel_id] * (1 - discount)
                satisfaction_score = row['preference_priority']
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': hotel_id,
                    'final_price': final_price,
                    'satisfaction_score': satisfaction_score
                })
                assigned = True
                break
            if not assigned: 
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': None, 
                    'final_price': None, 
                    'satisfaction_score': None
                })
    allocation_df = pd.DataFrame(allocation)
    return allocation_df, hotel_rooms

price_allocation_df, remaining_room_price = price_allocation(guests_df, hotels_df, preferences_df)

customers_accommodated_price = price_allocation_df[price_allocation_df['hotel_id'].notna()].shape[0]
rooms_occupied_price = price_allocation_df[price_allocation_df['hotel_id'].notna()].['hotel_id'].count()
different_hotels_occupied_price = price_allocation_df['hotel_id'].nunique()
total_business_price = price_allocation_df['final_price'].dropna().sum()
customer_satisfaction_price = price_allocation_df['satisfaction_score'].mean()

results_price = {
    "Customers Accomodated Price-based" : customers_accommodated_price,
    "Rooms occupied Price-based": rooms_occupied_price,
    "Different Hotels occupied Price-based": different_hotels_occupied_price,
    "Total Business Volume Price-based": float(total_business_price),
    "Average Customer Satisfaction Score Price-based": float(customer_satisfaction_price)
    }


"""
Availability Allocation
"""

def availability_allocation(guests_df, hotels_df, preferences_df):
    allocation = []
    hotel_rooms = hotels_df.set_index('hotel_id')['rooms_available'].to_dict()
    hotel_prices = hotels_df.set_index('hotel_id')['rooms_available'].to_dict()

    sorted_hotels = hotels_df.sort_values('rooms_available', ascending=False)['hotel_id'].tolist()
    hotel_rank = {hotel: idx for idx, hotel in enumerate(sorted_hotels)}

    preferences_df = preferences_df.assign(hotel_rank=preferences_df['hotel_id'].map(hotel_rank))
    preferences_df = preferences_df.sort_values(['guest_id', 'hotel_rank', 'preference_priority'])

    for guest_id, group in preferences_df.groupby('guest_id'):
        assigned = False
        for _, row in group.iterrows():
            hotel_id = row['hotel_id']
            if hotel_rooms.get(hotel_id, 0) > 0:
                hotel_rooms[hotel_id] -= 1
                discount = guests_df.loc[guests_df['guest_id'] == guest_id, 'discount_rate'].values[0]
                final_price = hotel_prices[hotel_id] * (1 - discount)
                satisfaction_score = row['preference_priority']
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': hotel_id,
                    'final_price': final_price,
                    'satisfaction_score': satisfaction_score
                })
                assigned = True
                break
        if not assigned: 
            allocation.append({
                'guest_id': guest_id;
                'hotel_id': None,
                'final_price': None,
                'satisfaction_score': None
            })
    return pd.DataFrame(allocation), hotel_rooms
availability_allocation_df, remaining_rooms_available = availability_allocation(guests_df, hotels_df, preferences_df)

customers_accommodated_available = availability_allocation_df[availability_allocation_df['hotel_id'].notna()].shape[0]
rooms_occupied_available = availability_allocation_df[availability_allocation_df['hotel_id'].notna()].['hotel_id'].count()
different_hotels_occupied_available = availability_allocation_df['hotel_id'].nunique()
total_business_available = availability_allocation_df['final_price'].dropna().sum()
customer_satisfaction_available = availability_allocation_df['satisfaction_score'].mean()

results_availability = {
    "Customers Accomodated Availability-based" : customers_accommodated_available,
    "Rooms occupied Availability-based": rooms_occupied_available,
    "Different Hotels occupied Availability-based": different_hotels_occupied_available,
    "Total Business Volume Availability-based": float(total_business_available),
    "Average Customer Satisfaction Score Availability-based": float(customer_satisfaction_available)
    }
