# Step 3: Design your preference schema
from pydantic import BaseModel, Field, model_validator
from datetime import date
from enum import Enum
from typing import List, Self

class TravelerType(str, Enum):
    SOLO = "solo"
    COUPLE = "couple"
    FAMILY_WITH_KIDS = "family_with_kids"
    FRIEND_GROUP = "friend_group"
    
class BudgetScope(str, Enum):
    TOTAL_TRIP = "total_trip"
    PER_DAY = "per_day"

class TravelStyle(str, Enum):
    LUXURY = "luxury"
    MID_RANGE = "mid_range"
    BACKPACKING = "backpacking"
    
class Pace(str, Enum):
    RELAXED = "relaxed"
    MODERATE = "moderate"
    PACKED = "packed"

class Interest(str, Enum):
    NIGHTLIFE = "nightlife"
    FOOD = "food"
    LOCAL_CULTURE = "local_culture"
    NATURE = "nature"
    FAMILY_ACTIVITIES = "family_activities"
    HISTORY = "history"
    ART = "art"
    ARCHITECTURE = "architecture"
    SHOPPING = "shopping"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    BEACHES = "beaches"
    WELLNESS = "wellness"

class CityStop(BaseModel):
    city: str
    arrival_date: date
    departure_date: date
    
    @model_validator(mode='after')
    def check_date_order(self) -> Self:
        if self.arrival_date > self.departure_date:
            raise ValueError("The departure date can't be before arrival date")
        return self

# Decide the schema additions
    # Preference
        # include_flights:bool
        # include_hotels: bool

class Preference(BaseModel):
    origin: str
    destinations: List[CityStop]
    group_size: int = Field(gt=0)
    traveler_type: TravelerType
    
    budget_amount: float = Field(gt=0)
    budget_scope: BudgetScope
    budget_currency: str = "USD" # string (ISO code, e.g. USD)
    
    travel_style: TravelStyle
    pace: Pace
    
    interests: List[Interest] = []
    
    hard_constraints: List[str] = []
    soft_preferences: List[str] = []
    
    traveler_ages: List[int] = []
    
    include_flights: bool = False
    include_hotels: bool = False
    
    notes: str = ""
    
    @model_validator(mode='after')
    def check_stops_are_sequential(self) -> Self:
        for i in range(len(self.destinations) - 1):
            if self.destinations[i].departure_date != self.destinations[i+1].arrival_date:
                raise ValueError("There is a gap between city stop and the next")
        return self
    
    @model_validator(mode='after')
    def check_group_size_consistency(self) -> Self:
        if self.traveler_type == TravelerType.SOLO:
            if self.group_size != 1:
                raise ValueError("SOLO travelers must have a group_size of 1.")
        elif self.traveler_type == TravelerType.COUPLE:
            if self.group_size != 2:
                raise ValueError("COUPLE travelers must have a group_size of 2.")
        elif self.traveler_type == TravelerType.FAMILY_WITH_KIDS:
            if self.group_size < 2:
                raise ValueError("FAMILY_WITH_KIDS must have a group_size of at least 2.")
        elif self.traveler_type == TravelerType.FRIEND_GROUP:
            if self.group_size < 2:
                raise ValueError("FRIEND_GROUP must have a group_size of at least 2.")
        return self

    @model_validator(mode='after')
    def check_traverler_ages_consistency(self) -> Self:
        if self.traveler_ages and len(self.traveler_ages) != self.group_size:
            raise ValueError("The number of travelers must match group size if provided")
        return self

solo_backpacker = Preference(origin="Austin", destinations=[CityStop(city="Bangkok", arrival_date=date(2026, 7, 26), departure_date=date(2026, 7, 30))], group_size=1, traveler_type=TravelerType.SOLO,
                            budget_amount=500, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.BACKPACKING, pace=Pace.PACKED, 
                            interests=[Interest.NIGHTLIFE, Interest.FOOD, Interest.LOCAL_CULTURE], hard_constraints=[], soft_preferences=["prefers_walking", "avoid_crowds"])

family_of_four = Preference(origin="Austin", destinations=[CityStop(city="Orlando", arrival_date=date(2026, 8, 1), departure_date=date(2026, 8, 11))], group_size=4, traveler_type=TravelerType.FAMILY_WITH_KIDS,
                            budget_amount=4000, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.MID_RANGE, pace=Pace.RELAXED, 
                            interests=[Interest.NATURE, Interest.FAMILY_ACTIVITIES], hard_constraints=["no_red_eye_flights"], soft_preferences=["early_riser"])

couple_luxury = Preference(origin="San Francisco", destinations=[CityStop(city="Kyoto", arrival_date=date(2026, 8, 1), departure_date=date(2026, 8, 8))], group_size=2, 
                            traveler_type=TravelerType.COUPLE,
                            budget_amount=8000, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.LUXURY, pace=Pace.RELAXED, 
                            interests=[Interest.FOOD, Interest.NIGHTLIFE], hard_constraints=[], soft_preferences=["prefers_walking"])



tight_budget_test = Preference(
    origin="Austin",
    destinations=[CityStop(city="Bangkok", arrival_date=date(2026, 7, 26), departure_date=date(2026, 7, 30))],
    group_size=1,
    traveler_type=TravelerType.SOLO,
    budget_amount=10,
    budget_scope=BudgetScope.TOTAL_TRIP,
    travel_style=TravelStyle.BACKPACKING,
    pace=Pace.PACKED,
    interests=[Interest.NIGHTLIFE, Interest.FOOD, Interest.LOCAL_CULTURE],
    hard_constraints=[],
    soft_preferences=["prefers_walking", "avoid_crowds"],
)

multi_country_test = Preference(
    origin="Austin",
    destinations=[
        CityStop(city="Tokyo", arrival_date=date(2026, 8, 1), departure_date=date(2026, 8, 4)),
        CityStop(city="Bangkok", arrival_date=date(2026, 8, 4), departure_date=date(2026, 8, 6)),
        CityStop(city="Rome", arrival_date=date(2026, 8, 6), departure_date=date(2026, 8, 9)),
    ],
    group_size=1,
    traveler_type=TravelerType.SOLO,
    budget_amount=1300,
    budget_scope=BudgetScope.TOTAL_TRIP,
    budget_currency="USD",
    travel_style=TravelStyle.MID_RANGE,
    pace=Pace.MODERATE,
    interests=[Interest.FOOD, Interest.HISTORY],
    hard_constraints=[],
    soft_preferences=[],
)