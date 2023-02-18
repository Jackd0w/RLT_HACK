import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json

st.set_page_config(page_title="ROSELTORG DASHBOARD", page_icon="Icon.jpg", layout="wide")

st.subheader("Test version")
st.title("Interactive Dashboard")


trafic_data = 

selected_class = st.radio("Select Class", trafic_data['class'].unique())
st.write("Selected Class:", selected_class)
st.write("Selected Class Type:", type(selected_class))