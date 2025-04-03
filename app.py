import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Athlete Performance Analysis', page_icon = "🏅")

# Load Data
@st.cache_data
def load_data():
    athletes_1 = pd.read_csv("data/athlete_performance_1.csv")
    athletes_2 = pd.read_csv("data/athlete_performance_2.csv")
    athletes = pd.concat([athletes_1, athletes_2], axis=0)
    noc_regions = pd.read_csv("data/noc_regions.csv")
    return athletes, noc_regions

athletes, noc_regions = load_data()

# Merge Data
athletes = athletes.merge(noc_regions, how='left', on='NOC')

# Title
st.title("🏅 Athlete Performance Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
sport_filter = st.sidebar.multiselect("Select Sports", athletes['Sport'].unique())
country_filter = st.sidebar.multiselect("Select Countries", athletes['region'].dropna().unique())
medal_filter = st.sidebar.multiselect("Select Medal Type", ['Gold', 'Silver', 'Bronze'])

def apply_filters(df):
    if sport_filter:
        df = df[df['Sport'].isin(sport_filter)]
    if country_filter:
        df = df[df['region'].isin(country_filter)]
    if medal_filter:
        df = df[df['Medal'].isin(medal_filter)]
    return df

filtered_data = apply_filters(athletes)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Athletes", len(filtered_data['ID'].unique()))
col2.metric("Total Events", len(filtered_data['Event'].unique()))
col3.metric("Avg. Height", round(filtered_data['Height'].mean(), 1))
col4.metric("Avg. Age", round(filtered_data['Age'].mean(), 1))

# Medals Trend Over Time
st.subheader("🏆 Medals Won Over Time")
medals_over_time = filtered_data.groupby('Year')['Medal'].count().reset_index()
st.line_chart(medals_over_time, x='Year', y='Medal')

# Medal Distribution Plot
st.subheader("🥇 Medal Distribution")
medal_counts = filtered_data['Medal'].value_counts().reset_index()
medal_counts.columns = ['Medal', 'Count']
fig_pie = px.pie(medal_counts, values='Count', names='Medal', title="Medal Distribution")
st.plotly_chart(fig_pie)

# Top Performing Countries
st.subheader("🌎 Top Performing Countries")
medals_by_country = filtered_data.groupby('region')['Medal'].count().nlargest(10).reset_index()
st.bar_chart(medals_by_country, x='region', y='Medal')

# Gender Distribution Across Sports
st.subheader("📊 Gender Distribution Across Sports")
gender_sport = filtered_data.groupby(['Sport', 'Sex']).size().unstack()
st.bar_chart(gender_sport)

# Show Raw Data Option
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_data)
