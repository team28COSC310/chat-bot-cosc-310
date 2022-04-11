from bs4 import BeautifulSoup
import googlemaps
from datetime import datetime

# To enable directions add a google API key here
gmaps = googlemaps.Client(key="AIzaSyCM1G81TL4nxyP4p-Ralg0Twza_mtKVphE")


def directions(origin, destination, departure_time=datetime.now()):
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="transit",
                                         departure_time=departure_time)

    try:
        direction_str = f"Directions to get to {destination}:\n\n"

        for i, step in enumerate(directions_result[0]['legs'][0]['steps']):
            instructions = BeautifulSoup(step['html_instructions'])
            direction_str += f"{i+1}: {instructions.get_text()} ({step['duration']['text']})"
            if i != len(directions_result[0]['legs'][0]['steps']) - 1:
                direction_str += "\n\n"

        return direction_str

    except IndexError:
        return "Sorry, no directions information is available."

