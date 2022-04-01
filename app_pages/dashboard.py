from re import S
import streamlit as st
import matplotlib as plt
import pandas as pd 
import altair as alt
from app_pages.model import dataset, two_dim_data
import numpy as np

def app():
    st.title('Dashboard')

    num_cols = list(dataset().select_dtypes(include=["int64", "float64"]).columns)
    cat_cols = list(dataset().select_dtypes(include=["object"]).columns)

    #numerical distribution
    select_num_cols = st.selectbox("Select a numerical variable to show its distribution", (num_cols))
    if select_num_cols is not None:
        num_hist = alt.Chart(dataset()).mark_bar().encode(
        alt.X(select_num_cols, bin=True),
        y='count()',
        ).properties(
            title=f'{select_num_cols} Distribution',
            width=650,
            height=450
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=15
        )
        st.altair_chart(num_hist)

    #categorical distribution
    gender_val_counts = dataset()["Gender"].value_counts().reset_index()
    gender_val_counts.columns = ["Gender", "Frequency"]
    gender_distribution = alt.Chart(gender_val_counts).mark_bar(size=75).encode(
        x='Gender',
        y='Frequency',
        color=alt.Color('Gender', scale=alt.Scale(range=['#EA98D2', '#1f77b4']))
    ).properties(
        title='Gender Distribution',
        width=650,
        height=450
    ).configure_axis(
        labelFontSize=15,
        titleFontSize=15
    ).configure_title(
        fontSize=15
    )
    st.altair_chart(gender_distribution)
    
    #scatter plots
    st.write("Select two numerical variables to plot against each other")
    scatter_cols_x_list = num_cols.copy()
    scatter_col_x = st.selectbox("Select a numerical variable for the X-axis:", scatter_cols_x_list)

    scatter_cols_y_list = reversed(scatter_cols_x_list)
    scatter_col_y = st.selectbox("Select a numerical variable for the y-axis:", scatter_cols_y_list)

    if scatter_col_x is not None and scatter_col_y is not None:
        scatter_plot = alt.Chart(dataset()).mark_circle(size=60).encode(
            x=scatter_col_x,
            y=scatter_col_y
        ).properties(
            title=f'{scatter_col_y} by {scatter_col_x}',
            width=650,
            height=450
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=16
        ).interactive()
    
        st.altair_chart(scatter_plot)

    #plot against categorical
    num_col_by_gender = st.selectbox("Select a numerical variable to show its average value by Gender", num_cols)
    if num_col_by_gender is not None:
        temp_gender_df = dataset().groupby("Gender")[num_col_by_gender].mean().reset_index()
        num_col_by_gender_chart = alt.Chart(dataset()).mark_bar(size=75).encode(
            x='Gender',
            y=num_col_by_gender,
            color=alt.Color('Gender', scale=alt.Scale(range=['#EA98D2', '#1f77b4']))
        ).properties(
            title=f'Avg. {num_col_by_gender} by Gender',
            width=650,
            height=450
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=15
        )
        st.altair_chart(num_col_by_gender_chart)
