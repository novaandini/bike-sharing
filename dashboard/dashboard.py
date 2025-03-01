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

def getDataByWeather(weatherSelection):
    st.subheader(f"Tren pengguna layanan Bike Sharing pada cuaca {weatherSelection}")
    weather_dict = {
        "Cerah": 1,
        "Berkabut": 2,
        "Hujan": 3,
        "Badai": 4
    }

    weatherSelection_num = weather_dict.get(weatherSelection, 0)

    hour_df = pd.read_csv('dashboard/hour_data.csv')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    df_filtered = hour_df[hour_df["weathersit"] == weatherSelection_num]

    if not df_filtered.empty:
    # Membuat line chart dengan Seaborn
        fig, ax = plt.subplots(figsize=(8, 5))

        hour_df["month_year"] = hour_df["dteday"].dt.to_period("M")

        df_grouped = hour_df[hour_df["weathersit"]==weatherSelection_num].groupby(["month_year", "weathersit"])["cnt"].sum().reset_index()

        # Konversi period ke string agar bisa dipakai sebagai label di grafik
        df_grouped["month_year"] = df_grouped["month_year"].astype(str)

        # Plot line chart dengan Seaborn
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_grouped, x="month_year", y="cnt", marker="o", ax=ax, color="blue")

        
        ax.set_title(f"Jumlah Customer Per Bulan Pada Cuaca {weatherSelection}")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Customer")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        
        # Menampilkan grafik di Streamlit
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk cuaca yang dipilih.")


with st.sidebar:
    selectbox = st.selectbox(
        label="Select Data",
        options=('Tren pengguna dalam kuartal', 'Pengaruh cuaca terhadap pelanggan')
    )

    if (selectbox == "Pengaruh cuaca terhadap pelanggan"):
        weatherSelection = st.selectbox(
            label="Pilih Cuaca",
            options=('Seluruh Data', 'Cerah', 'Berkabut', 'Hujan', 'Badai')
        )


if (selectbox == "Tren pengguna dalam kuartal"):
    st.header('Tren pengguna layanan Bike Sharing :sparkles:')

    with st.container():
        sum_orders_df()
elif (selectbox == "Pengaruh cuaca terhadap pelanggan"):
    st.header('Pengaruh cuaca terhadap layanan Bike Sharing :sparkles:')\

    with st.container():
        if (weatherSelection == 'Cerah'):
            getDataByWeather('Cerah')
        elif (weatherSelection == 'Berkabut'):
            getDataByWeather('Berkabut')
        elif (weatherSelection == 'Badai'):
            getDataByWeather('Badai')
        elif (weatherSelection == 'Hujan'):
            getDataByWeather('Hujan')
        elif (weatherSelection == 'Seluruh Data'):
            sum_orders_by_weathersit()
        else:
            st.error('This is an error', icon="🚨")
else:
    st.error('This is an error', icon="🚨")



