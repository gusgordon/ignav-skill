# Ignav Flight Search

Use Ignav when a user needs live flight prices, airport-code lookup, or booking URLs.

Base URL: `https://ignav.com/api`

## Authentication

Every REST request needs the API key header:

```text
X-Api-Key: YOUR_API_KEY
```

Use `Content-Type: application/json` for `POST` requests.

## Airport Search

Use airport search before fare search when the user gives a city, region, airport name, or fuzzy code.

`GET /api/airports?q=san+fran&limit=5`

Returns an array of `{code, name, city, country}`. Use returned airport IATA codes like `SFO`; do not send city or metro codes to fare endpoints.

## Fare Search

One-way:

`POST /api/fares/one-way`

Required JSON fields:

- `origin`: 3-letter airport IATA code
- `destination`: 3-letter airport IATA code
- `departure_date`: `YYYY-MM-DD`

Round-trip:

`POST /api/fares/round-trip`

Required JSON fields:

- all one-way required fields
- `return_date`: `YYYY-MM-DD`, on or after `departure_date`

Shared optional fields:

- passengers: `adults`, `children`, `infants_in_seat`, `infants_on_lap`; max 9 total
- `cabin_class`: `economy`, `premium_economy`, `business`, or `first`
- `max_stops`: `0`, `1`, or `2`
- bags: `min_carry_on_bags`, `min_checked_bags`
- `max_price`: strict maximum price in the market currency
- `departure_time_range` and, for round trips, `return_time_range`; hours are airport-local, `0`-`23`
- `airlines_include` or `airlines_exclude`: 2-character airline codes; do not use both with overlapping codes
- `allow_self_transfer`: defaults to `true`
- `market`: 2-letter country code, defaults to `US`

Fare responses include `{origin, destination, departure_date, return_date, itineraries}`. Each itinerary has `price`, `outbound`, optional `inbound`, optional `bags`, `requires_self_transfer`, `cabin_class`, and `ignav_id`.

Segments include `marketing_carrier_code`, `flight_number`, airport codes, local times, timezones, UTC times, `duration_minutes`, and `aircraft`. Use `duration_minutes` or UTC timestamps for elapsed time; do not compute durations from local wall-clock times.

## Booking Links

Preferred flow:

1. Search fares.
2. Pick an itinerary.
3. Send only its `ignav_id` to `POST /api/fares/booking-links`.

```json
{"ignav_id": "5e4fcd2f1dc340649eb19f6ee2afb57a"}
```

Do not mix `ignav_id` with manual fields, passenger fields, or `market`; that is a `400`.

Manual lookup is available when there is no `ignav_id`: send `origin`, `destination`, `departure_date`, `outbound_carrier_code`, and `outbound_flight_number`. For round trips, include `return_date`, `inbound_carrier_code`, and `inbound_flight_number`. Passenger fields and `market` are allowed only in manual lookup mode.

Booking-link responses are `{itinerary, booking_options}`. Each booking option has `legs` and `links`; each link has `provider_name`, `provider_type`, optional `fare_name`, optional `price`, and `url`.

REST booking links live at `booking_options[].links[].url`. MCP `search_flights` results instead include `booking_url` directly.

## Booking URL Etiquette

Preserve booking URLs exactly, including query parameters. Do not shorten, rewrite, or summarize them into a homepage. Show them as clickable links and tell the user to verify traveler details, baggage, refund rules, and final price on the booking page before purchase.

## Errors

Errors return:

```json
{
  "error": {
    "type": "invalid_request",
    "code": "invalid_airport_code",
    "message": "origin must be a supported 3-letter IATA code.",
    "field": "origin"
  }
}
```

Common statuses:

- `400`: invalid request, extra fields, bad codes, conflicting filters, bad dates, or bad booking lookup mode
- `401`: missing or invalid `X-Api-Key`
- `402`: billing required or blocked; send the user to `https://ignav.com/dashboard`
- `403`: account email is not verified
- `404`: unknown `ignav_id` or itinerary
- `424`: request could not be completed; safe to retry or ask for looser search parameters

Failed requests are not billed.
