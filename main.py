from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

df= pd.read_excel("airbnb.xlsx")

icon = Image.open("airbnb-logo.png")
airbnb_img=Image.open("airbnb_logo_detail.jpg")
st.set_page_config(page_title= "Airbnb Data Analysis",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",)

t1,t2=st.columns([1,5])
with t1:
    st.image(airbnb_img)
with t2:
    st.title(":red[AIR]BNB _Analysis_")

st.markdown(f""" <style>.stApp {{
                    background:url("https://wallpapercave.com/wp/wp5240523.jpg");
                    background-size: 100%}}

                 </style>""", unsafe_allow_html=True)
selected = option_menu(None, ["Home","Explore"],
                       icons=["house","bar-chart-line"],
                       menu_icon= "menu-button-wide",
                       default_index=0,orientation='horizontal',
                       styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                               "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )
if selected=="Home":
    col1,col2=st.columns([2,1])
    with col1:
        st.markdown("## What is _:red[AIRBNB]_?")
        st.write("**Airbnb, Inc. is an American company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.**")

    with col2:
        st.image("https://media.cntraveller.com/photos/63bd91b73c7bca633cbfe0fb/16:9/w_2580,c_limit/airbnb.jpg")
    with col1:
        st.markdown("## About this _:red[project]_")
        st.write("**In this project we will analyse AirBnb listings based on the data available in MongoDB Atlas. We will extract relevant data from MOngoDB to Pandas DataFrame and clean the data. we will use this data to further visualise and analyse AirBnb Listings based on Ratings, Numbers, Prices, etc.**")
elif selected=="Explore":
    tab1, tab2 = st.tabs(["OVERALL DATA", "FILTERED INSIGHTS"])
    with tab1:
        #property_type
        prop=df.property_type.value_counts().index[:10]
        prop_count=df.property_type.value_counts().values[:10]
        fig=px.bar(df,x=prop,y=prop_count,title="top 10 property types", color=prop)
        st.plotly_chart(fig,use_container_width=True)

        #avg price per property
        avg_price_p_type = df.Price.groupby(df.property_type.values).mean().sort_values(ascending=False)[0:17]
        fig = px.bar(df, x=avg_price_p_type.index, y=avg_price_p_type.values, title="AVG price per property types", color=avg_price_p_type.index)
        st.plotly_chart(fig, use_container_width=True)

        #ROOM TYPES
        room_count=df.Room_type.value_counts()
        fig = px.bar(df, x=room_count.index, y=room_count.values, title="Types of Rooms",
                     color=room_count.index)
        st.plotly_chart(fig, use_container_width=False)

        #avg availability per property
        n=st.selectbox('Select a range',[10,20,30])
        avail_prop=df.Availability_365.groupby(df.property_type.values).mean().sort_values(ascending=True)[(n-10):n]
        fig = px.bar(df, x=avail_prop.index, y=avail_prop.values, title="availability per property type",
                     color=avail_prop.index)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        c1,c2,c3=st.columns([1,1,1])
        with c1:
            country = st.multiselect("Country you're looking for:", sorted(df.Country.unique()),default=df.Country.unique(),
                                   placeholder='Select a country')
        with c2:
            property = st.multiselect("Type of property:", sorted(df['property_type'].unique()),default=sorted(df['property_type'].unique()),
                                        placeholder='Select a property')
        with c3:
            room_type = st.multiselect("Room Type:", sorted(df['Room_type'].unique()),default=sorted(df['Room_type'].unique()),
                                     placeholder='Select a room')
        with c1:
            price=st.slider('select a range',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()),
                      step=500)
        #query = f" Country == @{country} and Room_type == @{room_type} and property_type == @{property} and Price >= @{price[0]} and Price <= @{price[1]}"
        query='Country == @country and Room_type == @room_type and property_type == @property and Price >= @price[0] and Price <= @price[1]'

        #host
        df1 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                     title='Hosts with Highest Listings',
                     x='Listings',
                     y='Host_name',
                     orientation='h',
                     color='Host_name',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        df2 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df2,
                     title='Total Listings in each Room_types',
                     names='Room_type',
                     values='counts',
                     color_discrete_sequence=px.colors.sequential.Rainbow
                     )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig, use_container_width=True)

        #avg price
        df3 = df.query(query).groupby(by='Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=df3,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        #avg Availability
        df4=df.query(query).groupby('Room_type')['Availability_365'].mean().reset_index()

        fig = px.bar(data_frame=df4,
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)
