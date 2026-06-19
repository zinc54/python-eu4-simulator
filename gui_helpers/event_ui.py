import tkinter as tk
import random

class EventUI:
    def __init__(
        self,
        event_frame,
        event_system,
        show_only_frame,
        show_game_frame,
        get_player_country,
        refresh_display,
        set_can_pause
    ):
        self.event_frame = event_frame
        self.event_system = event_system
        self.show_only_frame = show_only_frame
        self.show_game_frame = show_game_frame
        self.get_player_country = get_player_country
        self.refresh_display = refresh_display
        self.set_can_pause = set_can_pause

    def build_event_screen(self):
        self.event_text = tk.Label(
            self.event_frame,
            text=""
        )
        self.event_choice_one = tk.Button(
            self.event_frame,
            text=""
        )
        self.event_choice_two = tk.Button(
            self.event_frame,
            text=""
        )
        self.event_text.pack()
        self.event_choice_one.pack()
        self.event_choice_two.pack()

    def show_event_screen(self):
        self.set_can_pause(False)
        selected_event_text = random.choice(list(self.event_system.events.keys()))
        options = list(self.event_system.events[selected_event_text].values())

        self.event_text.config(text=selected_event_text)
        self.event_choice_one.config(
            text=f"{options[0]} Consequence: {self.event_system.event_consequences[options[0]]['description']}",
            command=lambda: self.choose_event_option(options[0])
        )
        self.event_choice_two.config(
            text=f"{options[1]} Consequence: {self.event_system.event_consequences[options[1]]['description']}",
            command=lambda: self.choose_event_option(options[1])
        )

        self.show_only_frame(self.event_frame)

    def choose_event_option(self, choice):
        recruitment_country = self.get_player_country()
        self.event_system.apply_event_choice(recruitment_country, choice)

        self.show_game_frame()
        self.refresh_display()
        self.set_can_pause(True)
