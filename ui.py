#!/usr/bin/env python3
"""
ui.py - All terminal UI styling for KultureKonnect.
Uses colorama for colour and formatting.

To run, pip install colorama
make sure you have pip3 installed,
run sudo apt update,
then run sudo apt install python3-pip
then run sudo apt install python3-colorama
to confirm if it's installed, run python3 -c "import colorama; print('works')"

this module replaces all the plain print statements in the other modules with styled versions,
 and provides reusable building blocks for consistent formatting across the app.
"""

from colorama import init, Fore, Back, Style

# Auto-reset colour after every print
init(autoreset=True)

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = Fore.CYAN
SECONDARY = Fore.MAGENTA
SUCCESS   = Fore.GREEN
WARNING   = Fore.YELLOW
ERROR     = Fore.RED
DIM       = Style.DIM
BOLD      = Style.BRIGHT
RESET     = Style.RESET_ALL


# ── Generic building blocks ───────────────────────────────────────────────────

def divider(char="─", width=45, color=PRIMARY):
    print(color + char * width)

def blank():
    print()

def header(title, char="═", width=45, color=PRIMARY):
    """Prints a full-width box header."""
    blank()
    print(color + BOLD + char * width)
    print(color + BOLD + f"  {title.center(width - 4)}")
    print(color + BOLD + char * width)

def subheader(text, color=SECONDARY):
    print(color + BOLD + f"\n  {text}")
    divider("─", 45, color)

def success(msg):
    print(SUCCESS + BOLD + f"\n  ✔  {msg}")

def error(msg):
    print(ERROR + BOLD + f"\n  ✘  {msg}")

def warn(msg):
    print(WARNING + f"\n  ⚠  {msg}")

def info(msg):
    print(PRIMARY + f"  ℹ  {msg}")

def prompt(msg):
    """Styled input prompt — returns the user's input."""
    return input(Fore.YELLOW + f"  ▶  {msg}" + RESET)


# ── Welcome / auth screens ────────────────────────────────────────────────────

def welcome_screen():
    blank()
    print(PRIMARY + BOLD + "  ╔═══════════════════════════════════════════╗")
    print(PRIMARY + BOLD + "  ║                                           ║")
    print(PRIMARY + BOLD + "  ║   " + Fore.MAGENTA + BOLD + "  K U L T U R E   K O N N E C T  " + PRIMARY + BOLD + "    ║")
    print(PRIMARY + BOLD + "  ║                                           ║")
    print(PRIMARY + BOLD + "  ╚═══════════════════════════════════════════╝")
    blank()
    print(DIM + "  Your personalised guide to cultural events.")
    blank()

def auth_menu():
    header("WELCOME TO KULTURE KONNECT")
    print(f"  {BOLD}1.{RESET} Log In")
    print(f"  {BOLD}2.{RESET} Register")
    print(f"  {BOLD}3.{RESET} Exit")
    blank()

def login_screen():
    header("LOG IN", color=SECONDARY)

def register_screen():
    header("CREATE AN ACCOUNT", color=SECONDARY)
    print(DIM + "  Type 'back' at any prompt to return.\n")


# ── Main menu ─────────────────────────────────────────────────────────────────

def main_menu():
    header("MAIN MENU")
    print(f"  {BOLD}1.{RESET} Find events")
    print(f"  {BOLD}2.{RESET} Rate past attended events")
    print(f"  {BOLD}3.{RESET} Exit")
    blank()


# ── Preferences ───────────────────────────────────────────────────────────────

def preferences_header():
    header("SET YOUR PREFERENCES", color=SECONDARY)
    print(DIM + "  Tell us what kind of experience you are looking for.\n")

def pick_menu(prompt_text, options):
    """
    Numbered pick menu. Returns the chosen string.
    Replaces the plain pick_from_menu in preference_menu.py and profile.py.
    """
    print(SECONDARY + BOLD + f"\n  {prompt_text}")
    divider("─", 45, SECONDARY)
    for i, opt in enumerate(options, start=1):
        print(f"  {PRIMARY}{BOLD}{i}.{RESET}  {opt}")
    while True:
        raw = input(Fore.YELLOW + "  ▶  Your choice: " + RESET).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            chosen = options[int(raw) - 1]
            print(SUCCESS + f"  ✔  Selected: {chosen}")
            return chosen
        error(f"Enter a number between 1 and {len(options)}.")


