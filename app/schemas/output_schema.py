from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime, time
from typing import List, Self
from app.schemas.input_schema import Interest
import re

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

class Flight(BaseModel):
    origin_airport: str
    destination_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime
    airline: str
    estimated_cost: int = Field(ge=0)
    
    @model_validator(mode='after')
    def check_datetime_order(self) -> Self:
        if self.arrival_datetime <= self.departure_datetime:
            raise ValueError("Arrival datetime must be after departure datetime")
        return self

    @model_validator(mode='after')
    def check_airport_code_format(self) -> Self:
        pattern = r"^[A-Z]{3}$"
        if not re.match(pattern, self.origin_airport):
            raise ValueError(f"origin_airport '{self.origin_airport}' is not a valid 3-letter IATA code")
        if not re.match(pattern, self.destination_airport):
            raise ValueError(f"destination_airport '{self.destination_airport}' is not a valid 3-letter IATA code")
        return self

class Hotel(BaseModel):
    name: str
    city: str
    check_in_date: date
    check_out_date: date
    estimated_cost_per_night: int = Field(ge=0)
    
    @model_validator(mode='after')
    def check_date_order(self) -> Self:
        if self.check_out_date <= self.check_in_date:
            raise ValueError("Check out date must be after check in date")
        return self

class Itinerary(BaseModel):
    origin: str
    destinations: List[str]
    total_estimated_cost: int
    budget_currency: str
    cost_disclaimer: str
    days: List[Day]
    
    flights: List[Flight] = []
    hotels: List[Hotel] = []
    
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
        flight_total = sum(flight.estimated_cost for flight in self.flights)
        hotel_total = sum(hotel.estimated_cost_per_night * (hotel.check_out_date - hotel.check_in_date).days for hotel in self.hotels)
        self.total_estimated_cost = actual_total + flight_total + hotel_total
        return self
    