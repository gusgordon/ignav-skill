# llms-install.md

Ignav Flights is a hosted MCP server providing live flight prices, booking links, and airport lookup via Streamable HTTP at `https://ignav.com/mcp`.

- **Anonymous testing**: Available without signup (rate-limited).
- **Authenticated usage**: Use an API key via the `X-Api-Key` header. [Sign up](https://ignav.com/signup) and view your key on the [dashboard](https://ignav.com/dashboard).

**Anonymous JSON config example:**

```json
{
  "type": "streamable-http",
  "url": "https://ignav.com/mcp"
}
```

**API Key JSON config example:**

```json
{
  "type": "streamable-http",
  "url": "https://ignav.com/mcp",
  "headers": {
    "X-Api-Key": "YOUR_API_KEY"
  }
}
```

- **MCP docs**: [ignav.com/docs/mcp](https://ignav.com/docs/mcp)
- **REST docs**: [ignav.com/docs](https://ignav.com/docs)
- **Source/examples**: [github.com/gusgordon/ignav-skill](https://github.com/gusgordon/ignav-skill)
