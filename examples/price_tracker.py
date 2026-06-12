import os
import time

import requests


API_KEY = os.getenv("IGNAV_API_KEY", "YOUR_IGNAV_API_KEY")
BASE_URL = "https://ignav.com/api"
POLL_SECONDS = 300

SEARCH = {"origin": "SFO", "destination": "JFK", "departure_date": "2026-08-15", "market": "US"}


def cheapest_fare():
    response = requests.post(
        f"{BASE_URL}/fares/one-way",
        headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
        json=SEARCH,
        timeout=60,
    )
    response.raise_for_status()
    itineraries = response.json()["itineraries"]
    return min(itineraries, key=lambda item: item["price"]["amount"]) if itineraries else None


def fare_line(itinerary):
    price = itinerary["price"]
    segments = itinerary["outbound"]["segments"]
    first = segments[0]
    airline = itinerary["outbound"].get("carrier") or first["marketing_carrier_code"]
    return f'{price["currency"]} {price["amount"]} on {airline}, {len(segments) - 1} stop(s), departing {first["departure_time_local"]}'


def main():
    if API_KEY == "YOUR_IGNAV_API_KEY":
        raise SystemExit("Set IGNAV_API_KEY or edit API_KEY near the top of this file.")

    best_seen = None
    while True:
        fare = cheapest_fare()
        if fare is None:
            print("No matching fares right now.")
        elif best_seen is None or fare["price"]["amount"] < best_seen:
            best_seen = fare["price"]["amount"]
            print(f"New cheapest fare: {fare_line(fare)}")
        else:
            print(f"Still cheapest: {fare_line(fare)}")

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
