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
