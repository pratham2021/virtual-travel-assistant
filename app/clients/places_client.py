import os
import requests
from datetime import date
from dotenv import load_dotenv
from app.schemas.input_schema import (
    Interest,
    Preference,
    solo_backpacker,
    family_of_four,
    couple_luxury,
)
from concurrent.futures import ThreadPoolExecutor # helps us run multiple tasks at the same time

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")

INTEREST_QUERY_MAP = {
    Interest.FOOD: "restaurants and local food",
    Interest.NIGHTLIFE: "bars and nightlife",
    Interest.LOCAL_CULTURE: "local markets and cultural sites",
    Interest.NATURE: "parks and nature attractions",
    Interest.FAMILY_ACTIVITIES: "family friendly attractions",
    Interest.HISTORY: "historical landmarks and temples",
    Interest.ART: "art galleries and museums",
    Interest.ARCHITECTURE: "notable architecture and landmarks",
    Interest.SHOPPING: "shopping districts and markets",
    Interest.ADVENTURE: "outdoor adventure tours and activities",
    Interest.RELAXATION: "quiet gardens and scenic viewpoints",
    Interest.BEACHES: "beaches",
    Interest.WELLNESS: "spas and massage",
}


def get_city_coordinates(city_name: str) -> tuple[float, float] | None:
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.location",
    }

    body = {"textQuery": f"{city_name}"}

    response = requests.post(url, headers=headers, json=body)

    if response.status_code not in (200, 201):
        print(f"Places API error ({response.status_code}): {response.json()}")
        return None

    places = response.json().get("places", [])
    if not places:
        return None

    location = places[0]["location"]
    latitude = location["latitude"]
    longitude = location["longitude"]
    return (latitude, longitude)


def search_places(destination, query_text):
    # Google Places API endpoint that I'm sending requests to
    url = "https://places.googleapis.com/v1/places:searchText"

    # builds the headers dictionary
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating",
    }

    # request body
    body = {"textQuery": f"{query_text} in {destination}"}

    response = requests.post(url, headers=headers, json=body)

    if (
        response.status_code != 200
    ):  # if the API request didn't succeed, return an empty list
        print(f"Places API error ({response.status_code}): {response.json()}")
        return []

    return response.json().get("places", [])


def search_hotels(city_name: str):
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.types",
    }

    body = {"textQuery": f"Hotels and accommodation in {city_name}"}

    response = requests.post(url, headers=headers, json=body)

    if response.status_code not in (200, 201):
        print(f"Places API error ({response.status_code}): {response.json()}")
        return []

    return response.json().get("places", [])

# A list of things to do in each city for each interest
def get_candidate_venues(
    preference: Preference,
) -> dict[str, dict[Interest, list[dict]]]:
    candidate_venues = {} # Start with an empty dictionary that will hold the final, fully-collected results
    
    with ThreadPoolExecutor(max_workers=10) as executor: 
        # Create a pool that can run up to 10 tasks simultaneously;
        # "with" ensures the pool is properly cleaned up once this block finishes
        futures = {} # An empty dictionary that will map each scheduled task to the city+itinerary it represents
        
        for stop in preference.destinations:
            # Loop through every city the traveler is visiting
            for interest in preference.interests:
                # For each city, loop through every interest the traveler scheduled
                query_phrase = INTEREST_QUERY_MAP[interest] # Look up the search phrase that corresponds to this interest
                future = executor.submit(search_places, stop.city, query_phrase)
                # Schedule this specific search to run on the thread pool;
                # this does NOT wait for the search to finish - it returns immediately
                # with a "future" placeholder representing the in-progress task
                
                futures[future] = (stop.city, interest)
                # Remember which city and interest this particular future belongs to.
                # so we can correctly match its result later
        
        # At this point, every search across every city and every interest
        # has already been started and is running concurrently in the background
        
        # Retrieves the results of work that's already running (or already finished) from the first loop.
        for future in futures:
            # Loop through every scheduled task, one at a time, to collect its result
            
            city, interest = futures[future]
            # Look up which city and interest this specific future corresponds to
            
            results = future.result()
            # Get the actual result of this search; this pauses only if that particular
            # search hasn't finished yet - but since they've all been running in parallel,
            # most are likely already done by the time we ask
            
            if city not in candidate_venues:
                candidate_venues[city] = {}
            # If we've not seen this city, create an empty dictionary to hold that city's results
            
            candidate_venues[city][interest] = results
            # Store this search's results in the correct spot: under this city,
            # under this specific interest

    return candidate_venues 
    # Once every result has been collected and organized, return the complete,
    # fully-populated nested dictionary - same shape as the original sequential version,
    # just built using parallel searches instead of one-at-a-time searches

# places_client.py - add the formatting function (e.g. format_venues_for_prompt(candidate_venues) right after get_candidate_venues)
def format_venues_for_prompt(
    candidate_venues: dict[str, dict[Interest, list[dict]]],
) -> str:
    lines = []

    for city, interest_dict in candidate_venues.items():
        lines.append(f"=== {city.upper()} ===")

        for interest, venues in interest_dict.items():
            lines.append(f"{interest.value.upper()}:")
            trimmed_venues = venues[:8]

            for venue in trimmed_venues:
                name = venue["displayName"]["text"]
                address = venue["formattedAddress"]
                rating = venue.get("rating", "no rating")
                line = f"- {name} ({address}) - rating {rating}"
                lines.append(line)
            lines.append("")

    result = "\n".join(lines)
    return result


def format_hotels_for_prompt(candidate_hotels: dict[str, list[dict]]) -> str:
    lines = []
    for city, hotels in candidate_hotels.items():
        lines.append(f"=== {city.upper()} ===")
        for hotel in hotels:
            hotel_name = hotel["name"]
            hotel_rating = hotel["rating"]
            line = f"- {hotel_name} - rating {hotel_rating} stars"
            lines.append(line)
            lines.append("")
    result = "\n".join(lines)
    return result


# Transform raw hotel results into Hotel-shaped dicts
def format_hotels(
    raw_hotels: list[dict], city: str, check_in_date: date, check_out_date: date
) -> list[dict]:
    results = []
    for raw_hotel in raw_hotels:
        if "hotel" not in raw_hotel["types"]:
            continue
        name = raw_hotel["displayName"]["text"]
        rating = raw_hotel.get("rating", "no rating")

        formatted_hotel = {
            "name": name,
            "city": city,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "rating": rating,
        }

        results.append(formatted_hotel)
    return results


# itinerary_generator.py - update generate_itinerary to import and call get_candidate_venues and your new formatting function,
# then combine that text with the serialized preferences into the user message

# prompts.py - update SYSTEM_PROMPT with the new instructions about only selecting from provided venues
