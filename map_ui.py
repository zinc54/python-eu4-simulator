import tkinter as tk
from collections.abc import Callable
from typing import TypedDict

from battle import Battle


class CountryMapData(TypedDict):
    x1: int
    y1: int
    x2: int
    y2: int
    color: str


class MapUI:
    def __init__(self, parent_frame, game, countries, show_game_screen, map_data):
        self.parent_frame = parent_frame
        self.game = game
        self.countries = countries
        self.show_game_screen = show_game_screen
        self.map_data = map_data
        self.selected_country_name = ""
        self.canvas = tk.Canvas(
            self.parent_frame,
            width=600,
            height=400,
            background="lightblue",
        )
        self.canvas.pack()
        self.build_map()
    def select_country(self, country_name):
        if country_name == self.game.picked_country_name:
            selection_message = f"You are playing as {country_name}"
            self.canvas.itemconfig(
                self.battle_button_window,
                state="hidden",
            )
        else:
            selection_message = f"Selected: {country_name}"
            self.selected_country_name = country_name
            self.canvas.itemconfig(
                self.battle_button_window,
                state="normal",
            )

        self.canvas.itemconfig(
            self.selection_text,
            text=selection_message
        )
    def create_country_click_handler(self, country_name: str) -> Callable[[tk.Event], None]:
        def handle_country_click(event: tk.Event) -> None:
            self.select_country(country_name)

        return handle_country_click

    def show_battle_result(self, result):
        result_window = tk.Toplevel(self.parent_frame)
        result_window.title("Battle Results")
        result_window.geometry("500x300")
        content_frame = tk.Frame(result_window)
        content_frame.pack(expand=True)

        tk.Label(
            content_frame,
            text=f"{result['winner']} won!",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=0, columnspan=3, pady=15)

        tk.Label(content_frame, text="Country").grid(row=1, column=0)
        tk.Label(content_frame, text="Before").grid(row=1, column=1)
        tk.Label(content_frame, text="After").grid(row=1, column=2)

        attacker = result["attacker"]
        defender = result["defender"]
        
        tk.Label(
            content_frame,
            text=f"{attacker['name']} troops"
        ).grid(row=2, column=0)

        tk.Label(
            content_frame,
            text=f"{attacker['before']['troops']:.0f}"
        ).grid(row=2, column=1)

        tk.Label(
            content_frame,
            text=f"{attacker['after']['troops']:.0f}"
        ).grid(row=2, column=2)

        tk.Label(
            content_frame,
            text=f"{defender['name']} troops",
        ).grid(row=3, column=0)

        tk.Label(
            content_frame,
            text=f"{defender['before']['troops']:.0f}",
        ).grid(row=3, column=1)

        tk.Label(
            content_frame,
            text=f"{defender['after']['troops']:.0f}",
        ).grid(row=3, column=2)
        tk.Label(
            content_frame,
            text=f"{attacker['name']} morale"
        ).grid(row=4, column=0)
        tk.Label(
            content_frame,
            text=f"{attacker['before']['morale']:.1f}"
        ).grid(row=4, column=1)
        tk.Label(
            content_frame,
            text=f"{attacker['after']['morale']:.1f}"
        ).grid(row=4, column=2)
        tk.Label(
            content_frame,
            text=f"{defender['name']} morale"
        ).grid(row=5, column=0)
        tk.Label(
            content_frame,
            text=f"{defender['before']['morale']:.1f}"
        ).grid(row=5, column=1)
        tk.Label(
            content_frame,
            text=f"{defender['after']['morale']:.1f}"
        ).grid(row=5, column=2)
        continue_button = tk.Button(
            content_frame,
            text="Continue",
            command=result_window.destroy,
        )
        continue_button.grid(row=6, column=0, columnspan=3, pady=20)

        
    def start_battle(self):
        attacker = None
        defender = None
        for country in self.countries:
            if country.name == self.game.picked_country_name:
                attacker = country
            elif country.name == self.selected_country_name:
                defender = country
        if attacker is None or defender is None:
            self.canvas.itemconfig(
                self.selection_text,
                text="Pick an enemy country before starting a battle.",
            )
            return
        started_battle = Battle(attacker, defender)
        battle_result_info = started_battle.resolve_battle()
        self.show_battle_result(battle_result_info)
    def refresh_map_display(self):
        self.canvas.itemconfig(
            self.selection_text,
            text=f"Playing as: {self.game.picked_country_name}"
        )
        self.canvas.itemconfig(
            self.battle_button_window,
            state="hidden",
        )

    def build_map(self):
        self.battle_button = tk.Button(
            self.canvas,
            text="Battle this nation",
            command=self.start_battle,
        )
        self.exit_map_button = tk.Button(
            self.canvas,
            text="Exit Map",
            command=self.show_game_screen,
        )

        self.canvas.create_window(
            550,
            370,
            window=self.exit_map_button,
        )
        self.battle_button_window = self.canvas.create_window(
            300,
            350,
            window=self.battle_button,
            state="hidden",
        )
        self.selection_text = self.canvas.create_text(
            10,
            10,
            text=f"Playing as: {self.game.picked_country_name}",
            anchor="nw",
            font=("Arial", 12, "bold"),
        )
        for country in self.countries:
            map_data = self.map_data[country.name]

            self.canvas.create_rectangle(
                map_data["x1"],
                map_data["y1"],
                map_data["x2"],
                map_data["y2"],
                fill=map_data["color"],
                tags=country.name
            )

            center_x = (map_data["x1"] + map_data["x2"]) / 2
            center_y = (map_data["y1"] + map_data["y2"]) / 2

            self.canvas.create_text(
                center_x,
                center_y,
                text=country.name,
                fill="white",
                font=("Arial", 16, "bold"),
                tags=country.name,
            )

            self.canvas.tag_bind(
                country.name,
                "<Button-1>",
                self.create_country_click_handler(country.name),
            )
