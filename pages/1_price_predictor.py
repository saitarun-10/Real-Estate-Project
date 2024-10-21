import streamlit as st
import pickle
import bz2  # Updated to use bz2 for decompression
import pandas as pd
import numpy as np

st.title("Price Predictor")

# Load the df.pkl file (assuming it's not compressed)
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

# Load the compressed pipeline.pkl.bz2 file using bz2
with bz2.BZ2File('pipeline.pkl.bz2', 'rb') as file:
    pipeline = pickle.load(file)

st.dataframe(df)

st.header('Enter your inputs')
# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

bathrooms = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    # Form a dataframe
    data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room,
             furnishing_type,
             luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # Display
    st.text(f"The price of the flat is between {round(low, 2)} Cr and {round(high, 2)} Cr")
