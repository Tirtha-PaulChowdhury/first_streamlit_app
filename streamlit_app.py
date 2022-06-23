#Library imports
import streamlit
import pandas

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
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) #added the list, so that the picker will be pre-populated with these values

# Display the table on the page.
streamlit.dataframe(my_fruit_list)   
