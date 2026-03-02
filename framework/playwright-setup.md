# Playwright MCP — Setup Guide

Playwright MCP allows Claude Code to drive a real browser, enabling it to read
job portals and career pages that return JavaScript shells to standard HTTP
requests (WebFetch). Without it, portals like LinkedIn, Oracle HCM, and many
enterprise ATS systems are unreadable.

Skills that fetch live URLs — `/scan-jobs`, `/review-cv`, `/voice-export`,
`/skill-gap` — use WebFetch by default and fall back to Playwright automatically
when a JS shell is detected, provided Playwright is configured.

---

## Prerequisites

- Node.js 18 or later
- npm (bundled with Node.js)

---

## Installation

```bash
# Install the Playwright MCP package
npm install -g @playwright/mcp

# Install the Chromium browser (used by default)
npx playwright install chromium
```

---

## Configuration

Add Playwright as an MCP server in your Claude Code settings.

**Option 1: Edit `.claude/settings.json` directly**

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Option 2: Via Claude Code MCP settings UI**

Open Claude Code settings → MCP Servers → Add Server:
- Name: `playwright`
- Command: `npx`
- Args: `@playwright/mcp@latest`

Restart Claude Code after adding the server.

---

## Verify It Is Working

Run any skill that fetches a live URL:

```
/scan-jobs linkedin.com "CTO" remote
```

If Playwright is configured, Claude will use it automatically when WebFetch
returns a JS shell. You will see a note in the output indicating which fetch
method was used.

---

## Which Portals Require Playwright

| Portal | Requires Playwright |
|---|---|
| LinkedIn Jobs | Yes — always JS-rendered |
| Oracle HCM (company career portals) | Yes |
| Greenhouse, Lever, Workday | Usually |
| Taleo, iCIMS | Usually |
| Indeed (public search) | No — works with WebFetch |
| Upwork | No — works with WebFetch |
| Most public job board listing pages | No |

If a portal requires login, Playwright can navigate to it but will stop at the
login wall. In that case, paste the job description text directly instead.

---

## Headless vs. Headed Mode

By default, Playwright MCP runs headless (no visible browser window). If you
need to handle login flows or CAPTCHAs manually, you can run it in headed mode:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headed"]
    }
  }
}
```
