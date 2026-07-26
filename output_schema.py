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
    day_date: date
    theme: str
    activities: List[Activity]

class Itinerary(BaseModel):
    origin: str
    destination: str
    start_date: date
    end_date: date
    total_estimated_cost: int
    budget_currency: str
    cost_disclaimer: str
    days: List[Day]
    
    @model_validator(mode='after')
    def check_date_order(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError("The start date cannot be after the end date.")
        return self
    
    @model_validator(mode='after')
    def recompute_total_cost(self) -> Self:
        actual_total = sum(activity.estimated_cost for day in self.days for activity in day.activities)
        if self.total_estimated_cost != actual_total:
            raise ValueError(
                f"Total Estimated Cost of ({self.total_estimated_cost}) does not match "
                f"the sum of activity costs ({actual_total})"
            )
        return self
    