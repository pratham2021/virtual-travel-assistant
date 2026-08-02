import asyncio
import datetime
from pydantic import BaseModel
import reflex as rx
from rxconfig import config
import requests


class Activity(BaseModel):
    start_time: str = ""
    duration_minutes: int = 0
    end_time: str = ""
    name: str = ""
    category: str = ""
    description: str = ""
    estimated_cost: int = 0


class Day(BaseModel):
    city: str = ""
    day_date: str = ""
    theme: str = ""
    activities: list[Activity] = []


class Destination(BaseModel):
    destination_city_name: str = ""
    departure_date: datetime.date = datetime.date.today()
    arrival_date: datetime.date = datetime.date.today()


class State(rx.State):
    origin: str = ""
    group_size: int = 1
    budget_amount: float = 1000.0

    currency_options: dict[str, str] = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "GBP": "British Pound",
        "JPY": "Japanese Yen",
        "CHF": "Swiss Franc",
        "CAD": "Canadian Dollar",
        "AUD": "Australian Dollar",
        "NZD": "New Zealand Dollar",
        "CNY": "Chinese Yuan",
        "HKD": "Hong Kong Dollar",
        "SGD": "Singapore Dollar",
        "INR": "Indian Rupee",
        "KRW": "South Korean Won",
        "THB": "Thai Baht",
        "MYR": "Malaysian Ringgit",
        "IDR": "Indonesian Rupiah",
        "PHP": "Philippine Peso",
        "VND": "Vietnamese Dong",
        "TWD": "Taiwan Dollar",
        "PKR": "Pakistani Rupee",
        "BDT": "Bangladeshi Taka",
        "LKR": "Sri Lankan Rupee",
        "NPR": "Nepalese Rupee",
        "MMK": "Myanmar Kyat",
        "KHR": "Cambodian Riel",
        "LAK": "Lao Kip",
        "BND": "Brunei Dollar",
        "MOP": "Macanese Pataca",
        "MNT": "Mongolian Tugrik",
        "AED": "UAE Dirham",
        "SAR": "Saudi Riyal",
        "QAR": "Qatari Riyal",
        "KWD": "Kuwaiti Dinar",
        "BHD": "Bahraini Dinar",
        "OMR": "Omani Rial",
        "JOD": "Jordanian Dinar",
        "ILS": "Israeli Shekel",
        "TRY": "Turkish Lira",
        "EGP": "Egyptian Pound",
        "MAD": "Moroccan Dirham",
        "TND": "Tunisian Dinar",
        "DZD": "Algerian Dinar",
        "LYD": "Libyan Dinar",
        "SDG": "Sudanese Pound",
        "NGN": "Nigerian Naira",
        "GHS": "Ghanaian Cedi",
        "KES": "Kenyan Shilling",
        "TZS": "Tanzanian Shilling",
        "UGX": "Ugandan Shilling",
        "ZAR": "South African Rand",
        "ETB": "Ethiopian Birr",
        "XOF": "West African CFA Franc",
        "XAF": "Central African CFA Franc",
        "RWF": "Rwandan Franc",
        "BIF": "Burundian Franc",
        "CDF": "Congolese Franc",
        "GNF": "Guinean Franc",
        "SLL": "Sierra Leonean Leone",
        "LRD": "Liberian Dollar",
        "GMD": "Gambian Dalasi",
        "CVE": "Cape Verdean Escudo",
        "STN": "Sao Tome Dobra",
        "AOA": "Angolan Kwanza",
        "ZMW": "Zambian Kwacha",
        "MWK": "Malawian Kwacha",
        "MZN": "Mozambican Metical",
        "BWP": "Botswana Pula",
        "NAD": "Namibian Dollar",
        "SZL": "Swazi Lilangeni",
        "LSL": "Lesotho Loti",
        "MUR": "Mauritian Rupee",
        "SCR": "Seychellois Rupee",
        "MGA": "Malagasy Ariary",
        "KMF": "Comorian Franc",
        "DJF": "Djiboutian Franc",
        "SOS": "Somali Shilling",
        "ERN": "Eritrean Nakfa",
        "SSP": "South Sudanese Pound",
        "MXN": "Mexican Peso",
        "BRL": "Brazilian Real",
        "ARS": "Argentine Peso",
        "CLP": "Chilean Peso",
        "COP": "Colombian Peso",
        "PEN": "Peruvian Sol",
        "UYU": "Uruguayan Peso",
        "PYG": "Paraguayan Guarani",
        "BOB": "Bolivian Boliviano",
        "VES": "Venezuelan Bolivar",
        "GYD": "Guyanese Dollar",
        "SRD": "Surinamese Dollar",
        "GTQ": "Guatemalan Quetzal",
        "HNL": "Honduran Lempira",
        "NIO": "Nicaraguan Cordoba",
        "CRC": "Costa Rican Colon",
        "PAB": "Panamanian Balboa",
        "DOP": "Dominican Peso",
        "JMD": "Jamaican Dollar",
        "TTD": "Trinidad and Tobago Dollar",
        "BBD": "Barbadian Dollar",
        "BSD": "Bahamian Dollar",
        "BZD": "Belize Dollar",
        "XCD": "East Caribbean Dollar",
        "HTG": "Haitian Gourde",
        "CUP": "Cuban Peso",
        "AWG": "Aruban Florin",
        "ANG": "Netherlands Antillean Guilder",
        "KYD": "Cayman Islands Dollar",
        "BMD": "Bermudian Dollar",
        "PLN": "Polish Zloty",
        "CZK": "Czech Koruna",
        "HUF": "Hungarian Forint",
        "RON": "Romanian Leu",
        "BGN": "Bulgarian Lev",
        "RSD": "Serbian Dinar",
        "UAH": "Ukrainian Hryvnia",
        "RUB": "Russian Ruble",
        "BYN": "Belarusian Ruble",
        "GEL": "Georgian Lari",
        "AMD": "Armenian Dram",
        "AZN": "Azerbaijani Manat",
        "KZT": "Kazakhstani Tenge",
        "UZS": "Uzbekistani Som",
        "TJS": "Tajikistani Somoni",
        "KGS": "Kyrgyzstani Som",
        "TMT": "Turkmenistani Manat",
        "MDL": "Moldovan Leu",
        "ALL": "Albanian Lek",
        "MKD": "Macedonian Denar",
        "BAM": "Bosnia-Herzegovina Mark",
        "ISK": "Icelandic Krona",
        "NOK": "Norwegian Krone",
        "SEK": "Swedish Krona",
        "DKK": "Danish Krone",
        "FJD": "Fijian Dollar",
        "PGK": "Papua New Guinean Kina",
        "SBD": "Solomon Islands Dollar",
        "TOP": "Tongan Pa'anga",
        "VUV": "Vanuatu Vatu",
        "WST": "Samoan Tala",
        "XPF": "CFP Franc",
        "AFN": "Afghan Afghani",
        "IRR": "Iranian Rial",
        "IQD": "Iraqi Dinar",
        "SYP": "Syrian Pound",
        "LBP": "Lebanese Pound",
        "YER": "Yemeni Rial",
        "BTN": "Bhutanese Ngultrum",
        "MVR": "Maldivian Rufiyaa",
        "KPW": "North Korean Won",
    }

    CURRENCY_SYMBOLS: dict[str, str] = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CHF": "CHF",
        "CAD": "$",
        "AUD": "$",
        "NZD": "$",
        "CNY": "¥",
        "HKD": "$",
        "SGD": "$",
        "INR": "₹",
        "KRW": "₩",
        "THB": "฿",
        "MYR": "RM",
        "IDR": "Rp",
        "PHP": "₱",
        "VND": "₫",
        "TWD": "NT$",
        "PKR": "₨",
        "BDT": "৳",
        "LKR": "₨",
        "NPR": "₨",
        "MMK": "K",
        "KHR": "៛",
        "LAK": "₭",
        "BND": "$",
        "MOP": "MOP$",
        "MNT": "₮",
        "AED": "د.إ",
        "SAR": "﷼",
        "QAR": "﷼",
        "KWD": "د.ك",
        "BHD": ".د.ب",
        "OMR": "﷼",
        "JOD": "د.ا",
        "ILS": "₪",
        "TRY": "₺",
        "EGP": "£",
        "MAD": "د.م.",
        "TND": "د.ت",
        "DZD": "د.ج",
        "LYD": "ل.د",
        "SDG": "ج.س.",
        "NGN": "₦",
        "GHS": "₵",
        "KES": "KSh",
        "TZS": "TSh",
        "UGX": "USh",
        "ZAR": "R",
        "ETB": "Br",
        "XOF": "CFA",
        "XAF": "FCFA",
        "RWF": "FRw",
        "BIF": "FBu",
        "CDF": "FC",
        "GNF": "FG",
        "SLL": "Le",
        "LRD": "$",
        "GMD": "D",
        "CVE": "$",
        "STN": "Db",
        "AOA": "Kz",
        "ZMW": "ZK",
        "MWK": "MK",
        "MZN": "MT",
        "BWP": "P",
        "NAD": "$",
        "SZL": "L",
        "LSL": "L",
        "MUR": "₨",
        "SCR": "₨",
        "MGA": "Ar",
        "KMF": "CF",
        "DJF": "Fdj",
        "SOS": "S",
        "ERN": "Nfk",
        "SSP": "£",
        "MXN": "$",
        "BRL": "R$",
        "ARS": "$",
        "CLP": "$",
        "COP": "$",
        "PEN": "S/",
        "UYU": "$",
        "PYG": "₲",
        "BOB": "Bs.",
        "VES": "Bs.",
        "GYD": "$",
        "SRD": "$",
        "GTQ": "Q",
        "HNL": "L",
        "NIO": "C$",
        "CRC": "₡",
        "PAB": "B/.",
        "DOP": "RD$",
        "JMD": "$",
        "TTD": "$",
        "BBD": "$",
        "BSD": "$",
        "BZD": "$",
        "XCD": "$",
        "HTG": "G",
        "CUP": "$",
        "AWG": "ƒ",
        "ANG": "ƒ",
        "KYD": "$",
        "BMD": "$",
        "PLN": "zł",
        "CZK": "Kč",
        "HUF": "Ft",
        "RON": "lei",
        "BGN": "лв",
        "RSD": "дин.",
        "UAH": "₴",
        "RUB": "₽",
        "BYN": "Br",
        "GEL": "₾",
        "AMD": "֏",
        "AZN": "₼",
        "KZT": "₸",
        "UZS": "so'm",
        "TJS": "SM",
        "KGS": "с",
        "TMT": "m",
        "MDL": "L",
        "ALL": "L",
        "MKD": "ден",
        "BAM": "KM",
        "ISK": "kr",
        "NOK": "kr",
        "SEK": "kr",
        "DKK": "kr",
        "FJD": "$",
        "PGK": "K",
        "SBD": "$",
        "TOP": "T$",
        "VUV": "VT",
        "WST": "T",
        "XPF": "₣",
        "AFN": "؋",
        "IRR": "﷼",
        "IQD": "ع.د",
        "SYP": "£",
        "LBP": "ل.ل",
        "YER": "﷼",
        "BTN": "Nu.",
        "MVR": "Rf",
        "KPW": "₩",
    }

    budget_currency: str = "USD"
    itinerary_currency_symbol: str = ""
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

    traveler_type: str = (
        "solo"  # ["solo", "couple", "family_with_kids", "friend_group"]
    )
    budget_scope: str = "total_trip"  # ["total_trip", "per_day"]
    travel_style: str = "mid_range"  # ["backpacking", "mid_range", "luxury"]
    pace: str = "moderate"  # ["relaxed", "moderate", "packed"]

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

    job_id: str = ""
    is_submitting: bool = False
    submission_error: str = ""

    itinerary_status: str = ""
    itinerary_result: dict = {}
    itinerary_days: list[Day] = []
    polling_error: str = ""
    itinerary_by_city: dict[str, list[Day]] = {}

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
            if self.arrival_date and parsed_datetime.date() >= self.arrival_date:
                # make sure it's not after arrival date
                return
            self.departure_date = parsed_datetime.date()
        else:
            self.departure_date = None

    def set_arrival_date(self, date_string):
        if date_string:
            parsed_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            if self.departure_date and parsed_datetime.date() <= self.departure_date:
                # make sure it's not before departure date
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
        return [
            f"{currency_abbreviation} - {currency_name}"
            for currency_abbreviation, currency_name in self.currency_options.items()
        ]

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

        new_destination = Destination(
            destination_city_name=cleaned_destination,
            departure_date=self.departure_date,
            arrival_date=self.arrival_date,
        )

        self.destinations.append(new_destination)
        self.destination_city_name = ""
        self.departure_date = None
        self.arrival_date = None
        self.destination_error = ""

    def remove_destination(self, destination: Destination):
        if destination in self.destinations:
            self.destinations.remove(destination)

    def build_preference_payload(self):
        converted_destinations = []
        for destination in self.destinations:
            destination_dictionary = {
                "city": destination.destination_city_name,
                "departure_date": destination.arrival_date.strftime("%Y-%m-%d"),
                "arrival_date": destination.departure_date.strftime("%Y-%m-%d"),
            }
            converted_destinations.append(destination_dictionary)

        payload = {
            "origin": self.origin,
            "destinations": converted_destinations,
            "group_size": self.group_size,
            "traveler_type": self.traveler_type,
            "budget_amount": self.budget_amount,
            "budget_scope": self.budget_scope,
            "budget_currency": self.budget_currency,
            "travel_style": self.travel_style,
            "pace": self.pace,
            "interests": self.selected_interests,
            "hard_constraints": self.hard_constraints,
            "soft_preferences": self.soft_preferences,
            "traveler_ages": self.traveler_ages,
            "include_flights": self.include_flights,
            "include_hotels": self.include_hotels,
            "notes": self.notes,
        }

        return payload

    async def poll_for_result(self):
        max_attempts = 100
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                response = requests.get(
                    f"http://127.0.0.1:8000/generate-itinerary/{self.job_id}"
                )

                result = response.json()
                self.itinerary_status = result.get("status", None)

                if self.itinerary_status is None:
                    self.polling_error = (
                        "Received an unexpected response while checking your itinerary."
                    )
                    return

                if response.status_code not in [200, 201]:
                    self.polling_error = (
                        "Something went wrong checking your itinerary's status."
                    )
                    return
            except requests.exceptions.RequestException as requestE:
                self.polling_error = (
                    "Something went wrong checking your itinerary's status."
                )
                return

            if self.itinerary_status == "complete":
                self.itinerary_result = result["result"]
                raw_days = self.itinerary_result.get("days", [])
                self.itinerary_currency_symbol = self.CURRENCY_SYMBOLS[
                    self.itinerary_result.get("budget_currency", "USD")
                ]
                self.itinerary_days = [Day(**day) for day in raw_days]
                for i in range(len(self.itinerary_days)):
                    self.itinerary_days[i].day_date = datetime.datetime.strptime(
                        self.itinerary_days[i].day_date, "%Y-%m-%d"
                    ).strftime("%B %d, %Y")
                    for j in range(len(self.itinerary_days[i].activities)):
                        parsed_start = datetime.datetime.strptime(
                            self.itinerary_days[i].activities[j].start_time, "%H:%M:%S"
                        )
                        duration_span = datetime.timedelta(
                            minutes=self.itinerary_days[i]
                            .activities[j]
                            .duration_minutes
                        )
                        calculated_end = parsed_start + duration_span
                        self.itinerary_days[i].activities[j].start_time = (
                            parsed_start.strftime("%-I:%M %p")
                        )
                        self.itinerary_days[i].activities[j].end_time = (
                            calculated_end.strftime("%-I:%M %p")
                        )

                itinerary_by_city = {}
                for day in self.itinerary_days:
                    if day.city not in itinerary_by_city:
                        itinerary_by_city[day.city] = []
                    itinerary_by_city[day.city].append(day)

                self.itinerary_by_city = itinerary_by_city
                return

            if self.itinerary_status == "failed":
                self.polling_error = result["error"]
                return

            yield
            await asyncio.sleep(3)
            current_attempt += 1
        self.polling_error = (
            "This is taking longer than expected. Please check back later."
        )

    async def submit_form(self):
        # Check 1: Origin
        self.polling_error = ""
        stripped_origin = self.origin.strip()

        if len(stripped_origin) < 2:
            self.submission_error = (
                "Please enter a valid origin city (at least 2 characters)."
            )
            return

        # Check 2: Destinations
        if len(self.destinations) == 0:
            self.submission_error = "Please add at least one destination."
            return

        if len(self.destinations) > 10:
            self.submission_error = (
                "Please limit your trip to 10 destinations or fewer."
            )
            return

        # Check 3: Budget amount (has to be at least 50 bucks.)
        if self.budget_amount < 50:
            self.submission_error = (
                "Please enter a budget of at least 50 (in your selected currency)."
            )
            return

        # Check 4: Traveler ages required for families, and must match group size
        if self.traveler_type == "family_with_kids":
            if len(self.traveler_ages) == 0:
                self.submission_error = (
                    "Please add an age for each traveler in your family."
                )
                return
            if len(self.traveler_ages) != self.group_size:
                self.submission_error = (
                    f"There must be exactly {self.group_size} travelers."
                )
                return
            elif (
                len(self.traveler_ages) > 0
                and len(self.traveler_ages) != self.group_size
            ):
                self.submission_error = (
                    f"There must be exactly {self.group_size} travelers."
                )
                return

        # Check 5: Traveler type and group size consistency
        if self.traveler_type == "solo" and self.group_size != 1:
            self.submission_error = "There must be one traveler."
            return
        if self.traveler_type == "couple" and self.group_size != 2:
            self.submission_error = "Couples must have two travelers."
            return
        if (
            self.traveler_type == "family_with_kids"
            or self.traveler_type == "friend_group"
        ) and self.group_size < 2:
            self.submission_error = "There must be at least two travelers."
            return

        # Check 6: At least one interest
        if not self.selected_interests:
            self.submission_error = "Please select at least one interest."
            return

        self.submission_error = ""
        self.is_submitting = True
        yield

        payload = self.build_preference_payload()

        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate-itinerary", json=payload
            )

            print(response.json())

            if response.status_code in [200, 201]:
                result = response.json()
                self.job_id = result["job_id"]
                self.submission_error = ""
                async for _ in self.poll_for_result():
                    pass
            else:
                self.submission_error = (
                    "Something went wrong on our end. Please try again in a moment."
                )
        except requests.exceptions.RequestException as requestE:
            self.submission_error = "We couldn't connect to the server. Please check your internet connection and try again."
        except requests.exceptions.Timeout as timeoutE:
            self.submission_error = "Our servers took too long to respond. Please check your internet connection and try again"
        except requests.exceptions.ConnectionError as connectionError:
            self.submission_error = "Can't connect to servers. Please check your Wi-Fi or cellular data connection."
        except requests.exceptions.HTTPError as httpE:
            self.submission_error = (
                "The server returned an invalid response. Please try again later."
            )
        finally:
            self.is_submitting = False


