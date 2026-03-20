import streamlit as st  
import datetime  

# Slide 14  
"Hello **class**"  

# Slide 18  
"""The elements **appear in the order of their definition**, and to **apply changes**, first **save the file**, then open the browser, and finally **refresh** (top right corner)."""  

# Slide 20  
st.text("My first app")  
st.write()  

st.markdown("My *first* **app** in :red[Streamlit]!!")  
st.markdown("""> This is a blockquote with a [link](http://google.com).""")  
st.markdown("""  
                |                |Column 1                      |Column 2           |  
                |----------------|------------------------------|-------------------|  
                |Python          |Programming language          |:blush:            |  
                |Streamlit       |Python framework              |:blush:            |  
                |UNIE            |Place to learn                |:blush:  :smile:   |  
            """)  

st.write()  

st.title("This is a title")  
st.markdown("# This is a title")  
st.write()  
st.header("This is a header")  
st.markdown("## This is a header")  
st.write()  
st.subheader("This is a subheader")  
st.markdown("### This is a subheader")  

st.write()  
st.latex("y=x^2")  

st.write()  
st.caption("This is a note")  

st.write()  
st.code("""  
        def cosine_function(cos_x):  
            "description of the function"  
            sin_x = cos_x - 180  
            return sin_x  
        """, language="python")  

# Slide 21 - Interactivity: Inputs  
st.subheader("Interactivity - Input")  

# Show inputs without storing them, then demonstrate storing and using them
input_text = st.text_input("Enter your name")  
st.write(input_text)  

input_number = st.number_input("Enter your age", min_value=0, max_value=150)  

if input_number < 18:  
    st.markdown(":red[You] cannot drink alcohol :cocktail:")  
else:  
    st.markdown(":green[You] can drink alcohol :cocktail:")  

input_date = st.date_input("Date of birth")  
st.write(datetime.datetime.now().date())  
st.write(input_date)  


# Selection Interactivity  
st.subheader("Interactivity - Selection")  

country_of_residence = st.radio("Where do you live?", ["Spain", "Portugal", "United Kingdom"])  

if country_of_residence == "Spain":  
    population = 47  
    st.write(f"Spain has {population} million inhabitants.")  
elif country_of_residence == "Portugal":  
    population = 8  
    st.write(f"Portugal has {population} million inhabitants.")  

# Data Section  
st.subheader("Data")  
# Demonstrate handling and visualizing data in Streamlit  


import pandas as pd
import random

# first without the visits field-> show static table and dataframe, then add visits and then give column config to the df
df = pd.DataFrame(
    {
        "web":["google","youtube","facebook"],
        "url":["https://google.com","https://youtube.com","https://facebook.com"],
        "rating":[4,5,4],
    }
    )

st.table(df)
#display computer capacity, download, filter etc.
st.dataframe(df)

df = pd.DataFrame(
    {
        "web":["google","youtube","facebook"],
        "url":["https://google.com","https://youtube.com","https://facebook.com"],
        "rating":[4,5,4],
        "visits (last 30 days)":[[random.randint(0, 5000) for _ in range(30)] for _ in range(3)]
    }
    )

st.table(df)

st.dataframe(df,
             column_config={
                 "web":"Web Page",
                 "url":st.column_config.LinkColumn("Link"),
                 "rating":st.column_config.NumberColumn(
                     label = "Note", 
                     format="%d ⭐"),
                 "visits (last 30 days)": st.column_config.LineChartColumn("Visits History", y_min=0, y_max=5000)
             },
             hide_index=True)

edited_df = st.data_editor(df)

df = pd.DataFrame(
    {
       "web":["google","youtube","facebook"],
        "url":["https://google.com","https://youtube.com","https://facebook.com"],
        "rating":[4,5,4],
   }
)


edited_df = st.data_editor(df,
                column_config={
                 "web":"Pagina Web",
                 "url":st.column_config.LinkColumn("Link"),
                 "rating":st.column_config.NumberColumn(
                     label = "Note", 
                     format="%d ⭐"),
             },
             hide_index=True)

st.metric("Ventas (€)","57 M€","-8%")
st.metric("Beneficio (€)","24 M€","10 M€")

st.json({
        "web":["google","youtube","facebook"],
        "url":["https://google.com","https://youtube.com","https://facebook.com"],
        "rating":[4,5,4],
        "visits (last 30 days)":[[random.randint(0, 5000) for _ in range(30)] for _ in range(3)]
    })

st.subheader("Visualization")
# Visualization. First, the default Streamlit ones, which are based on Altair

import pandas as pd
import numpy as np

data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(data)

st.line_chart(data, color=["#fcba03","#6bfc03","#1b300c"])

import streamlit as st
import pandas as pd

# Coordinates of Madrid
madrid_lat = 40.4168
madrid_lon = -3.7038
number_of_points = 100

# Create DataFrame with Madrid's coordinates
df = pd.DataFrame({'latitude': np.random.normal(madrid_lat, 1.2, number_of_points),
                    'longitude': np.random.normal(madrid_lon, 1.2, number_of_points)})

# Display map centered on Madrid
st.map(df, latitude="latitude", longitude="longitude", zoom=3)

# Now the rest
# matplotlib
import matplotlib.pyplot as plt
x = np.linspace(0, 10, 100)


y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y)
# Add later
ax.set_ylabel("Y Axis")
ax.set_xlabel("X Axis")
ax.set_title("Sine")
st.pyplot(fig)

# plotly
import plotly.express as px

fig = px.line(x=x, y=y)

st.plotly_chart(fig)

## LAYOUT

st.subheader("LAYOUT")

with st.sidebar: #like aside
    st.write("I am writing in the sidebar")
    st.radio("Pick",[1,2,3])

container1 = st.container()
container1.write("HI")

container2 = st.container()
container2.write("BYE")

container1.write("HI AGAIN")



with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("HI!!!")
    with col2:
        st.checkbox("PICK ONE",["ENDESA","IBERDROLA"])
    with col3:
        st.data_editor(df)

with st.container():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.write("I am where i wanted to be") 

tab1, tab2 = st.tabs(["Tab 1","Tab 2"])
with tab1:
    st.write("Content Tab 1")
tab2.write(df)

with st.expander("This is a desplegable"):
    st.write("Content")
