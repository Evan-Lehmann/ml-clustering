import streamlit as st
from multipage import MultiPage
from app_pages import model, dashboard

app = MultiPage()
app.add_page("Model", model.app)
app.add_page("Dashboard", dashboard.app) 

app.run() 