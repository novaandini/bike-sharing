import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def sum_orders_df():
    day_df = pd.read_csv('dashboard/day_data.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    days_orders_df = day_df.resample(rule='Q', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    days_orders_df.index = days_orders_df.index.to_period('Q').strftime('Q%q %Y')
    days_orders_df = days_orders_df.reset_index()
    days_orders_df.rename(columns={
        "instant": "Banyak Data Transaksi",
        "cnt": "Banyak Sepeda"
    }, inplace=True)

    st.subheader("Total sepeda yang disewakan per kuartal")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        days_orders_df["dteday"],
        days_orders_df["Banyak Sepeda"],
        marker='o', 
        linewidth=2,
        color="#000000"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)

def sum_orders_by_weathersit():
    hour_df = pd.read_csv('dashboard/hour_data.csv')
    byweathersit_df = hour_df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "customer"
    }, inplace=True)

    byweathersit_df["weathersit"] = byweathersit_df["weathersit"].replace({
        1: "Cerah",
        2: "Berkabut",
        3: "Hujan",
        4: "Badai"
    })

    st.subheader("Total sepeda yang disewakan sesuai cuaca")
    weathersit = byweathersit_df["weathersit"]
    
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="customer", 
        x="weathersit",
        data=byweathersit_df.sort_values(by="customer", ascending=False),
        color="#000000",
        ax=ax
    )
    ax.set_title("Number of Customer by Weathersit", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    for i, count in enumerate(byweathersit_df["customer"]):
        plt.text(weathersit[i], count + 10, str(count), ha='center', fontsize=25)

    st.pyplot(fig)


with st.sidebar:
    selectbox = st.selectbox(
        label="Select Data",
        options=('Tren pengguna dalam kuartal', 'Pengaruh cuaca terhadap pelanggan')
    )

if (selectbox == "Tren pengguna dalam kuartal"):
    st.header('Tren pengguna layanan Bike Sharing :sparkles:')

    with st.container():
        sum_orders_df()
elif (selectbox == "Pengaruh cuaca terhadap pelanggan"):
    st.header('Pengaruh cuaca terhadap layanan Bike Sharing :sparkles:')

    with st.container():
        sum_orders_by_weathersit()
else:
    st.error('This is an error', icon="🚨")


