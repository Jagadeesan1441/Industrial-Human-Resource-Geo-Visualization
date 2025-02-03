import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("structured_classified.csv")

# Clean column names: Remove extra spaces
df.columns = df.columns.str.strip().str.replace("  ", " ")  # Replace double spaces with single space

# Streamlit UI
st.set_page_config(page_title="Workers Population Dashboard", layout="wide")
st.title("📊 Workers Population Dashboard")
st.sidebar.header("Filters")

# Sidebar Filters
state_filter = st.sidebar.selectbox("Select State", sorted(df['STATE'].dropna().unique()))
industry_filter = st.sidebar.selectbox("Select Industry Classification", sorted(df['Industry Classification'].dropna().unique()))

# Filter dataset based on selections
filtered_data = df[(df['STATE'] == state_filter) & (df['Industry Classification'] == industry_filter)]

# Verify if the required columns exist after cleaning
expected_cols = [
    'Main Workers - Rural - Persons', 'Main Workers - Urban - Persons',
    'Marginal Workers - Rural - Persons', 'Marginal Workers - Urban - Persons'
]

for col in expected_cols:
    if col not in df.columns:
        st.error(f"Column '{col}' not found! Check your dataset.")
        st.stop()

# Aggregate worker data
worker_data = {
    'Rural': {
        'Main Workers': filtered_data['Main Workers - Rural - Persons'].sum(),
        'Marginal Workers': filtered_data['Marginal Workers - Rural - Persons'].sum()
    },
    'Urban': {
        'Main Workers': filtered_data['Main Workers - Urban - Persons'].sum(),
        'Marginal Workers': filtered_data['Marginal Workers - Urban - Persons'].sum()
    }
}

# Convert to DataFrame for visualization
worker_df = pd.DataFrame(worker_data).reset_index()
worker_df.columns = ['Area', 'Main Workers', 'Marginal Workers']

# Bar Chart: Main vs. Marginal Workers in Rural & Urban
fig = px.bar(
    worker_df,
    x='Area',
    y=['Main Workers', 'Marginal Workers'],
    title=f"Main and Marginal Workers in {state_filter} - {industry_filter}",
    labels={"value": "Worker Count", "variable": "Worker Type"},
    barmode='group'
)

# Show plot
st.plotly_chart(fig, use_container_width=True)

# Show total counts
st.subheader("📋 Workforce Summary")
st.write(f"**Total Main Workers:** {worker_data['Rural']['Main Workers'] + worker_data['Urban']['Main Workers']}")
st.write(f"**Total Marginal Workers:** {worker_data['Rural']['Marginal Workers'] + worker_data['Urban']['Marginal Workers']}")

# Show filtered data
st.subheader("🔍 Filtered Data")
st.dataframe(filtered_data)
