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

#taking fruit input from user
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# Flattening the JSON response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Creating a pandas dataframe from the flattened data
streamlit.dataframe(fruityvice_normalized)


#don't run anything past here while we troubleshoot
streamlit.stop()

#checking the snowflake connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit_load_list contains:")
streamlit.dataframe(my_data_rows)


#allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#this will not work correctly but just go with it for now
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from_streamlit')")