def index() -> rx.Component:
    current_currency = (
        f"{State.budget_currency} - {State.currency_options[State.budget_currency]}"
    )

    return rx.center(
        rx.container(
            rx.vstack(
                rx.heading("Plan Your Trip", size="8", margin_bottom="0.5em"),
                rx.vstack(
                    rx.heading("Trip Basics", size="6"),
                    rx.input(
                        placeholder="Origin",
                        value=State.origin,
                        on_change=State.set_origin,
                    ),
                    rx.input(
                        type="number",
                        value=State.group_size,
                        on_change=State.set_group_size,
                        placeholder="1",
                    ),
                    rx.select(
                        State.traveler_type_options.keys(),  # A list of strings or values that populate the choices in the dropdown menu.
                        value=State.current_traveler_type,  # A state variable bound to the currently selected option
                        on_change=State.handle_traveler_type_change,  # What happens when the user selects a different option from the dropdown, manipulating the state variable.
                    ),
                    spacing="4",
                    align="center",
                ),
                rx.divider(),
                rx.vstack(
                    rx.heading("Budget", size="6"),
                    rx.select(
                        State.formatted_currencies,  # A list of strings or values that populate the choices in the dropdown menu.
                        value=current_currency,  # A state variable bound to the currently selected option
                        on_change=State.handle_currency_option_change,  # What happens when the user selects a different option from the dropdown, manipulating the state variable.
                    ),
                    rx.input(
                        type="number",
                        value=State.budget_amount,
                        step=0.01,
                        on_change=State.set_budget_amount,
                    ),
                    rx.select(
                        State.budget_scope_options.keys(),
                        value=State.current_budget_scope,
                        on_change=State.handle_budget_scope_change,
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.vstack(
                    rx.heading("Style & Pace", size="6"),
                    rx.select(
                        State.travel_style_options.keys(),
                        value=State.current_travel_style,
                        on_change=State.handle_travel_style_change,
                    ),
                    rx.select(
                        State.pace_options.keys(),
                        value=State.current_pace_option,
                        on_change=State.handle_pace_change,
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.vstack(
                    rx.heading("Extras", size="6"),
                    rx.text_area(
                        placeholder="Any special occasions, accessibility needs, or preferences to add?",
                        value=State.notes,
                        on_change=State.set_notes,
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
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.heading("Interests", size="6"),
                rx.grid(
                    rx.foreach(
                        State.INTEREST_OPTIONS,
                        lambda interest: rx.hstack(
                            rx.checkbox(
                                interest[0],
                                is_checked=State.selected_interests.contains(
                                    interest[1]
                                ),
                                on_change=lambda val: State.toggle_item(
                                    interest[1], val
                                ),
                            ),
                            padding_y="0.25em",  # padding only applied to the top and bottom
                        ),
                    ),
                    columns="2",
                    spacing="3",
                    row_gap="3",
                    column_gap="6",
                    max_width="80%",
                    margin="0 8% 0 12%",
                    template_columns="1fr 1fr",
                ),
                rx.divider(),
                rx.heading("Restrictions & Preferences", size="6"),
                rx.grid(
                    rx.foreach(
                        State.HARD_CONSTRAINT_OPTIONS,
                        lambda constraint: rx.checkbox(
                            constraint[0],
                            is_checked=State.hard_constraints.contains(constraint[1]),
                            on_change=lambda val: State.toggle_hard_constraint(
                                constraint[1], val
                            ),
                        ),
                    ),
                    rx.foreach(
                        State.SOFT_PREFERENCE_OPTIONS,
                        lambda constraint: rx.checkbox(
                            constraint[0],
                            is_checked=State.soft_preferences.contains(constraint[1]),
                            on_change=lambda val: State.toggle_soft_preference(
                                constraint[1], val
                            ),
                        ),
                    ),
                    columns="2",
                    spacing="3",
                    row_gap="3",
                    column_gap="6",
                    max_width="80%",
                    margin="0 8% 0 18%",
                    template_columns="1fr 1fr",
                ),
                rx.divider(),
                rx.vstack(
                    rx.heading("Traveler Ages", size="6"),
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
                                size=14,  # Slightly smaller icon size to fit neatly in row
                                stroke_width=2.5,
                            ),
                            background_color=rx.color("grass", 3),
                            radius="full",
                            width="28px",
                            height="28px",
                            on_click=State.add_traveler_age,
                            _hover={
                                "background_color": rx.color("grass", 4),
                                "cursor": "pointer",
                            },
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
                                    size=14,  # Slightly smaller icon size to fit neatly in row
                                    stroke_width=2.5,
                                ),
                                background_color=rx.color("crimson", 3),
                                radius="full",
                                width="28px",
                                height="28px",
                                on_click=lambda: State.remove_traveler_age(age),
                                _hover={
                                    "background_color": rx.color("crimson", 4),
                                    "cursor": "pointer",
                                },
                            ),
                            align="center",
                            spacing="3",
                        ),
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.heading("Trip Details", size="6"),
                rx.vstack(
                    rx.input(
                        placeholder="City name",
                        value=State.destination_city_name,
                        on_change=State.set_destination_city_name,
                    ),
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
                    rx.hstack(
                        rx.icon_button(
                            rx.icon(
                                "plus",
                                color=rx.color("grass", 11),
                                size=14,  # Slightly smaller icon size to fit neatly in row
                                stroke_width=2.5,
                            ),
                            background_color=rx.color("grass", 3),
                            radius="full",
                            width="28px",
                            height="28px",
                            on_click=lambda: State.add_destination(),
                            _hover={
                                "background_color": rx.color("grass", 4),
                                "cursor": "pointer",
                            },
                        ),
                        spacing="3",
                        align="center",
                    ),
                    rx.foreach(
                        State.destinations,
                        lambda destination: rx.hstack(
                            rx.text(
                                f"{destination.destination_city_name}: {destination.departure_date} -> {destination.arrival_date}"
                            ),
                            rx.icon_button(
                                rx.icon(
                                    "x",
                                    color=rx.color("crimson", 11),
                                    size=14,  # Slightly smaller icon size to fit neatly in row
                                    stroke_width=2.5,
                                ),
                                background_color=rx.color("crimson", 3),
                                radius="full",
                                width="28px",
                                height="28px",
                                on_click=lambda: State.remove_destination(destination),
                                _hover={
                                    "background_color": rx.color("crimson", 4),
                                    "cursor": "pointer",
                                },
                            ),
                        ),
                    ),
                    align="center",
                    spacing="4",
                ),
                rx.divider(),
                rx.button(
                    rx.cond(State.is_submitting, "Submitting...", "Generate Itinerary"),
                    on_click=State.submit_form,
                    disabled=State.is_submitting,
                ),
                rx.cond(
                    State.is_submitting
                    | (State.itinerary_status == "running")
                    | (State.itinerary_status == "pending"),
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("Generating your itinerary... this may take a minute."),
                        align="center",
                        spacing="3",
                    ),
                ),
                rx.cond(
                    State.submission_error != "",
                    rx.text(State.submission_error, color=rx.color("crimson", 7)),
                ),
                rx.cond(
                    State.polling_error != "",
                    rx.text(State.polling_error, color=rx.color("crimson", 7)),
                ),
                rx.cond(
                    State.itinerary_result.length() != 0,
                    rx.vstack(
                        rx.heading("Your Itinerary", size="7"),
                        rx.heading(
                            f"Origin: {State.itinerary_result['origin']}", size="6"
                        ),
                        rx.heading(
                            f"Total Cost: {State.itinerary_result['total_estimated_cost']} {State.itinerary_result['budget_currency']}",
                            size="6",
                        ),
                        rx.heading(
                            f"Note: {State.itinerary_result['cost_disclaimer']}",
                            size="3",
                        ),
                        rx.foreach(
                            State.itinerary_by_city,
                            lambda city_entry: rx.vstack(
                                rx.heading(f"{city_entry[0]}", size="6"),
                                rx.foreach(
                                    city_entry[1],
                                    lambda day: rx.vstack(
                                        rx.heading(f"{day.day_date}", size="4"),
                                        rx.vstack(
                                            rx.heading(
                                                f"Theme: {day.theme}",
                                                font_style="italic",
                                                color=rx.color("gray", 9),
                                            ),
                                            rx.vstack(
                                                rx.foreach(
                                                    day.activities,
                                                    lambda activity: rx.vstack(
                                                        rx.cond(
                                                            activity.estimated_cost
                                                            == 0,
                                                            rx.text(
                                                                f"{activity.start_time} - {activity.end_time}: {activity.name} - Free",
                                                                font_style="italic",
                                                                color=rx.color(
                                                                    "gray", 9
                                                                ),
                                                            ),
                                                            rx.text(
                                                                f"{activity.start_time} - {activity.end_time}: {activity.name} - {State.itinerary_currency_symbol}{activity.estimated_cost}",
                                                                font_style="italic",
                                                                color=rx.color(
                                                                    "gray", 9
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                                padding_left="3em",
                                            ),
                                            padding_left="3em",
                                        ),
                                        padding_left="3em",
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                spacing="5",
                padding="0.5em",  # inner space is twice the current element's font size
                width="100%",
                align="center",
            ),
        ),
        width="100%",
    )


app = rx.App()
app.add_page(index)


# Next steps
# 1. Test the full submission flow end-to-end - with your backend server actually running, fill out the form completely and click submit;
# confirm you get a job_id back with no errors
# 2. Polling logic - once job_id is set, repeatedly check /generate-itinerary/{job_id} until the itinerary is "complete" or "failed"
# 3. Results display - rendering the finished itinerary once polling succeeds
