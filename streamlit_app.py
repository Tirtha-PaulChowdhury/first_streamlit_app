#Library imports
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#adding web-app title
streamlit.title('My Mom\'s New Healthy Diner')

#adding the menu
streamlit.header('Breakfast Favourites')
streamlit.text('🍜Omega 3 & Blueberry Oatmeal')
streamlit.text('🍱🍹Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🍐🍞Avocado Toast')


streamlit.header('🍌🍉Build Your own Fruit Smoothie🍓🍍')

#using pandas dataframe to store all the fruits from a file in S3
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#setting the index on fruit column, so that while picking, name of fruits will show up
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so user can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) #added the list, so that the picker will be pre-populated with these values

#only showing fruits selected, instead of all the fruits table
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)   



#checking if fruityvice api is working fine or not
streamlit.header("Fruityvice Fruit Advice!")



#creating function
def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  # Flattening the JSON response
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized



try:
  #taking fruit input from user
  fruit_choice = streamlit.text_input('What fruit would you like information about?')

  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # Creating a pandas dataframe from the flattened data
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()


  
streamlit.header("View Our Fruit List - Add Your Favourites!")

#function for getting the fruit load list
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

  
#adding a streamlit button
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)


  
  
#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit
  
  
#allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)




