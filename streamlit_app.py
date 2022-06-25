import streamlit
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('Breakfast Menu')
streamlit.text(':chicken: Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_show = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_show]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  streamlit.header("Fruityvice Fruit Advice!")
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # show json as dataframe
    streamlit.dataframe(back_from_function)

except URLError:
  streamlit.error()

def get_fruitload_list():
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
  my_data_row = my_cur.fetchall()
  return my_data_row

def insert_fruit_to_list(fruit):
  insert_statement = f"insert into pc_rivery_db.public.fruit_load_list values ('{fruit}')"
  print(insert_statement)
  my_cur = my_cnx.cursor()
  my_cur.execute(insert_statement)
  return 'Thanks for adding ' + fruit
#   my_data_row = my_cur.fetchall()
  
if streamlit.button("Get Fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.header("My fruit load list contains: ")
  fruit_list = get_fruitload_list()
  streamlit.dataframe(fruit_list)

# fruits_to_list = [fruit[0] for fruit in list(my_data_row)]

  fruit_choice = streamlit.text_input('What fruit would you like to add ?')
  if fruit_choice != '':
    text = insert_fruit_to_list(fruit_choice)
    streamlit.write(text)
  
  my_cnx.close()

# select_fruit = streamlit.multiselect("What fruit would you like to select ?", fruits_to_list, ["banana"])
