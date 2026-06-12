import os

import requests


API_KEY = os.getenv("IGNAV_API_KEY", "YOUR_IGNAV_API_KEY")
BASE_URL = "https://ignav.com/api"

IGNAV_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ignav_search_flights",
            "description": "Search live one-way or round-trip flight prices.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "trip_type": {"type": "string", "enum": ["one_way", "round_trip"]},
                    "origin": {"type": "string", "description": "3-letter airport IATA code"},
                    "destination": {"type": "string", "description": "3-letter airport IATA code"},
                    "departure_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "return_date": {"type": "string", "description": "YYYY-MM-DD for round trips"},
                    "adults": {"type": "integer", "minimum": 1, "default": 1},
                    "cabin_class": {
                        "type": "string",
                        "enum": ["economy", "premium_economy", "business", "first"],
                        "default": "economy",
                    },
                    "max_stops": {"type": "integer", "minimum": 0, "maximum": 2},
                    "market": {"type": "string", "default": "US"},
                },
                "required": ["trip_type", "origin", "destination", "departure_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ignav_get_booking_links",
            "description": "Get booking links for a fare-search itinerary by ignav_id.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "ignav_id": {"type": "string"},
                },
                "required": ["ignav_id"],
            },
        },
    },
]


def post_json(path, payload, api_key=API_KEY):
    response = requests.post(
        f"{BASE_URL}{path}",
        headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def handle_ignav_tool(name, arguments, api_key=API_KEY):
    if name == "ignav_search_flights":
        payload = dict(arguments)
        trip_type = payload.pop("trip_type")
        path = "/fares/round-trip" if trip_type == "round_trip" else "/fares/one-way"
        return post_json(path, payload, api_key)

    if name == "ignav_get_booking_links":
        return post_json("/fares/booking-links", {"ignav_id": arguments["ignav_id"]}, api_key)

    raise ValueError(f"Unknown Ignav tool: {name}")


# In your LLM loop:
# 1. Register IGNAV_TOOLS with the model.
# 2. When the model calls one, pass the tool name and parsed JSON arguments here.
# 3. Return this JSON to the model as the tool result.
# 4. For REST booking links, show booking_options[].links[].url exactly.