# ── Profile ───────────────────────────────────────────────────────────────────

def profile_header():
    header("COMPLETE YOUR PROFILE", color=SECONDARY)
    print(DIM + "  Let us get to know you a little better.\n")

def profile_loaded(name):
    success(f"Profile loaded. Hello again, {BOLD}{name}{RESET}{SUCCESS}!")

def profile_created(name):
    success(f"Profile saved. Welcome to KultureKonnect, {BOLD}{name}{RESET}{SUCCESS}!")


# ── Recommendations ───────────────────────────────────────────────────────────

def recommendations_header(name, count):
    blank()
    print(SUCCESS + BOLD + "═" * 45)
    if count:
        print(SUCCESS + BOLD + f"  🎉  {count} event(s) found for you, {name}!")
    else:
        print(WARNING + BOLD + f"  No events matched your preferences, {name}.")
    print(SUCCESS + BOLD + "═" * 45)
    blank()

def recommendation_card(index, event):
    """Print a single styled event card."""
    avg = float(event.get("avg_rating") or 0)
    rating_text = "Not yet rated" if avg <= 0 else f"{avg:.1f} / 10"

    # Colour-code budget
    budget_colors = {"Low": Fore.GREEN, "Medium": Fore.YELLOW, "High": Fore.RED}
    budget_color  = budget_colors.get(event.get("budget", ""), Fore.WHITE)

    print(PRIMARY + BOLD + f"  [{index}] {event['name']}")
    divider("·", 43, DIM)
    print(f"  {'Location':<12} {Fore.WHITE}{event.get('city', '')}")
    print(f"  {'Type':<12} {SECONDARY}{event.get('type', '')}")
    print(f"  {'Budget':<12} {budget_color}{event.get('budget', '')}")
    print(f"  {'Time':<12} {Fore.WHITE}{event.get('time', '')}")
    print(f"  {'Rating':<12} {Fore.YELLOW}{rating_text}")
    if event.get("description"):
        print(f"  {'Details':<12} {DIM}{event.get('description')}")
    blank()

def no_recommendations(name):
    blank()
    print(WARNING + BOLD + "═" * 45)
    print(WARNING + f"  No events matched your preferences, {name}.")
    print(DIM   + "  Try a higher budget or different time of day.")
    print(WARNING + BOLD + "═" * 45)
    blank()


# ── Post-action menu ──────────────────────────────────────────────────────────

def post_actions_header():
    subheader("CHOOSE AN ACTIVITY", color=PRIMARY)

def action_menu():
    blank()
    print(f"  {BOLD}1.{RESET} Schedule an Itinerary")
    print(f"  {BOLD}2.{RESET} Make a Reservation")
    print(f"  {BOLD}3.{RESET} Buy Tickets")
    print(f"  {BOLD}4.{RESET} Return to Main Menu")
    blank()

def action_confirmed(action_label, event_name):
    blank()
    print(SUCCESS + BOLD + "─" * 45)
    print(SUCCESS + BOLD + f"  ✔  {action_label}: {event_name}")
    print(SUCCESS + "  Thank you for using KultureKonnect!")
    print(SUCCESS + BOLD + "─" * 45)
    blank()


# ── Ratings ───────────────────────────────────────────────────────────────────

def ratings_header():
    header("RATE A PAST EVENT", color=SECONDARY)

def rating_saved(venue_name, rating):
    success(f"Rating of {BOLD}{rating}/10{RESET}{SUCCESS} saved for {BOLD}{venue_name}{RESET}{SUCCESS}.")


# ── Exit ──────────────────────────────────────────────────────────────────────

def goodbye():
    blank()
    print(PRIMARY + BOLD + "  Thank you for using KultureKonnect. See you next time!")
    blank()