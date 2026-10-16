# 🛒 Grocery Store Navigator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-in%20development-orange)]()

Grocery Store Navigator connects to real Kroger store data. Give it a grocery list and a ZIP code, and it finds your items in a nearby store and orders them by aisle so you can walk one efficient pass through the store.

The frontend is still a work in progress. The backend is fully usable from the terminal.

## Features

- Read a grocery list from a text file (one item per line)
- Find nearby Kroger stores by ZIP code
- Look up each item with the Kroger API
- Print a route sorted by aisle, with items in the same aisle grouped together
- Report items that weren't found or have no aisle information

## Project structure

```
├── backend/
│   ├── main.py              # CLI entry point
│   ├── kroger_api.py        # Kroger auth, store and product requests
│   ├── routing.py           # Pure aisle-ordering logic
│   ├── tests/               # pytest tests
│   ├── .env.example         # Template for API credentials
│   ├── requirements.txt
│   └── requirements-dev.txt
└── frontend/                # React app (in development)
```

## Getting started

1. Get API credentials from the [Kroger developer portal](https://developer.kroger.com/).
2. Set up the backend:

   ```bash
   cd backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # then add your client ID and secret
   ```

3. Run it:

   ```bash
   python main.py --zip 46123 --list groceries.txt
   ```

   Both flags are optional: you'll be prompted for a ZIP code, and a default list is used if `--list` is omitted.

4. Run the tests:

   ```bash
   pip install -r requirements-dev.txt
   pytest
   ```

## Roadmap

- Connect the React frontend to the backend through an HTTP API
- Support other retailers (Walmart, Target)
- Mobile version with live store layout
- Smart recommendations and substitutions
