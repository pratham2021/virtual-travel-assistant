import reflex as rx
from rxconfig import config

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
        "Total trip budget": "total_trip",
        "Budget per day": "per_day",
    }
    
    travel_style_options = {
        "Backpacking": "backpacking",
        "Mid-range": "mid_range",
        "Luxury": "luxury",
    }
    
    pace_options = {
        "Relaxed": "relaxed",
        "Moderate": "moderate",
        "Packed": "packed",
    }
    
    traveler_type: str = "solo" # ["solo", "couple", "family_with_kids", "friend_group"]
    budget_scope: str = "total_trip" # ["total_trip", "per_day"]
    travel_style: str = "mid_range" # ["backpacking", "mid_range", "luxury"]
    pace: str = "moderate" # ["relaxed", "moderate", "packed"]
    
    include_flights: bool = False
    include_hotels: bool = False
    
    interests: list[str] = []
    
    hard_constraints: list[str] = []
    soft_preferences: list[str] = []
    
    traveler_ages: list[int] = []
    destinations: list = []
    
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
    
    # Format currencies
    @rx.var
    def formatted_currencies(self) -> list[str]:
        return [f"{currency_abbreviation} - {currency_name}" for currency_abbreviation, currency_name in self.currency_options.items()]
    
    def handle_currency_option_change(self, selected_formatted_string: str):
        self.budget_currency = selected_formatted_string.split(" - ")[0]
    
    def handle_traveler_type_change(self, traveler_type_option: str):
        self.traveler_type = self.traveler_type_options[traveler_type_option]
    
    def handle_budget_scope_change(self, budget_scope_option: str):
        self.budget_scope = self.budget_scope_options[budget_scope_option]
    
    def handle_travel_style_change(self, travel_style_option: str):
        self.travel_style = self.travel_style_options[self.travel_style_options]
    
    def handle_pace_change(self, pace_option: str):
        self.pace = self.pace_options[pace_option]

            
def index() -> rx.Component:
    current_currency = f"{State.budget_currency} - {State.currency_options[State.budget_currency]}"
    
    return rx.vstack(
        rx.heading("Plan Your Trip", size="9"),
        
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
            value=State.traveler_type, # A state variable bound to the currently selected option
            on_change=State.handle_traveler_type_change # What happens when the user selects a different option from the dropdown, manipulating the state variable.
        ),
        
        rx.select(
            State.budget_scope_options.keys(),
            value=State.budget_scope,
            on_change=State.handle_budget_scope_change
        ),
        
        rx.select(
            State.travel_style_options.keys(),
            value=State.travel_style,
            on_change=State.handle_travel_style_change
        ),
        
        rx.select(
            State.pace_options.keys(),
            value=State.pace,
            on_change=State.handle_pace_change
        ),
        
        rx.text_area(
            placeholder="Any special occasions, accessibility needs, or preferences to add?",
            value=State.notes,
            on_change=State.set_notes
        ),
                
        spacing="5",
        padding="5"
    )

app = rx.App()
app.add_page(index)
