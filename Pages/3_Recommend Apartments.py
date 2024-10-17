import streamlit as st
import pickle
import pandas as pd

st.title("Recommend Apartments")

# Load the data and similarity matrices
location_df = pickle.load(open('location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('cosine_sim3.pkl', 'rb'))

# Assuming you have a dataset containing apartment details
apartment_data = pd.read_csv('datasets/appartments.csv')  # Adjust this if it's a CSV file


# Function to recommend properties with scores and include links
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Get property details from the apartment_data (including the link)
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    }).merge(apartment_data[['PropertyName', 'Link']], on='PropertyName', how='left')

    return recommendations_df


st.title('Select Location and Radius')
selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in KMs')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    for key, value in result_ser.items():
        st.text(str(key) + " ---> " + str(round(value / 1000)) + ' kms')

st.title('Recommend Apartments')
selected_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))


# if st.button('Recommend'):
#     # Store recommendations in session state
#     recommendation_df = recommend_properties_with_scores(selected_apartment)
#     st.session_state.recommendations = recommendation_df  # Save to session state
#
# if 'recommendations' in st.session_state:
#     # Display the recommendations and radio buttons
#     apartment_options = st.session_state.recommendations['PropertyName'].tolist()
#     apartment_choice = st.radio('Select a recommended apartment', apartment_options)
#
#     # Get the selected apartment's link based on the apartment_choice
#     selected_apartment_link = st.session_state.recommendations.loc[st.session_state.recommendations['PropertyName'] == apartment_choice, 'Link'].values[0]
#
#     # Create a clickable link that opens in a new tab
#     if apartment_choice:
#         st.markdown(f"""
#                     <a href="{selected_apartment_link}" target="_blank">
#                         <button style="background-color:#FF4B4B;color:white;border:none;padding:10px 20px;border-radius:5px;">
#                             Visit {apartment_choice}
#                         </button>
#                     </a>
#                     """, unsafe_allow_html=True)

if st.button('Recommend'):
    # Store recommendations in session state
    recommendation_df = recommend_properties_with_scores(selected_apartment)
    st.session_state.recommendations = recommendation_df  # Save to session state

if 'recommendations' in st.session_state:
    # Display the recommendations and radio buttons with similarity scores
    apartment_options = [f"{row['PropertyName']} (Similarity Score: {row['SimilarityScore']:.2f})" for _, row in st.session_state.recommendations.iterrows()]
    apartment_choice = st.radio('Select a recommended apartment', apartment_options)

    # Get the selected apartment's link based on the apartment_choice (extract the property name)
    property_name = apartment_choice.split(" (")[0]
    selected_apartment_link = st.session_state.recommendations.loc[st.session_state.recommendations['PropertyName'] == property_name, 'Link'].values[0]

    # Create a clickable link that opens in a new tab
    if apartment_choice:
        st.markdown(f"""
                    <a href="{selected_apartment_link}" target="_blank">
                        <button style="background-color:#FF4B4B;color:white;border:none;padding:10px 20px;border-radius:5px;">
                            Visit {property_name}
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

