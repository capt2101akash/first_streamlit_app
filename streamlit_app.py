import streamlit
import pandas as pd 
import requests
import snowflake.connector

streamlit.header('Breakfast Menu')
streamlit.text(':chicken: Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_show = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_show]
streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# show json as dataframe
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("My fruit load list contains: ")
streamlit.dataframe(my_data_row)

fruits_to_list = [fruit[0] for fruit in list(my_data_row)]

fruit_choice = streamlit.text_input('What fruit would you like to add ?','banana')
streamlit.write('Thanks for adding ', fruit_choice)

select_fruit = streamlit.multiselect("What fruit would you like to select ?", fruits_to_list, ["banana"])
