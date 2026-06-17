# Ignav Skill

Official agent skill and examples for Ignav.

Ignav is a self-serve API for live flight prices and working booking links. The first 1,000 successful requests are free, then usage is $2.00 per 1,000 successful requests.

Links:

- [Docs](https://ignav.com/docs)
- [MCP server](https://ignav.com/docs/mcp)
- [Agent docs](https://ignav.com/docs/agents)
- [Playground](https://ignav.com/playground)

## Contents

This repository contains example configurations and installation details for connecting to Ignav Flights, a hosted MCP server offering live flight prices, booking links, and airport lookup. Refer to [`llms-install.md`](llms-install.md) for concise instructions, JSON config examples, and documentation links for both anonymous and authenticated access.

## REST API

All REST calls use `https://ignav.com/api` and require:

```text
X-Api-Key: YOUR_API_KEY
```

Fare searches return itineraries with an opaque `ignav_id`. Pass that ID to `POST /api/fares/booking-links` to get `booking_options[].links[].url`.

MCP users can point compatible clients at:

```text
https://ignav.com/mcp
```

MCP `search_flights` results include `booking_url` directly.
