import streamlit as st
import matplotlib as plt
import pandas as pd 
import altair as alt
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt

def dataset():
    customers = pd.read_csv("https://raw.githubusercontent.com/Evan-Lehmann/ml-clustering/main/data/Mall_Customers.csv")
    customers = customers.drop(columns=["CustomerID"])
    return customers

def processed_data():
    global scaler, ohe
    ohe, scaler = OneHotEncoder(), StandardScaler()
    pipe = ColumnTransformer([
        ("scale", scaler, ["Age", "Annual Income (k$)", "Spending Score (1-100)"]),
        ("encode", ohe, ["Gender"])
    ], remainder="passthrough")
    processed_customers = pd.DataFrame(pipe.fit_transform(dataset()))
    processed_customers.columns = ["Age", "Annual Income (k$)", "Spending Score (1-100)", "cat_zero", "cat_one"]
    return processed_customers

def two_dim_data():
    global pca
    pca = PCA(n_components=2)
    two_dim_data = pd.DataFrame(pca.fit_transform(processed_data()))
    two_dim_data.columns=["X-axis", "Y-axis"]
    return two_dim_data  

def app():
    global dataset
    st.title('Model')

    def convert_df(df):
        return df.to_csv().encode('utf-8') #allows datasets to be downloaded as CSVs

    #original dataset
    st.subheader("Original Dataset")
    st.dataframe(dataset())
    st.write("Shape:", dataset().shape)

    original_csv = convert_df(dataset())
    st.download_button(
        label="Download data as a CSV",
        data=original_csv,
        file_name='original_cluster_data.csv',
        mime='text/csv'
    )

    #model
    st.subheader("Cluster Data")
    #choose number of clusters
    n_clusters = st.slider("Number of Clusters", min_value=2, max_value=5, value=2)

    #fit model to data  
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(processed_data())
    clusters_pred = kmeans.predict(processed_data())

    cluster_df = dataset().copy()
    cluster_df["Cluster"] = clusters_pred
    st.write("Number of Clusters:", n_clusters)

    processed_two_dim = two_dim_data().copy()
    processed_two_dim["Cluster"] = kmeans.labels_

    colors = ["darkred", "pink", "gold", "darkgreen", "cyan"]

    cluster_chart = alt.Chart(processed_two_dim).mark_circle(size=60).encode(
        x="X-axis",
        y="Y-axis",
        color=alt.Color("Cluster", scale=alt.Scale(range=colors, domain=list(range(n_clusters))))
    ).properties(
        title='Two Dimensional Scatter Plot of Customers',
        width=650,
        height=450
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=16
    ).interactive()
    st.altair_chart(cluster_chart)

    #clustered dataset
    st.subheader("Clustered Dataset")

    st.dataframe(cluster_df)
    st.write("Shape:", cluster_df.shape)

    customers_csv = convert_df(cluster_df)
    st.download_button(
        label="Download data as a CSV",
        data=customers_csv,
        file_name='clustered_customers.csv',
        mime='text/csv'
    )

    #clustered dataset stats
    st.subheader("Cluster Stats & Charts")

    cluster_num_agg = cluster_df.groupby("Cluster").mean()
    cluster_num_agg.columns = [col + " Avg." for col in cluster_num_agg.columns]
    cluster_num_agg = cluster_num_agg.reset_index()
    cluster_num_agg["Count"] = cluster_df.groupby("Cluster")["Cluster"].count().values
    st.dataframe(cluster_num_agg)
    st.write("Shape:", cluster_num_agg.shape)

    cluster_num_agg_csv = convert_df(cluster_df)

    st.download_button(
        label="Download data as a CSV",
        data=cluster_num_agg_csv,
        file_name='clusters_stats.csv',
        mime='text/csv'
    )
    st.write("")

    #grouped bar chart by gender by cluster
    cluster_gender_agg = pd.DataFrame(cluster_df.groupby("Cluster")["Gender"].value_counts())
    cluster_gender_agg = cluster_gender_agg.reset_index(level=0)
    cluster_gender_agg["Count"] = cluster_gender_agg["Gender"]
    cluster_gender_agg = cluster_gender_agg.drop(columns=["Gender"])
    cluster_gender_agg["Gender"] = cluster_gender_agg.index.copy()

    gender_bar_chart = alt.Chart(cluster_gender_agg).mark_bar(opacity=1).encode(
        column = alt.Column('Cluster:N', spacing=10),
        x =alt.X('Gender', axis=None),
        y =alt.Y('Count:Q'),
        color=alt.Color('Gender', scale=alt.Scale(range=['#EA98D2', '#659CCA']))
    ).properties(
        title='Gender Count by Cluster',
        width=100,
        height=300
    ).configure_axisTop(
        labelColor='white',
        titleColor='white'
    ).configure_header(
        titleColor='white',
        labelColor='white',
    ).configure_title(
        fontSize=16,
        anchor='middle'
    ).configure_view(stroke='transparent')

    st.altair_chart(gender_bar_chart)

    #parallel coordinate plot
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=processed_data().columns)
    centroids['Cluster'] = centroids.index

    parallel_coords_chart = alt.Chart(centroids).transform_window(
        index='count()'
        ).transform_fold(
            list(centroids.drop(columns=["Cluster", "cat_zero", "cat_one"]).columns)
        ).mark_line().encode(
            x='key:N',
            y='value:Q',
            detail='index:N',
            color=alt.Color("Cluster", scale=alt.Scale(range=colors, domain=list(range(n_clusters))))
        ).properties(
            title='Parallel Coordinates of Clusters',
            width=650,
            height=550
        ).configure_title(
            fontSize=16
        ).interactive()

    st.altair_chart(parallel_coords_chart)