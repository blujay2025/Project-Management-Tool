######################### API Stuff!!! ##############################

# import requests

# # Define the base URL of the PokeAPI
# base_url = "https://pokeapi.co/api/v2/pokemon/"

# # Specify the name of the Pokémon you want to look up
# pokemon_name = "pikachu"

# # Create the full URL
# url = f"{base_url}{pokemon_name}"

# # Make the GET request to the API
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the response JSON
#     pokemon_data = response.json()
    
#     # Extract specific information from the data
#     name = pokemon_data['name']
#     height = pokemon_data['height']
#     weight = pokemon_data['weight']
#     abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]

#     # Print out the information
#     print(f"Name: {name.capitalize()}")
#     print(f"Height: {height}")
#     print(f"Weight: {weight}")
#     print(f"Abilities: {', '.join(abilities)}")
# else:
#     print(f"Error: {response.status_code} - Could not retrieve data for {pokemon_name}")









# Web Scraping - BeautifulSoup4 and Selenium (for dynamic webpages)
import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())