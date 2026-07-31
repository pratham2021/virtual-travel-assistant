import reflex as rx
from rxconfig import config
import datetime
from pydantic import BaseModel

class Destination(BaseModel):
    destination_city_name: str = ""
    departure_date: datetime.date = datetime.date.today()
    arrival_date: datetime.date = datetime.date.today()

class State(rx.State):
    origin: str = ""
    group_size: int = 1
    budget_amount: float = 1000.0
    
    currency_options: dict[str, str] = {
        "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
        "CHF": "Swiss Franc", "CAD": "Canadian Dollar", "AUD": "Australian Dollar", "NZD": "New Zealand Dollar",
        "CNY": "Chinese Yuan", "HKD": "Hong Kong Dollar", "SGD": "Singapore Dollar", "INR": "Indian Rupee",
        "KRW": "South Korean Won", "THB": "Thai Baht", "MYR": "Malaysian Ringgit", "IDR": "Indonesian Rupiah",
        "PHP": "Philippine Peso", "VND": "Vietnamese Dong", "TWD": "Taiwan Dollar", "PKR": "Pakistani Rupee",
        "BDT": "Bangladeshi Taka", "LKR": "Sri Lankan Rupee", "NPR": "Nepalese Rupee", "MMK": "Myanmar Kyat",
        "KHR": "Cambodian Riel", "LAK": "Lao Kip", "BND": "Brunei Dollar", "MOP": "Macanese Pataca",
        "MNT": "Mongolian Tugrik", "AED": "UAE Dirham", "SAR": "Saudi Riyal", "QAR": "Qatari Riyal",
        "KWD": "Kuwaiti Dinar", "BHD": "Bahraini Dinar", "OMR": "Omani Rial", "JOD": "Jordanian Dinar",
        "ILS": "Israeli Shekel", "TRY": "Turkish Lira", "EGP": "Egyptian Pound", "MAD": "Moroccan Dirham",
        "TND": "Tunisian Dinar", "DZD": "Algerian Dinar", "LYD": "Libyan Dinar", "SDG": "Sudanese Pound",
        "NGN": "Nigerian Naira", "GHS": "Ghanaian Cedi", "KES": "Kenyan Shilling", "TZS": "Tanzanian Shilling",
        "UGX": "Ugandan Shilling", "ZAR": "South African Rand", "ETB": "Ethiopian Birr", "XOF": "West African CFA Franc",
        "XAF": "Central African CFA Franc", "RWF": "Rwandan Franc", "BIF": "Burundian Franc", "CDF": "Congolese Franc",
        "GNF": "Guinean Franc", "SLL": "Sierra Leonean Leone", "LRD": "Liberian Dollar", "GMD": "Gambian Dalasi",
        "CVE": "Cape Verdean Escudo", "STN": "Sao Tome Dobra", "AOA": "Angolan Kwanza", "ZMW": "Zambian Kwacha",
        "MWK": "Malawian Kwacha", "MZN": "Mozambican Metical", "BWP": "Botswana Pula", "NAD": "Namibian Dollar",
        "SZL": "Swazi Lilangeni", "LSL": "Lesotho Loti", "MUR": "Mauritian Rupee", "SCR": "Seychellois Rupee",
        "MGA": "Malagasy Ariary", "KMF": "Comorian Franc", "DJF": "Djiboutian Franc", "SOS": "Somali Shilling",
        "ERN": "Eritrean Nakfa", "SSP": "South Sudanese Pound", "MXN": "Mexican Peso", "BRL": "Brazilian Real",
        "ARS": "Argentine Peso", "CLP": "Chilean Peso", "COP": "Colombian Peso", "PEN": "Peruvian Sol",
        "UYU": "Uruguayan Peso", "PYG": "Paraguayan Guarani", "BOB": "Bolivian Boliviano", "VES": "Venezuelan Bolivar",
        "GYD": "Guyanese Dollar", "SRD": "Surinamese Dollar", "GTQ": "Guatemalan Quetzal", "HNL": "Honduran Lempira",
        "NIO": "Nicaraguan Cordoba", "CRC": "Costa Rican Colon", "PAB": "Panamanian Balboa", "DOP": "Dominican Peso",
        "JMD": "Jamaican Dollar", "TTD": "Trinidad and Tobago Dollar", "BBD": "Barbadian Dollar", "BSD": "Bahamian Dollar",
        "BZD": "Belize Dollar", "XCD": "East Caribbean Dollar", "HTG": "Haitian Gourde", "CUP": "Cuban Peso",
        "AWG": "Aruban Florin", "ANG": "Netherlands Antillean Guilder", "KYD": "Cayman Islands Dollar", "BMD": "Bermudian Dollar",
        "PLN": "Polish Zloty", "CZK": "Czech Koruna", "HUF": "Hungarian Forint", "RON": "Romanian Leu",
        "BGN": "Bulgarian Lev", "RSD": "Serbian Dinar", "UAH": "Ukrainian Hryvnia", "RUB": "Russian Ruble",
        "BYN": "Belarusian Ruble", "GEL": "Georgian Lari", "AMD": "Armenian Dram", "AZN": "Azerbaijani Manat",
        "KZT": "Kazakhstani Tenge", "UZS": "Uzbekistani Som", "TJS": "Tajikistani Somoni", "KGS": "Kyrgyzstani Som",
        "TMT": "Turkmenistani Manat", "MDL": "Moldovan Leu", "ALL": "Albanian Lek", "MKD": "Macedonian Denar",
        "BAM": "Bosnia-Herzegovina Mark", "ISK": "Icelandic Krona", "NOK": "Norwegian Krone", "SEK": "Swedish Krona",
        "DKK": "Danish Krone", "FJD": "Fijian Dollar", "PGK": "Papua New Guinean Kina", "SBD": "Solomon Islands Dollar",
        "TOP": "Tongan Pa'anga", "VUV": "Vanuatu Vatu", "WST": "Samoan Tala", "XPF": "CFP Franc",
        "AFN": "Afghan Afghani", "IRR": "Iranian Rial", "IQD": "Iraqi Dinar", "SYP": "Syrian Pound",
        "LBP": "Lebanese Pound", "YER": "Yemeni Rial", "BTN": "Bhutanese Ngultrum", "MVR": "Maldivian Rufiyaa",
        "KPW": "North Korean Won",
    }
    
    budget_currency: str = "USD"
    notes: str = ""
    
    traveler_type_options = {
        "Solo": "solo",
        "Couple": "couple",
        "Family with kids": "family_with_kids",
        "Friends": "friend_group",
    }
    
    budget_scope_options = {
        "Total trip": "total_trip",
        "Budget per day": "per_day",
    }
    
    travel_style_options = {
        "Backpacking": "backpacking",
        "Mid range": "mid_range",
        "Luxury": "luxury",
    }
    
    pace_options = {
        "Relaxed": "relaxed",
        "Moderate": "moderate",
        "Packed": "packed",
    }
    
    INTEREST_OPTIONS: dict[str, str] = {
        "Nightlife": "nightlife",
        "Food": "food",
        "Local Culture": "local_culture",
        "Nature": "nature",
        "Family Activities": "family_activities",
        "History": "history",
        "Art": "art",
        "Architecture": "architecture",
        "Shopping": "shopping",
        "Adventure": "adventure",
        "Relaxation": "relaxation",
        "Beaches": "beaches",
        "Wellness": "wellness",
    }
        
    selected_interests: list[str] = []
    
    current_traveler_type = "Solo"
    current_budget_scope = "Total trip"
    current_travel_style = "Mid range"
    current_pace_option = "Moderate"
    
    traveler_type: str = "solo" # ["solo", "couple", "family_with_kids", "friend_group"]
    budget_scope: str = "total_trip" # ["total_trip", "per_day"]
    travel_style: str = "mid_range" # ["backpacking", "mid_range", "luxury"]
    pace: str = "moderate" # ["relaxed", "moderate", "packed"]
    
    include_flights: bool = False
    include_hotels: bool = False
    
    destination_error = ""
    
    HARD_CONSTRAINT_OPTIONS: dict[str, str] = {
        "Wheelchair accessible": "wheelchair_accessible",
        "No red-eye flights": "no_red_eye_flights",
        "Vegetarian": "vegetarian",
        "Vegan": "vegan",
        "Gluten-free": "gluten_free",
        "No stairs": "no_stairs",
        "Service animal accommodation": "service_animal_accommodation",
        "Quiet/low-sensory environments": "quiet_low_sensory_environments",
    }
    hard_constraints: list[str] = []
    
    SOFT_PREFERENCE_OPTIONS: dict[str, str] = {
        "Prefers walking": "prefers_walking",
        "Avoid crowds": "avoid_crowds",
        "Early riser": "early_riser",
        "Night owl": "night_owl",
        "Prefers public transit": "prefers_public_transit",
        "Loves trying new foods": "loves_new_foods",
        "Prefers quieter destinations": "prefers_quieter_destinations",
        "Likes to shop": "likes_to_shop",
    }
    soft_preferences: list[str] = []
    
    traveler_ages: list[int] = []
    
    current_traveler_age: int = 0
    
    destinations: list[Destination] = []
    
    destination_city_name: str = ""
    departure_date: datetime.date | None = None
    arrival_date: datetime.date | None = None
    
    def set_origin(self, value: str):
        self.origin = value
    
    def set_group_size(self, group_size: str):
        try:
            self.group_size = int(group_size)
        except ValueError:    
            self.group_size = 1
    
    def set_budget_amount(self, budget_amount: str):
        try:
            self.budget_amount = float(budget_amount)
        except ValueError:
            self.budget_amount = 1000.0
    
    def set_notes(self, notes: str):
        self.notes = notes
    
    def set_current_traveler_age(self, value: str):
        try:
            age = int(value)
            if age < 0:
                age = 0
            self.current_traveler_age = age
        except ValueError:
            self.current_traveler_age = 0
    
    def set_destination_city_name(self, destination: str):
        self.destination_city_name = destination
    
    def set_departure_date(self, date_string):
        if date_string:
            parsed_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            if self.arrival_date and parsed_datetime.date() >= self.arrival_date: # make sure it's not after arrival date
                return
            self.departure_date = parsed_datetime.date()
        else:
            self.departure_date = None
            
    def set_arrival_date(self, date_string):
        if date_string:
            parsed_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            if self.departure_date and parsed_datetime.date() <= self.departure_date: # make sure it's not before departure date
                return
            self.arrival_date = parsed_datetime.date()
        else:
            self.arrival_date = None
            
    @rx.var
    def departure_date_str(self) -> str:
        if isinstance(self.departure_date, datetime.date):
            return self.departure_date.strftime("%Y-%m-%d")
        return ""
    
    @rx.var
    def arrival_date_str(self) -> str:
        if isinstance(self.arrival_date, datetime.date):
            return self.arrival_date.strftime("%Y-%m-%d")
        return ""
    
    # Format currencies
    @rx.var
    def formatted_currencies(self) -> list[str]:
        return [f"{currency_abbreviation} - {currency_name}" for currency_abbreviation, currency_name in self.currency_options.items()]
    
    def handle_currency_option_change(self, selected_formatted_string: str):
        self.budget_currency = selected_formatted_string.split(" - ")[0]
    
    def handle_traveler_type_change(self, traveler_type_option: str):
        self.current_traveler_type = traveler_type_option    
        self.traveler_type = self.traveler_type_options[traveler_type_option]
    
    def handle_budget_scope_change(self, budget_scope_option: str):
        self.current_budget_scope = budget_scope_option
        self.budget_scope = self.budget_scope_options[budget_scope_option]
    
    def handle_travel_style_change(self, travel_style_option: str):
        self.current_travel_style = travel_style_option
        self.travel_style = self.travel_style_options[travel_style_option]
    
    def handle_pace_change(self, pace_option: str):
        self.current_pace_option = pace_option
        self.pace = self.pace_options[pace_option]
    
    @rx.event
    def set_include_flights(self, value: bool):
        self.include_flights = value
        
    @rx.event
    def set_include_hotels(self, value: bool):
        self.include_hotels = value
    
    def toggle_item(self, interest: str, is_checked: bool):
        if is_checked:
            if interest not in self.selected_interests:
                self.selected_interests.append(interest)
        elif interest in self.selected_interests:
            self.selected_interests.remove(interest)
    
    def toggle_hard_constraint(self, constraint: str, is_checked: bool):
        if is_checked:
            if constraint not in self.hard_constraints:
                self.hard_constraints.append(constraint)
        elif constraint in self.hard_constraints:
            self.hard_constraints.remove(constraint)
    
    def toggle_soft_preference(self, constraint: str, is_checked: bool):
        if is_checked:
            if constraint not in self.soft_preferences:
                self.soft_preferences.append(constraint)
        elif constraint in self.soft_preferences:
            self.soft_preferences.remove(constraint)
    
    def add_traveler_age(self):
        if len(self.traveler_ages) < self.group_size:
            self.traveler_ages.append(self.current_traveler_age)
            self.current_traveler_age = 0
    
    def remove_traveler_age(self, age: int):
        if age in self.traveler_ages:
            self.traveler_ages.remove(age)
    
    def add_destination(self):
        cleaned_destination = self.destination_city_name.strip()
        if not cleaned_destination or cleaned_destination == "":
            self.destination_error = "Please enter a city name."
            return
        
        if not self.departure_date or not self.arrival_date:
            self.destination_error = "Arrival date can't be before departure date."
            return
        
        new_destination = Destination(destination_city_name=cleaned_destination, departure_date=self.departure_date, arrival_date=self.arrival_date)
    
        self.destinations.append(new_destination)
        self.destination_city_name = ""
        self.departure_date = None
        self.arrival_date = None
        self.destination_error = ""

    def remove_destination(self, destination: Destination):
        if destination in self.destinations:
            self.destinations.remove(destination)
            
