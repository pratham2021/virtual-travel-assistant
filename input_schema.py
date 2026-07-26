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

class Preference(BaseModel):
    origin: str
    destination: str
    start_date: date
    end_date: date
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
    
    notes: str = ""
    
    @model_validator(mode='after')
    def check_date_order(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError("The start date cannot be after the end date.")
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

solo_backpacker = Preference(origin="Austin", destination="Bangkok", start_date=date(2026, 7, 26), end_date=date(2026, 7, 30), group_size=1, traveler_type=TravelerType.SOLO,
                            budget_amount=500, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.BACKPACKING, pace=Pace.PACKED, 
                            interests=[Interest.NIGHTLIFE, Interest.FOOD, Interest.LOCAL_CULTURE], hard_constraints=[], soft_preferences=["prefers_walking", "avoid_crowds"])


family_of_four = Preference(origin="Austin", destination="Orlando", start_date=date(2026, 8, 1), end_date=date(2026, 8, 11), group_size=4, traveler_type=TravelerType.FAMILY_WITH_KIDS,
                            budget_amount=4000, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.MID_RANGE, pace=Pace.RELAXED, 
                            interests=[Interest.NATURE, Interest.FAMILY_ACTIVITIES], hard_constraints=["no_red_eye_flights"], soft_preferences=["early_riser"])

couple_luxury = Preference(origin="San Francisco", destination="Kyoto", start_date=date(2026, 8, 1), end_date=date(2026, 8, 8), group_size=2, 
                            traveler_type=TravelerType.COUPLE,
                            budget_amount=8000, budget_scope=BudgetScope.TOTAL_TRIP, travel_style=TravelStyle.LUXURY, pace=Pace.RELAXED, 
                            interests=[Interest.FOOD, Interest.NIGHTLIFE], hard_constraints=[], soft_preferences=["prefers_walking"])


