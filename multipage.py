import streamlit as st

class MultiPage:
    def __init__(self):
        self.apps = []
    def add_page(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
    def run(self):
        app = st.sidebar.selectbox(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])
        app['function']()