def index() -> rx.Component:
    current_currency = f"{State.budget_currency} - {State.currency_options[State.budget_currency]}"
    
    return rx.vstack(
        rx.heading("Plan Your Trip", size="7"),
            
        rx.input(    
            placeholder="",
            value=State.origin, 
            on_change=State.set_origin
        ),
            
        rx.input(
            type="number",            
            value=State.group_size,
            on_change=State.set_group_size,
            placeholder="1"
        ),
            
        rx.input(
            type="number",
            value=State.budget_amount,
            step=0.01,
            on_change=State.set_budget_amount,
        ),
            
        rx.select(
            State.formatted_currencies, # A list of strings or values that populate the choices in the dropdown menu.
            value=current_currency, # A state variable bound to the currently selected option
            on_change=State.handle_currency_option_change # What happens when the user selects a different option from the dropdown, manipulating the state variable.
        ),
            
        rx.select(
            State.traveler_type_options.keys(), # A list of strings or values that populate the choices in the dropdown menu.
            value=State.current_traveler_type, # A state variable bound to the currently selected option
            on_change=State.handle_traveler_type_change # What happens when the user selects a different option from the dropdown, manipulating the state variable.
        ),
            
        rx.select(
            State.budget_scope_options.keys(),
            value=State.current_budget_scope,
            on_change=State.handle_budget_scope_change
        ),
            
        rx.select(
            State.travel_style_options.keys(),
            value=State.current_travel_style,
            on_change=State.handle_travel_style_change
        ),
            
        rx.select(
            State.pace_options.keys(),
            value=State.current_pace_option,
            on_change=State.handle_pace_change
        ),
            
        rx.text_area(
            placeholder="Any special occasions, accessibility needs, or preferences to add?",
            value=State.notes,
            on_change=State.set_notes
        ),
            
        rx.checkbox(
            "Flights",
            checked=State.include_flights,
            on_change=State.set_include_flights,
        ),
            
        rx.checkbox(
            "Hotels",
            checked=State.include_hotels,
            on_change=State.set_include_hotels,
        ),
            
        rx.heading("Interest Options", size= "7"),
            
        rx.foreach(
            State.INTEREST_OPTIONS,
            lambda interest: rx.hstack(
                rx.checkbox(
                    interest[0],
                    is_checked=State.selected_interests.contains(interest[1]),
                    on_change=lambda val: State.toggle_item(interest[1], val),
                ),
                padding_y="0.25em", # padding only applied to the top and bottom
            ),
        ),
            
        rx.heading("Restrictions", size= "7"),  
            
        rx.foreach(
            State.HARD_CONSTRAINT_OPTIONS,
            lambda constraint: rx.checkbox(
                constraint[0],
                is_checked=State.hard_constraints.contains(constraint[1]),
                on_change=lambda val: State.toggle_hard_constraint(constraint[1], val),
            )
        ),
            
        rx.heading("Preferences", size= "7"),  
            
        rx.foreach(
            State.SOFT_PREFERENCE_OPTIONS,
            lambda constraint: rx.checkbox(
                constraint[0],
                is_checked=State.soft_preferences.contains(constraint[1]),
                on_change=lambda val: State.toggle_soft_preference(constraint[1], val),
            ),
        ),
            
        rx.heading("Age", size="7"),
            
        rx.vstack(
            rx.input(
                type="number",
                value=State.current_traveler_age,
                on_change=State.set_current_traveler_age,
                placeholder="Enter age",
            ),
                
            rx.hstack(
                rx.icon_button(
                    rx.icon(
                        "plus",
                        color=rx.color("grass", 11),
                        size=14, # Slightly smaller icon size to fit neatly in row
                        stroke_width=2.5
                    ),
                            
                    background_color=rx.color("grass", 3),
                    radius="full",
                    width="28px",
                    height="28px",
                    on_click=lambda: State.add_traveler_age,
                    _hover={ "background_color": rx.color("grass", 4), "cursor": "pointer" },
                ),
                align="center",
                spacing="3",
            ),
                
            rx.foreach(
                State.traveler_ages,
                lambda age: rx.hstack(
                    rx.text(f"Age: {age}"),
                    rx.icon_button(
                        rx.icon(
                            "x",
                            color=rx.color("crimson", 11),
                            size=14, # Slightly smaller icon size to fit neatly in row
                            stroke_width=2.5
                        ),
                        background_color=rx.color("crimson", 3),
                        radius="full",
                        width="28px",
                        height="28px",
                        on_click=lambda: State.remove_traveler_age(age),
                        _hover={ "background_color": rx.color("crimson", 4), "cursor": "pointer" },
                    ),
                    align="center",
                    spacing="3",
                ),
            ),  
        ),
        
        rx.heading("Trip Details", size="7"),
        
        rx.vstack(
            rx.input(placeholder="City name", value=State.destination_city_name, on_change=State.set_destination_city_name()),

            rx.text("Departure Date", size="3"),
            
            rx.input(
                type="date",
                value=State.departure_date_str, 
                on_change=lambda val: State.set_departure_date(val),
                min=datetime.date.today().strftime("%Y-%m-%d"),
            ),
            
            rx.text("Arrival Date", size="3"),
                        
            rx.input(
                type="date",
                value=State.arrival_date_str, 
                on_change=lambda val: State.set_arrival_date(val),
                min=datetime.date.today().strftime("%Y-%m-%d"),
            ),
            
            rx.icon_button(
                rx.icon(
                    "plus",
                    color=rx.color("grass", 11),
                    size=14, # Slightly smaller icon size to fit neatly in row
                    stroke_width=2.5
                ),
                background_color=rx.color("grass", 3),
                radius="full",
                width="28px",
                height="28px",
                on_click=lambda: State.add_destination(),
                _hover={ "background_color": rx.color("grass", 4), "cursor": "pointer" },
            ),
            
            rx.foreach(
                State.destinations,
                lambda destination: rx.hstack(
                    rx.text(f"{destination.destination_city_name}: {destination.departure_date} -> {destination.arrival_date}"),
                    
                    rx.icon_button(
                        rx.icon(
                            "x",
                            color=rx.color("crimson", 11),
                            size=14, # Slightly smaller icon size to fit neatly in row
                            stroke_width=2.5
                        ),
                        background_color=rx.color("crimson", 3),
                        radius="full",
                        width="28px",
                        height="28px",
                        on_click=lambda: State.remove_destination(destination),
                        _hover={ "background_color": rx.color("crimson", 4), "cursor": "pointer" },
                    ),      
                ),
            ),
            
            rx.cond(
                State.destination_error != "",
                rx.text(State.destination_error, color=rx.color("crimson", 7)),
            ),
        ),
        

        
        spacing="5",
        padding="5"
    )


app = rx.App()
app.add_page(index)