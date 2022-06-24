import streamlit
import pandas as pd 
import requests

streamlit.header('Breakfast Menu')
streamlit.text(':chicken: Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_show = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_show]
streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# show json as dataframe
streamlit.dataframe(fruityvice_normalized)
