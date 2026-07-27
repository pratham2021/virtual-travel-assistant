from pydantic import BaseModel, Field, model_validator
from datetime import date, time
from typing import List, Self
from input_schema import Interest

class Activity(BaseModel):
  start_time: time
  duration_minutes: int = Field(gt=0)
  name: str
  category: Interest
  description: str # short sentence
  estimated_cost: int = Field(ge=0)

class Day(BaseModel):
    city: str
    day_date: date
    theme: str
    activities: List[Activity]

class Itinerary(BaseModel):
    origin: str
    destinations: List[str]
    total_estimated_cost: int
    budget_currency: str
    cost_disclaimer: str
    days: List[Day]
    
    @model_validator(mode='after')
    def check_date_order(self) -> Self:
        if not self.days:
            raise ValueError("Itinerary must contain at least one day")
        for i in range(len(self.days) - 1):    
            if self.days[i].day_date >= self.days[i+1].day_date:
                raise ValueError("Days must be in strictly increasing chronological order with no duplicates")
        return self
    
    @model_validator(mode='after')
    def recompute_total_cost(self) -> Self:
        actual_total = sum(activity.estimated_cost for day in self.days for activity in day.activities)
        self.total_estimated_cost = actual_total
        return self
    