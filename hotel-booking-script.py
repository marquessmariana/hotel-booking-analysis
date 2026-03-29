# PROJECT: Hotel Booking Analysis
# OBJECTIVE: Analyze booking patterns, revenue and cancellations
# AUTHOR: Mariana Marques
# DATE: March 2026


# ============================================
# 1. LIBRARY IMPORTS
# ============================================

import pandas as pd


# ============================================
# 2. DATA LOADING
# ============================================

df1 = pd.read_csv(r'C:path\hotel_bookings_2015.csv')
df2 = pd.read_csv(r'C:path\hotel_bookings_2016.csv')
df3 = pd.read_csv(r'C:path\hotel_bookings_2017.csv')

df = pd.concat([df1, df2, df3], ignore_index=True)
del df1, df2, df3


# ============================================
# 3. INITIAL DATA EXPLORATION
# ============================================

print(df.shape)   
print(df.head())  

print("\nData type:")
print(df.dtypes)


# ============================================
# 4. DATA CLEANING & PROCESSING
# ============================================

missing_percent = (df.isnull().sum() / len(df)) * 100
print("\n% Missing value per column::")
print(missing_percent.round(2)) # check % vazios

numerical_cols = (df.select_dtypes(include=['number']) < 0).sum()

condition = df['adr'] >= 0
df = df[condition]

print("Number of negative values in adr:", (df['adr'] < 0).sum()) #excluir adr negativo


total_duplicates = df.duplicated().sum()
percentage_duplicates = (total_duplicates / len(df)) * 100

print(f"Total duplicates: {total_duplicates}")
print(f"Percentage of duplicates: {percentage_duplicates:.2f}%")

duplicatas = df[df.duplicated(keep=False)]

result = duplicatas[['distribution_channel']].value_counts()
percent = (result / len(duplicatas) * 100).round(2)

print(pd.concat([result, percent], axis=1, keys=['count', '%'])) #check duplicatas

#filling columns
df = df.drop(columns=['company'])
df['children'] = df['children'].fillna(0)
df['country']  = df['country'].fillna('Unknown')
df['agent']    = df['agent'].fillna(0)

print("Missing value after cleaning:")
print(df.isnull().sum())

print("\nDataFrame shape after cleaning:", df.shape)

#df.to_excel(r'C:path\hotel_bookings_clean.xlsx', index=False)


# ============================================
# 5. FEATURE ENGINEERING
# ============================================

#completed arrival date
df['arrival_full_date'] = pd.to_datetime(
    df['arrival_date_year'].astype(str) + '-' +
    df['arrival_date_month'] + '-' +
    df['arrival_date_day_of_month'].astype(str)) 

#format date
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date']) 

df['month_year'] = df['arrival_full_date'].dt.strftime('%b%Y') #month year jan2015
df['Week_day'] = df['arrival_full_date'].dt.day_name() # week day

#cancellation notice
df['days_until_status_change'] = (df['arrival_full_date'] - df['reservation_status_date']).dt.days
bins = [float('-inf'), 7, 15, 30, 90, 180, 365, float('inf')]
labels = ['1 week', '15 days', '1 month', '3 months', '6 months', '1 year', 'more than 1 year']
df['cancellation_notice'] = pd.cut(df['days_until_status_change'], bins=bins, labels=labels) 

#advance_booking
bins = [float('-inf'), 30, 90, 180, 270, 365, float('inf')]
labels = ['1 month', '3 months', '6 months','9 months', '1 year', 'more than 1 year']
df['advance_booking'] = pd.cut(df['lead_time'], bins=bins, labels=labels)

#month_period
bins = [0, 10, 20, 31]
labels = ['beginning', 'middle', 'end']
df['month_period'] = pd.cut(df['arrival_date_day_of_month'], bins=bins, labels=labels)

