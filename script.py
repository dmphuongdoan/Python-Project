import random
import pandas as pd

guests_df = pd.read_excel('dataset/guests.xlsx')
hotels_df = pd.read_excel('dataset/hotels.xlsx')
preferences_df = pd.read_excel('dataset/preferences.xlsx')

#print(guests_df.head())
#print(hotels_df.head())
#print(preferences_df.head())

# Random Allocation: Customers are randomly distributed to the rooms.
# Customer preferences: Customers are allocated to the hotel based on their preference.
# Price Allocation: Hotels are sorted by price and customers are assigned rooms in order.
# Availability Allocation: Hotels are sorted by the availability and customers are assigned rooms in order.

hotels = hotels_df[['hotel', 'rooms', 'price']].set_index('hotel')
guests = guests_df[['guest', 'discount']].set_index('guest')
preferences = preferences_df[['guest','hotel','priority']].set_index(['guest','priority'])

"""
Random Allocation.
"""
def random_allocation(guests, hotels):
    allocated_customers = []
    hotel_occupied = {hotel: 0 for hotel in hotels.index}
    hotel_revenue = {hotel: 0 for hotel in hotels.index}
    customer_satisfaction = {guest: 0 for guest in guests.index}
    all_guests = guests.index.tolist()
    random.shuffle(all_guests)
    for guest in all_guests:
        if not any(hotel_occupied[hotel] < hotels.loc[hotel, 'rooms'] for hotel in hotels.index): 
            break

        assigned_hotel = random.choice([hotel for hotel in hotels.index if hotel_occupied[hotel] < hotels.loc[hotel, 'rooms']])
        hotel_occupied[assigned_hotel] += 1
        hotel_revenue[assigned_hotel] += hotels.loc[assigned_hotel, 'price']
        allocated_customers.append((guest, assigned_hotel))

        # The satisfaction of customers based on proximity to preferences
        preference_rank = preferences.loc[guest]
        if assigned_hotel in preference_rank['hotel'].values:
            satisfaction_index = preference_rank[preference_rank['hotel'] == assigned_hotel].index[0] + 1
            customer_satisfaction[guest] = satisfaction_index
    
    total_customers = int(len(allocated_customers))
    total_rooms_occupied = int(sum(hotel_occupied.values()))
    total_revenue = int(sum(hotel_revenue.values()))
    total_hotels_occupied = int(len([hotel for hotel, rooms in hotel_occupied.items() if rooms > 0]))
    average_satisfaction = float(sum(customer_satisfaction.values()) / total_customers if total_customers else 0)
    return {
        "Strategy": "Random Allocation",
        "total_customers": total_customers,
        "total_rooms_occupied": total_rooms_occupied,
        "total_revenue": total_revenue,
        "total_hotels_occupied": total_hotels_occupied,
        "average_satisfaction": average_satisfaction
    }

"""
Customer Preferences Allocation 
"""
def customer_preferences_allocation(hotels, guests, preferences):
    allocated_customers = []
    hotel_occupied = {hotel: 0 for hotel in hotels.index}
    hotel_revenue = {hotel: 0 for hotel in hotels.index}
    customer_satisfaction = {guest: 0 for guest in guests.index}

    for guest in guests.index:
        preference_rank = preferences.loc[guest]
        assigned_hotel = preference_rank.iloc[0]['hotel']

        if hotel_occupied[assigned_hotel] < hotels.loc[assigned_hotel, 'rooms']:
            hotel_occupied[assigned_hotel] += 1 
            hotel_revenue[assigned_hotel] += hotels.loc[assigned_hotel, 'price']*(1 - guests.loc[guest, 'discount'])
            allocated_customers.append((guest, assigned_hotel))

            # The satisfaction of customers based on proximity to preferences
            satisfaction_index = preference_rank[preference_rank['hotel'] == assigned_hotel].index[0] + 1
            customer_satisfaction[guest] = satisfaction_index
    
    total_customers = int(len(allocated_customers))
    total_rooms_occupied = int(sum(hotel_occupied.values()))
    total_revenue = int(sum(hotel_revenue.values()))
    total_hotels_occupied = int(len([hotel for hotel, rooms in hotel_occupied.items() if rooms > 0]))
    avg_satisfaction = float(sum(customer_satisfaction.values()) / total_customers if total_customers else 0)

    return {
        "strategy": "Customer Preferences Allocation",
        "total_customers": total_customers,
        "total_rooms_occupied": total_rooms_occupied,
        "total_revenue": total_revenue,
        "total_hotels_occupied": total_hotels_occupied,
        "avg_satisfaction": avg_satisfaction
    }

result = customer_preferences_allocation(hotels, guests, preferences)
print(result)