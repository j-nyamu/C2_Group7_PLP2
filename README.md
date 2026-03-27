# KultureKonnect

A terminal-based cultural event recommender. Users register or log in, build a profile, get matched to local events, and can schedule/reserve/buy tickets — then rate the events they attend.

## Quick Start

```bash
python3 kulture_konnect.py
```

---

## Project Structure

```
kulture_konnect.py   ← entry point, orchestrates the full app loop
db.py                ← shared MySQL connection helper (reads from .env)
auth.py              ← register / login, password hashing
profile.py           ← create and load user profiles
preference_menu.py   ← main menu + per-session preference collection
recommender.py       ← loads venues from DB, filters to matches
post_actions.py      ← event selection + itinerary/reservation/ticket actions
rec_ratings.py       ← rate a previously attended event
ui.py                ← all terminal styling (colorama)

create_tables.py     ← one-time setup: creates all DB tables
migrate.py           ← one-time migration: seeds DB from JSON files
venue_database.json  ← source data for venues (used by migrate.py)
```

---

## Environment Setup

### 1. Prerequisites

- Python 3.8+
- A running MySQL instance (the project uses Aiven cloud MySQL)
- `ca.pem` SSL certificate file in the project root (download from your Aiven console)

### 2. Install dependencies

```bash
pip install mysql-connector-python colorama python-dotenv
```

On Ubuntu/Debian you can also install colorama via apt:

```bash
sudo apt update
sudo apt install python3-pip
sudo apt install python3-colorama
```

Verify colorama is installed:

```bash
python3 -c "import colorama; print('works')"
```

### 3. Configure the database connection

Create a `.env` file in the project root (never commit this file):

```
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=defaultdb
DB_SSL_DISABLED=false
DB_SSL_CA=ca.pem
DB_SSL_VERIFY_CERT=true
DB_SSL_VERIFY_IDENTITY=true
```

`db.py` reads all of these with `os.getenv()`. If a value is missing the connection will fail with a clear error.

> **Warning:** Do not share or push `.env` to a public repository. Add it to `.gitignore`.

### 4. Load the .env file

`db.py` does not auto-load `.env` — you must either export the variables in your shell or use `python-dotenv`. The simplest approach is to add this near the top of `kulture_konnect.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

Or export manually before running:

```bash
export $(grep -v '^#' .env | xargs)
```

### 5. Create tables (run once)

```bash
python3 create_tables.py
```

This creates: `users`, `profiles`, `user_actions`, `venues`, `venue_ratings`.

### 6. Seed venue data (run once)

```bash
python3 migrate.py
```

Reads `venue_database.json` and any `profiles/*.json` files and inserts them into the DB. Uses `INSERT IGNORE` so it is safe to re-run.

### 7. Run the app

```bash
python3 kulture_konnect.py
```

---

## How the Scripts Talk to Each Other

```
kulture_konnect.py
│
├── auth.py            auth_gate() → login() / register() → returns username
│   └── db.py          get_connection() for user lookup and INSERT
│
├── profile.py         get_or_create_profile(username, user_id)
│   └── db.py          SELECT / INSERT profiles table
│
├── preference_menu.py load_main_menu() → get_preferences() → returns dict
│   └── ui.py          all display calls
│
├── recommender.py     load_events() from DB, get_recommendations() filters them
│   └── db.py          SELECT venues + AVG(venue_ratings)
│
├── post_actions.py    show_post_actions_menu(matches, user_id)
│   └── db.py          INSERT into user_actions (itinerary / reservation / ticket)
│
└── rec_ratings.py     save_events_rating(user_id)
    └── db.py          JOIN user_actions + venues, INSERT/UPDATE venue_ratings
```

`ui.py` is a pure display layer imported by most modules — it has no DB calls.

`db.py` is the only file that knows the connection details. Every other module calls `get_connection()` from it.

### Data flow for a typical session

1. `auth_gate()` prompts login or register → returns `username`
2. `get_user_id(username)` looks up the integer `user_id` (used as the FK everywhere else)
3. `get_or_create_profile()` loads or builds the user's profile dict (name, age, budget, city)
4. `load_main_menu()` returns `"1"`, `"2"`, or `"3"`
5. On `"1"`: `get_preferences()` collects activity type + noise + time → `get_recommendations()` filters the venues table against profile + preferences → `show_post_actions_menu()` saves the chosen action to `user_actions`
6. On `"2"`: `save_events_rating()` joins `user_actions` → `venues` to show only attended venues, then writes a 1–10 score to `venue_ratings`

---

## Database Schema (quick reference)

| Table | Purpose |
|---|---|
| `users` | Credentials — username, salt, hashed password |
| `profiles` | Per-user details — name, age, gender, budget, city |
| `venues` | Event/venue catalogue — type, city, budget, noise, min_age, time_of_day |
| `user_actions` | History of itineraries / reservations / tickets per user |
| `venue_ratings` | 1–10 ratings; one row per (venue, user) pair |

---

## Things to Watch Out For

**`.env` credentials must not be in version control**
Rotate any credentials before pushing to a public repo and add `.env` to `.gitignore`.

**`ca.pem` must be present**
SSL is enabled by default (`DB_SSL_DISABLED=false`). If `ca.pem` is missing or in the wrong directory the connection will fail with an SSL error. Download it from your Aiven service page and place it in the project root.

**`python-dotenv` is not auto-loaded**
`db.py` calls `os.getenv()` but never calls `load_dotenv()`. If you run the app without exporting the env vars first, every `DB_*` variable will be an empty string and the connection will fail. Add `load_dotenv()` to `kulture_konnect.py` or export the vars in your shell beforehand.

**City matching is case-insensitive but whitespace-sensitive**
`get_recommendations()` does `.strip().lower()` comparisons, so `"nairobi"` vs `"Nairobi"` will still match. However, any leading or trailing spaces typed at profile creation (e.g. `"nairobi "`) will silently break matching.

**`post_actions.py` uses raw `print` instead of `ui.*`**
Unlike the other modules, `post_actions.py` still uses plain `print` and raw ANSI escape codes. If you refactor the colour scheme in `ui.py`, remember to update this file separately.

**`rec_ratings.py` joins on venue name, not ID**
The join is `LOWER(v.name) = LOWER(ua.event_name)`. If a venue is renamed in the DB after actions were recorded against the old name, those attended events will no longer appear in the ratings list.

**`migrate.py` is for historical JSON data only**
Run it once after `create_tables.py` to seed the initial data. It will print warnings for any JSON profile whose username does not already exist in the `users` table.
