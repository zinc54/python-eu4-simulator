import tkinter as tk

from event_system import EventSystem
from save_repository import SaveRepository
from gui_helpers.save_load_ui import SaveLoadUI
from gui_helpers.recruitment_ui import RecruitmentUI
from gui_helpers.event_ui import EventUI
from gui_helpers.advisor_ui import AdvisorUI
from country import Country
from collections.abc import Callable
from map_ui import MapUI
from game_event import GameEvent

class GameGUI:
    def __init__(self, game, countries, map_data):
        self.save_rep = SaveRepository()
        self.game = game
        self.event_sys = EventSystem()
        self.countries = countries
        self.map_data = map_data
        self.window = tk.Tk()
        self.window.title("Python EU4 Simulator")
        self.window.geometry("600x400")
        self.first_time_game_frame_shown = True
        self.can_pause = False
        self.create_frames()
        self.map_ui = MapUI(
            self.map_frame,
            self.game,
            self.countries,
            self.show_game_frame,
            self.map_data,
        )
        self.save_load_ui = SaveLoadUI(
            self.save_rep,
            self.pre_load_frame,
            self.pre_save_frame,
            self.show_only_frame,
            self.show_start_screen,
            self.show_game_frame,
            self.set_loaded_game,
            self.get_game_state,
            self.create_button
        )
        self.recruitment_ui = RecruitmentUI(
            self.recruitment_frame,
            self.show_only_frame,
            self.show_game_frame,
            self.get_player_country,
            self.refresh_display,
            self.create_button,
            self.set_can_pause
        )
        self.event_ui = EventUI(
            self.event_frame,
            self.event_sys,
            self.show_only_frame,
            self.show_game_frame,
            self.get_player_country,
            self.refresh_display,
            self.set_can_pause
        )
        self.advisor_ui = AdvisorUI(
            self.advisor_selection_frame,
            self.game,
            self.show_only_frame,
            self.show_game_screen,
            self.set_can_pause
        )
        self.build_start_screen()
        self.build_country_screen()
        self.build_game_screen()
        self.build_pause_menu()
        self.window.bind("<Escape>", self.show_pause_menu)
    # ---------- App Setup / Navigation ----------
    def set_can_pause(self, value: bool) -> None:
        self.can_pause = value
    def create_frames(self):
        self.start_frame = tk.Frame(self.window)
        self.game_frame = tk.Frame(self.window)
        self.country_selection_frame = tk.Frame(self.window)
        self.advisor_selection_frame = tk.Frame(self.window)
        self.event_frame = tk.Frame(self.window)
        self.recruitment_frame = tk.Frame(self.window)
        self.pause_menu_frame = tk.Frame(self.window)
        self.pre_load_frame = tk.Frame(self.window)
        self.pre_save_frame = tk.Frame(self.window)
        self.map_frame = tk.Frame(self.window)
        self.frames = [
            self.start_frame,
            self.game_frame,
            self.country_selection_frame,
            self.advisor_selection_frame,
            self.event_frame,
            self.recruitment_frame,
            self.pause_menu_frame,
            self.pre_load_frame,
            self.pre_save_frame,
            self.map_frame,
        ]

    def create_button(self, frame: tk.Frame, text: str, command: Callable[[], None]) -> tk.Button:
        button = tk.Button(frame, text=text, command=command)
        button.pack()
        return button

    def create_country_selection_handler(self, country_name: str) -> Callable[[], None]:
        def handle_country_selection() -> None:
            self.select_country(country_name)

        return handle_country_selection

    def show_only_frame(self, frame_to_show: tk.Frame) -> None:
        for frame in self.frames:
            frame.pack_forget()
        frame_to_show.pack()

    def show_start_screen(self) -> None:
        self.show_only_frame(self.start_frame)

    def start_new_game(self) -> None:
        self.show_only_frame(self.country_selection_frame)

    def exit_game(self) -> None:
        self.window.destroy()

    def run(self) -> None:
        self.window.mainloop()

    # ---------- Screen Builders ----------
    def build_start_screen(self):
        self.new_game_button = self.create_button(
            self.start_frame,
            "New Game",
            self.start_new_game
        )
        self.load_game_button = self.create_button(
            self.start_frame,
            "Load Game",
            self.save_load_ui.show_load_screen
        )
        self.exit_game_button = self.create_button(
            self.start_frame,
            "Exit game",
            self.exit_game
        )
        self.show_start_screen()

    def build_country_screen(self):
        for country in self.countries:
            self.create_button(
                self.country_selection_frame,
                country.name,
                self.create_country_selection_handler(country.name),
            )
        self.country_confirmation_label = tk.Label(self.country_selection_frame, text="")


    def build_game_screen(self):
        self.month_label = tk.Label(self.game_frame, text="Month: 0")
        self.chosen_country_label = tk.Label(
            self.game_frame,
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.title_label = tk.Label(
            self.game_frame,
            text="Python EU4 Simulator"
        )
        self.title_label.pack()
        self.month_label.pack()
        self.next_month_button = self.create_button(
            self.game_frame,
            "Next Month",
            self.next_month
        )
        self.open_map_button = self.create_button(
            self.game_frame,
            "Open Map",
            self.show_map_screen
        )
    def show_map_screen(self):
        self.map_ui.refresh_map_display()
        self.show_only_frame(self.map_frame)
    def build_pause_menu(self, event=None):
        self.create_button(
            self.pause_menu_frame,
            "Continue",
            self.continue_game_from_pause_menu
        )
        self.create_button(
            self.pause_menu_frame,
            "Save Game",
            self.save_load_ui.show_save_screen
        )
        self.create_button(
            self.pause_menu_frame,
            "Load Game",
            self.save_load_ui.show_load_screen
        )
        self.create_button(
            self.pause_menu_frame,
            "Exit Game",
            self.exit_game
        )

    def show_pause_menu(self, event=None):
        if not self.can_pause:
            return
        self.show_only_frame(self.pause_menu_frame)

    def continue_game_from_pause_menu(self):
        self.show_only_frame(self.game_frame)
    def show_game_frame(self):
        self.refresh_display()
        self.chosen_country_label.pack()
        self.can_pause = True
        self.show_only_frame(self.game_frame)

    def set_loaded_game(self, loaded_game, loaded_countries: list[Country]) -> None:
        self.game = loaded_game
        self.countries = loaded_countries
        self.advisor_ui.set_game(loaded_game)
        for widget in self.map_frame.winfo_children():
            widget.destroy()
        self.map_ui = MapUI(
            self.map_frame,
            self.game,
            self.countries,
            self.show_game_frame,
            self.map_data,
        )
    def get_game_state(self):
        return self.game, self.countries

    # ---------- Month Flow ----------
    def next_month(self) -> None:
        self.game.advance_month(self.countries)
        self.refresh_display()
        month_status = self.game.get_month_action()
        if month_status == "event":
            self.event_ui.show_event_screen()
        elif month_status == "recruitment":
            self.recruitment_ui.show_recruitment_screen()
    # ---------- Country / Advisors ----------
    def select_country(self, country_name: str) -> None:
        self.game.picked_country_name = country_name
        self.country_confirmation_label.config(
            text=f"You have chosen {country_name}"
        )
        self.country_confirmation_label.pack()
        self.window.after(500, self.advisor_ui.show_advisor_screen)

    def show_game_screen(self) -> None:
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.chosen_country_label.pack()
        if self.first_time_game_frame_shown:
            self.build_country_reports()
        self.first_time_game_frame_shown = False
        self.show_only_frame(self.game_frame)
        self.can_pause = True
    def build_country_reports(self) -> None:
        for country in self.countries:
            ducats_report = tk.Label(
                self.game_frame,
                text = f"{country.name} has {country.ducats:.2f} ducats"
            )
            troops_report = tk.Label(
                self.game_frame,
                text=f"{country.name} has {country.troops:.0f} troops"
            )
            ducats_report.pack()
            troops_report.pack()        
    # ---------- Display / Helpers ----------
    def get_player_country(self) -> Country | None:
        for country in self.countries:
            if country.name == self.game.picked_country_name:
                return country
        return None
    def refresh_display(self) -> None:
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        self.build_game_screen()
        self.month_label.config(text=f"Month: {self.game.months_passed}")
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.chosen_country_label.pack()
        self.build_country_reports()
    def get_event_log(self) -> list[GameEvent]:
        return self.game.event_log
