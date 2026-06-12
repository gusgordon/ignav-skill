# Ignav Skill

Official agent skill and examples for Ignav.

Ignav is a self-serve API for live flight prices and working booking links. The first 1,000 successful requests are free, then usage is $2.00 per 1,000 successful requests.

Links:

- [Docs](https://ignav.com/docs)
- [MCP server](https://ignav.com/docs/mcp)
- [Agent docs](https://ignav.com/docs/agents)
- [Playground](https://ignav.com/playground)

## Contents

- `SKILL.md` teaches agents the REST API flow: airport search, fare search, `ignav_id` booking links, errors, and booking URL handling.
- `examples/price_tracker.py` polls one route and prints when the cheapest fare drops.
- `examples/agent_tool.py` shows framework-neutral tool schemas and a small handler for LLM tool loops.
- `examples/mcp-configs/` has remote MCP setup snippets for Claude Code, Claude, and Cursor.

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
