import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import statsmodels.api as sm

st.title("Insights")

# Load the dataset
df = pd.read_csv('datasets/gurgaon_properties_post_feature_selection_v2.csv').drop(columns=['store room','floor_category','balcony'])

# Preprocess the dataset
df['agePossession'] = df['agePossession'].replace({
    'Relatively New': 'new', 'Moderately Old': 'old',
    'New Property': 'new', 'Old Property': 'old', 'Under Construction': 'under construction'
})
df['property_type'] = df['property_type'].replace({'flat': 0, 'house': 1})
df['luxury_category'] = df['luxury_category'].replace({'Low': 0, 'Medium': 1, 'High': 2})

new_df = pd.get_dummies(df, columns=['sector', 'agePossession'], drop_first=True)

# Split data into X and y
X = new_df.drop(columns=['price'])
y = new_df['price']
y_log = np.log1p(y)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Ridge Regression model
ridge = Ridge(alpha=0.0001)
ridge.fit(X_scaled, y_log)

# Coefficient DataFrame
coef_df = pd.DataFrame(ridge.coef_.reshape(1, -1), columns=X.columns).stack().reset_index().drop(columns=['level_0'])
coef_df = coef_df.rename(columns={'level_1': 'feature', 0: 'coef'})

# Sector-wise Price Change
st.subheader('Sector-wise Price Comparison')

sector_list = df['sector'].unique()

sector_1 = st.selectbox('Select First Sector:', sector_list)
sector_2 = st.selectbox('Select Second Sector:', sector_list)

if sector_1 and sector_2:
    sector_1_data = df[df['sector'] == sector_1]['price'].mean()
    sector_2_data = df[df['sector'] == sector_2]['price'].mean()

    percent_change = ((sector_2_data - sector_1_data) / sector_1_data) * 100
    st.markdown(f"<h5> The percent change in average price between {sector_1} and {sector_2} is: {percent_change:.2f}%</h5>", unsafe_allow_html=True)



# Interactive Feature Importance
st.subheader('Interactive Feature Importance')

# Allow user to select the number of features to display
num_features = st.slider('Select number of top features to display:', min_value=5, max_value=20, value=10)


def plot_feature_importance(coef_df, num_features):
    coef_df_sorted = coef_df.sort_values(by='coef', ascending=False).head(num_features)
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='coef', y='feature', data=coef_df_sorted)

    # Annotate the values on the bars
    for i in ax.containers:
        ax.bar_label(i, fmt='%.2f')

    plt.title(f'Top {num_features} Important Features Influencing Price')
    plt.xlabel('Coefficient Value')
    plt.ylabel('Feature')
    st.pyplot(plt)


plot_feature_importance(coef_df, num_features)

# Perform PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)


import plotly.express as px
# Assume 'X_scaled' is already defined and PCA has been applied
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Create a DataFrame for the PCA results
pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])

# If you want to color the points by a specific feature, e.g., property_type
pca_df['property_type'] = df['property_type']  # Assuming 'df' is your original DataFrame

# Create an interactive scatter plot
fig_scatter = px.scatter(pca_df, x='PC1', y='PC2', color='property_type',
                         title='2D PCA Scatter Plot',
                         labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'},
                         template='plotly_white')

# Display the interactive plot in Streamlit
st.plotly_chart(fig_scatter)


# Create a summary of key insights based on regression results
st.subheader('Key Insights from Regression Analysis')

# Extract relevant statistics
positive_coefficients = coef_df[coef_df['coef'] > 0].sort_values(by='coef', ascending=False).head(5)
negative_coefficients = coef_df[coef_df['coef'] < 0].sort_values(by='coef').head(5)

st.write("### Features Increasing Price:")
for index, row in positive_coefficients.iterrows():
    st.write(f"- **{row['feature']}**: Increases price by {row['coef']:.2f}")

st.write("### Features Decreasing Price:")
for index, row in negative_coefficients.iterrows():
    st.write(f"- **{row['feature']}**: Decreases price by {abs(row['coef']):.2f}")


