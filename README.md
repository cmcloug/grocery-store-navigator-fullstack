# 🛒 Grocery Store Navigator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-in%20development-orange)]()

Grocery Store Navigator connects to real Kroger store data. Give it a grocery list and a ZIP code, and it finds your items in a nearby store and orders them by aisle so you can walk one efficient pass through the store.

Use it from the terminal (CLI) or through the React web app.

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
│   ├── app.py               # Flask API used by the frontend
│   ├── kroger_api.py        # Kroger auth, store and product requests
│   ├── routing.py           # Pure aisle-ordering logic
│   ├── tests/               # pytest tests
│   ├── .env.example         # Template for API credentials
│   ├── requirements.txt
│   └── requirements-dev.txt
└── frontend/                # React + Vite web app
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

4. Or run the web app (two terminals):

   ```bash
   # terminal 1, in backend/
   python app.py
   # terminal 2, in frontend/
   npm install && npm run dev
   ```

   Then open http://localhost:5173.

5. Run the tests:

   ```bash
   pip install -r requirements-dev.txt
   pytest
   ```

## Roadmap

- Support other retailers (Walmart, Target)
- Mobile version with live store layout
- Smart recommendations and substitutions