#total_nights
df['total_nights'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']


#room_classify
room_map = {
    'A': 'Standard', 'B': 'Standard',
    'D': 'Superior', 'E': 'Superior', 'L': 'Superior',
    'C': 'Deluxe', 'F': 'Deluxe',
    'G': 'Premium', 'H': 'Premium',
    'P': 'Special'}

df['room_type'] = df['reserved_room_type'].map(room_map).fillna('Other')


#meal_classify 
meal_map = {
    'SC': 'Room Only',
    'BB': 'Breakfast',
    'HB': 'Half Board',
    'FB': 'Full Board',
    'Undefined': 'Undefined'}

df['meal_type'] = df['meal'].map(meal_map)


#country_rename 91% covered
country_map = {
    'PRT': 'Portugal',
    'GBR': 'United Kingdom',
    'FRA': 'France',
    'ESP': 'Spain',
    'DEU': 'Germany',
    'ITA': 'Italy',
    'IRL': 'Ireland',
    'BEL': 'Belgium',
    'BRA': 'Brazil',
    'NLD': 'Netherlands',
    'USA': 'United States',
    'CHE': 'Switzerland',
    'CN': 'China',
    'AUT': 'Austria',
    'SWE': 'Sweden'}

df['country_name'] = df['country'].map(country_map).fillna('Others')


#market_segment classify
market_segment_map = {
    'Online TA': 'Online TA',
    'Offline TA/TO': 'Offline TA/TO',
    'Groups': 'Groups',
    'Direct': 'Direct booking',
    'Corporate': 'Business',
    'Complementary': 'Courtesy',
    'Aviation': 'Aviation Crew',
    'Undefined': 'Undefined'}

df['market_segment_name'] = df['market_segment'].map(market_segment_map)

#distribuition channel classify
distribution_channel_map = {
    'TA/TO': 'TA/TO',
    'Direct': 'Direct booking',
    'Corporate': 'Business',
    'GDS': 'Global Agency',
    'Undefined': 'Undefined'}

df['distribution_channel_name'] = df['distribution_channel'].map(distribution_channel_map)

#customer_type classify
customer_type_map = {
    'Transient': 'Individual guest',
    'Transient-Party': 'Group event',
    'Contract': 'Business Contract',
    'Group': 'Group'}

df['customer_type_name'] = df['customer_type'].map(customer_type_map)

#df_final
cols = {
    'hotel': 'Hotel',
    'is_canceled': 'Canceled',
    'arrival_full_date': 'Arrival_Full_Date',
    'month_year': 'Month_Year',
    'Week_day': 'Weekday',
    'month_period': 'Month_Period',
    'adults': 'Adults',
    'children': 'Children',
    'babies': 'Babies',
    'country': 'Country_ISO',
    'country_name': 'Country',
    'customer_type_name': 'Customer_Type',
    'market_segment_name': 'Market_Segment',
    'distribution_channel_name': 'Distribution_Channel',
    'is_repeated_guest': 'Repeated_Guest',
    'previous_cancellations': 'Previous_Cancellations',
    'previous_bookings_not_canceled': 'Previous_Not_Canceled',
    'lead_time': 'Lead_Time',
    'advance_booking': 'Advance_Booking',
    'deposit_type': 'Deposit_Type',
    'days_in_waiting_list': 'Days_In_Waiting_List',
    'meal_type': 'Meal_Type',
    'room_type': 'Room_Type',
    'total_nights': 'Total_Nights',
    'adr': 'ADR',
    'total_of_special_requests': 'Special_Requests',
    'cancellation_notice': 'Cancellation_Notice',
    'days_until_status_change': 'Days_Until_Status_Change',
    'reservation_status': 'Reservation_Status',
    'reservation_status_date': 'Reservation_Status_Date'}

df_analysis = df[cols.keys()].rename(columns=cols)
print(df_analysis.columns.tolist())

#export
df_analysis.to_excel(r'C:path\hotel_booking_analysis.xlsx', index=False)
print("File exported successfully!")




