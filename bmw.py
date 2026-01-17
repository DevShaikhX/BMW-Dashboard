import streamlit as st
from data import df

st.title("BMW Car Data Overview ")
st.write("This dashboard provides an overview of BMW car data.")

st.subheader(f"BMW Data:{df}")