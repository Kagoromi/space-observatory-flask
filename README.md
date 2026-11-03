# Space Observatory Application


## App Info
Space Observatory Application for searching NASA objects, saving entries to SQLite, managing astronomer notes, and accessing data via REST API endpoints.

## External API
Public NASA Image and Video Library API (https://images-api.nasa.gov/search).

## Run Instructions
Install dependencies:
pip install flask requests

Run application:
python app.py

Open browser:
http://127.0.0.1:5000/

## Database Schema (SQLite)
Table saved_space_objects:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- external_id: TEXT UNIQUE
- title: TEXT NOT NULL
- center: TEXT
- date_created: TEXT
- notes: TEXT
- created_at: TEXT

## REST API Endpoints
```
- GET /api/items (Get all records)
- GET /api/items/<id> (Get single record)
- POST /api/items (Create record)
- PATCH /api/items/<id> (Update record)
- DELETE /api/items/<id> (Delete record)
```
