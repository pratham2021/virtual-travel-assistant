import os
import requests
from dotenv import load_dotenv
from datetime import date, datetime
from input_schema import TravelStyle
from places_client import search_places, get_city_coordinates
from airport_codes import get_airport_code

load_dotenv()

duffel_token = os.getenv("DUFFEL_ACCESS_TOKEN")
google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")

CABIN_CLASS_MAP = {
  TravelStyle.BACKPACKING: "economy",
  TravelStyle.MID_RANGE: "economy",
  TravelStyle.LUXURY: "business"
}

def build_passenger_list(traveler_ages: list[int], num_passengers: int) -> list[dict]:
    if not traveler_ages:
        return [{"type": "adult"} for _ in range(num_passengers)]
    
    passenger_list = []
    for age in traveler_ages:
        if age >= 18:
            passenger_list.append({"type": "adult"})
        else:
            passenger_list.append({"age": age})
    return passenger_list
    
def search_flights(origin_airport: str, destination_airport: str, departure_date: date, traveler_ages: list[int], num_passengers: int, cabin_class: str) -> list[dict]:
    url = "https://api.duffel.com/air/offer_requests"
    headers = { # This is to let the API know that it is indeed us who is pinging the API
      "Authorization": f"Bearer {duffel_token}", # authenticates your request using a secure, unique access token. we have a valid account and permission to make API calls
      "Duffel-Version": "v2", # version of the API version we wish to use
      "Content-Type": "application/json", # we're telling the API we're sending JSON data
      "Accept": "application/json" # we're requesting for the aPI to send data back as JSON
    }

    body = {
        "data": {
          "slices": [
              {
                  "origin": origin_airport,
                  "destination": destination_airport,
                  "departure_date": departure_date.isoformat()
              }
          ],
          "passengers": build_passenger_list(traveler_ages, num_passengers),
          "cabin_class": cabin_class
      }
    }
    
    response = requests.post(url=url, headers=headers, json=body)
    
    if response.status_code not in (200, 201):
        print(f"Duffel API error ({response.status_code}): {response.json()}")
        return []
    
    offers = response.json()["data"]["offers"]
    simplified_offers = []

    for offer in offers:
        segments = offer["slices"][0]["segments"]
        airline_name = segments[0]["operating_carrier"]["name"]
        if airline_name == "Duffel Airways":
            continue
        
        # segments[-1] is where and when the traveler actually finishes their journey
        simplified_offers.append({
            "origin_airport": segments[0]["origin"]["iata_code"],
            "destination_airport": segments[-1]["destination"]["iata_code"],
            "departure_datetime": segments[0]["departing_at"],
            "arrival_datetime": segments[-1]["arriving_at"],
            "airline": airline_name,
            "estimated_cost": float(offer["total_amount"]),
        })
    
    simplified_offers = sorted(simplified_offers, key=lambda offer: offer["estimated_cost"])
    simplified_offers = simplified_offers[:10]
    return simplified_offers # Return the 10 cheapest options
  
def format_flights_for_prompt(candidate_flights: dict[str, list[dict]]) -> str:
    lines = []
    for leg_label, flights in candidate_flights.items():
        lines.append(f"=== {leg_label.upper()} ===")
        for flight in flights:
            airline = flight["airline"]
            departure = flight["departure_datetime"]
            arrival = flight["arrival_datetime"]
            cost = flight["estimated_cost"]
            line = f"- {airline}: departs {departure}, arrives {arrival} - ${cost}"
            lines.append(line)
        lines.append("")
    result = "\n".join(lines)
    return result