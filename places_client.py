import os
import requests
from dotenv import load_dotenv
from input_schema import Interest, Preference, solo_backpacker, family_of_four, couple_luxury

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

def search_places(destination, query_text):
    # API endpoint that I'm sending requests to
    url = "https://places.googleapis.com/v1/places:searchText"
    
    # builds the headers dictionary
    headers = {
      "Content-Type": "application/json",
      "X-Goog-Api-Key": api_key,
      "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating"
    }
    
    # request body
    body = {
      "textQuery": f"{query_text} in {destination}"
    }
    
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200: # if the API request didn't succeed, return an empty list
        print(f"Places API error ({response.status_code}): {response.json()}")
        return []
    
    return response.json().get("places", []) # return the 

def get_candidate_venues(preference: Preference) -> dict[Interest, list[dict]]:
    # Each interest represents a genuinely different category of thing the traveler wants
    candidate_venues = {}
    for interest in preference.interests:
        query_phrase = INTEREST_QUERY_MAP[interest]
        results = search_places(preference.destination, query_phrase)
        candidate_venues[interest] = results
    return candidate_venues

candidate_venues = get_candidate_venues(solo_backpacker)
  
# places_client.py - add the formatting function (e.g. format_venues_for_prompt(candidate_venues) right after get_candidate_venues)
def format_venues_for_prompt(candidate_venues: dict[Interest, list[dict]]) -> str:
    lines = []

    for interest, venues in candidate_venues.items():
        lines.append(interest.value.upper() + ":")
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


# itinerary_generator.py - update generate_itinerary to import and call get_candidate_venues and your new formatting function, 
# then combine that text with the serialized preferences into the user message


# prompts.py - update SYSTEM_PROMPT with the new instructions about only selecting from provided venues
