import pandas as pd
from geopy.distance import geodesic

DATA_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
df = pd.read_csv(DATA_URL)

large_df = df[
    (df["type"] == "large_airport") & 
    (df["scheduled_service"] == "yes") & 
    (df["iata_code"].notna()) & 
    (df["iata_code"].str.len() == 3) 
].copy() 

LARGE_AIRPORTS = large_df.to_dict(orient="records")

PREFERRED_HUBS = {
    "london": "LHR",
    "new york": "JFK",
    "chicago": "ORD",
    "paris": "CDG",
    "rome": "FCO",
    "san francisco": "SFO",
    "tokyo": "HND",
    "venice": "VCE",
    "florence": "FLR",
    "munich": "MUC",
    "vienna": "VIE",
    "prague": "PRG",
}


CITY_INDEX = {}


for _, row in large_df[large_df["municipality"].notna()].iterrows():
    city_key = row["municipality"].strip().lower()
    if city_key not in CITY_INDEX:
        CITY_INDEX[city_key] = (row["latitude_deg"], row["longitude_deg"])


for _, row in df[df["municipality"].notna()].iterrows():
    city_key = row["municipality"].strip().lower()
    if city_key not in CITY_INDEX:
        CITY_INDEX[city_key] = (row["latitude_deg"], row["longitude_deg"])

def get_airport_code(city_name: str, radius_km: float = 100.0) -> str | None:
    if not city_name or not isinstance(city_name, str):
        return None

    clean_city = city_name.strip().lower()


    if clean_city in PREFERRED_HUBS:
        return PREFERRED_HUBS[clean_city]

    
    city_coords = CITY_INDEX.get(clean_city)
    if not city_coords:
        return None

    
    candidates = []
    for ap in LARGE_AIRPORTS:
        dist = geodesic(city_coords, (ap["latitude_deg"], ap["longitude_deg"])).km
        if dist <= radius_km:
            candidates.append((dist, ap))

    if not candidates:
        nearest = min(
            LARGE_AIRPORTS,
            key=lambda ap: geodesic(city_coords, (ap["latitude_deg"], ap["longitude_deg"])).km
        )
        return nearest["iata_code"]

    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]["iata_code"]