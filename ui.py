#!/usr/bin/env python3
"""
ui.py - Centralised display layer for KultureKonnect.

Import this in any file and call the helpers instead of print().
Every visual decision lives here — the other files stay logic-only.

Usage:
    from ui import ui
    ui.header("MY SECTION")
    ui.ok("All done!")
    ui.err("Something went wrong.")
    ui.menu_item(1, "Log In")
    ui.pick_prompt("Choose an activity", ["Movies", "Games"])
    ui.results_table(matches)
    ui.welcome()
    ui.spinner_search()        # call before loading events
    ui.success_action(message) # call after itinerary/reservation/ticket
"""

import os
import time

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich.text    import Text
from rich.rule    import Rule
from rich.live    import Live
from rich.spinner import Spinner
from rich         import box

# Single shared console — import this too if you need raw console.print()
console = Console()


class UI:
    # ------------------------------------------------------------------
    # Structural / section markers
    # ------------------------------------------------------------------

    def clear(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def rule(self, title=""):
        """Yellow horizontal rule with an optional centred title."""
        console.print(Rule(f"[bold yellow]{title}[/bold yellow]", style="yellow"))

    def header(self, title, subtitle=None):
        """
        Section header — yellow rule + bold title + optional dim subtitle.
        Drop-in replacement for the  print("=" * 45) / print(title) pattern.
        """
        console.print()
        self.rule(title)
        if subtitle:
            console.print(f"  [dim]{subtitle}[/dim]")

    # ------------------------------------------------------------------
    # Status messages  (ok / err / warn / info)
    # ------------------------------------------------------------------

    def ok(self, msg):
        """Green success line.  Replaces bare print() for success text."""
        console.print(f"  [bold green]✔  {msg}[/bold green]")

    def err(self, msg):
        """Red error line.  Replaces print() for validation / error text."""
        console.print(f"  [red]✘  {msg}[/red]")

    def warn(self, msg):
        """Yellow warning line."""
        console.print(f"  [yellow]!  {msg}[/yellow]")

    def info(self, msg):
        """Plain dim info line for secondary / contextual messages."""
        console.print(f"  [dim]{msg}[/dim]")

    def plain(self, msg):
        """Unstyled print — use when you just need a newline or plain text."""
        console.print(msg)

    # ------------------------------------------------------------------
    # Panels  (bordered boxes)
    # ------------------------------------------------------------------

    def success_panel(self, msg):
        """
        Green bordered panel.
        Use for multi-line confirmations: registration, login, profile saved, etc.
        """
        console.print(Panel(f"[bold green]{msg}[/bold green]", border_style="green", padding=(0, 2)))

    def warning_panel(self, msg):
        """Yellow bordered panel for soft warnings / no-results messages."""
        console.print(Panel(f"[yellow]{msg}[/yellow]", border_style="yellow", padding=(0, 2)))

    def error_panel(self, msg):
        """Red bordered panel for hard errors."""
        console.print(Panel(f"[red]{msg}[/red]", border_style="red", padding=(0, 2)))

    def success_action(self, msg):
        """
        Final confirmation panel shown after itinerary / reservation / ticket.
        Includes the thank-you line automatically.
        """
        console.print()
        console.print(Panel(
            f"[bold green]{msg}[/bold green]\n\n[dim]Thank you for using KultureKonnect! 🌍[/dim]",
            border_style="green",
            padding=(1, 2),
        ))
        console.print()

    # ------------------------------------------------------------------
    # Menus
    # ------------------------------------------------------------------

    def menu_item(self, number, label):
        """
        Single numbered menu option.
        Call once per option inside your menu block.
        e.g.  ui.menu_item(1, "Log In")
        """
        console.print(f"  [bold cyan]{number}.[/bold cyan]  {label}")

    def pick_prompt(self, prompt, options):
        """
        Numbered option list + input loop.
        Replaces the pick_from_menu() helper that is duplicated in
        preference_menu.py and profile.py.
        Returns the chosen string.
        """
        console.print(f"\n  [bold yellow]{prompt}[/bold yellow]")
        for i, option in enumerate(options, start=1):
            console.print(f"  [bold cyan]{i}.[/bold cyan]  {option}")
        while True:
            choice = input("  Enter the number of your choice: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            self.err(f"Invalid choice. Please enter a number between 1 and {len(options)}.")

    # ------------------------------------------------------------------
    # Special screens
    # ------------------------------------------------------------------

    def welcome(self):
        """
        Full-screen welcome banner.
        Call once at the very start of main().
        """
        self.clear()
        console.print()
        welcome_text = Text(justify="center")
        welcome_text.append("🌍  KULTURE KONNECT  🌍\n", style="bold yellow")
        welcome_text.append("Your personalised guide to cultural events\n", style="dim white")
        welcome_text.append("in Kigali, Nairobi, and beyond",              style="dim white")
        console.print(Panel(welcome_text, border_style="yellow", padding=(1, 4)))
        console.print()

    def spinner_search(self):
        """
        Animated spinner shown while events are being loaded / filtered.
        Call this just before recommender.load_events().
        """
        console.print()
        with Live(
            Spinner("dots", text="  [yellow]Searching for events that match your preferences...[/yellow]"),
            console=console,
            refresh_per_second=12,
        ):
            time.sleep(1.2)

    # ------------------------------------------------------------------
    # Results table
    # ------------------------------------------------------------------

    def results_table(self, matches, username=""):
        """
        Render the recommendations as a Rich table.
        Replaces the manual for-loop print block in kulture_konnect.py.

        matches  : list of event dicts from recommender.get_recommendations()
        username : optional — used in the header line
        """
        console.print()
        self.rule("Your Recommendations")
        console.print()

        if not matches:
            self.warning_panel(
                f"No events matched your preferences{', ' + username if username else ''}.\n"
                "Try a higher budget or a different time of day."
            )
            return

        name_str = f", [bold]{username}[/bold]" if username else ""
        console.print(f"  [bold green]✔  Found [yellow]{len(matches)}[/yellow] event(s) for you{name_str}![/bold green]\n")

        table = Table(
            box=box.ROUNDED,
            border_style="yellow",
            header_style="bold yellow",
            show_lines=True,
            expand=True,
        )
        table.add_column("#",       style="dim",        width=3,  justify="center")
        table.add_column("Event",   style="bold white", min_width=20)
        table.add_column("Type",    style="cyan",       width=14)
        table.add_column("City",    style="green",      width=10)
        table.add_column("Budget",  style="magenta",    width=8,  justify="center")
        table.add_column("Time",    style="blue",       width=11)
        table.add_column("Details", style="dim white",  min_width=24)

        for i, event in enumerate(matches, start=1):
            table.add_row(
                str(i),
                event["name"],
                event["type"],
                event["city"],
                event["budget"],
                event["time"],
                event.get("description", "—"),
            )

        console.print(table)
        console.print()

    # ------------------------------------------------------------------
    # Event selection list  (post_actions)
    # ------------------------------------------------------------------

    def event_list(self, matches):
        """
        Simple numbered list of matched events for the post-actions selector.
        Returns the chosen event dict.
        """
        console.print()
        self.rule("Choose Your Activity")
        console.print()

        for i, event in enumerate(matches, start=1):
            console.print(
                f"  [bold cyan]{i}.[/bold cyan]  {event['name']} "
                f"[dim]({event['type']})[/dim]"
            )
        console.print()

        while True:
            try:
                choice = int(input("  Enter the event number: "))
                if 1 <= choice <= len(matches):
                    return matches[choice - 1]
                self.err(f"Please enter a number between 1 and {len(matches)}.")
            except ValueError:
                self.err("Please enter a valid number.")


# Single instance — every file imports this one object
ui = UI()
