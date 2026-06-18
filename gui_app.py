import random
import tkinter as tk

from event_system import EventSystem
from save_repository import SaveRepository
from save_load_ui import SaveLoadUI

class GameGUI:
    def __init__(self, game, countries):
        self.save_rep = SaveRepository()
        self.game = game
        self.event_sys = EventSystem()
        self.countries = countries
        self.window = tk.Tk()
        self.window.title("Python EU4 Simulator")
        self.window.geometry("600x400")
        self.can_pause = False
        self.create_frames()
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
        self.build_start_screen()
        self.build_country_screen()
        self.build_game_screen()
        self.build_advisor_screen()
        self.build_event_screen()
        self.build_recruiting_screen()
        self.build_pause_menu()
        self.window.bind("<Escape>", self.show_pause_menu)
    # ---------- App Setup / Navigation ----------
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
        self.frames = [
            self.start_frame,
            self.game_frame,
            self.country_selection_frame,
            self.advisor_selection_frame,
            self.event_frame,
            self.recruitment_frame,
            self.pause_menu_frame,
            self.pre_load_frame,
            self.pre_save_frame
        ]

    def create_button(self, frame, text, command):
        button = tk.Button(frame, text=text, command=command)
        button.pack()
        return button

    def show_only_frame(self, frame_to_show):
        for frame in self.frames:
            frame.pack_forget()
        frame_to_show.pack()

    def show_start_screen(self):
        self.show_only_frame(self.start_frame)

    def start_new_game(self):
        self.show_only_frame(self.country_selection_frame)

    def exit_game(self):
        self.window.destroy()

    def run(self):
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
        self.ottomans_button = self.create_button(
            self.country_selection_frame,
            "Ottomans",
            lambda: self.select_country("Ottomans")
        )
        self.france_button = self.create_button(
            self.country_selection_frame,
            "France",
            lambda: self.select_country("France")
        )
        self.country_confirmation_label = tk.Label(self.country_selection_frame, text="")

    def build_advisor_screen(self):
        self.total_advisor_cost = 0
        self.mil_advisor_label = tk.Label(self.advisor_selection_frame, text="Military Advisor:")
        self.dip_advisor_label = tk.Label(self.advisor_selection_frame, text="Diplomatic Advisor:")
        self.admin_advisor_label = tk.Label(self.advisor_selection_frame, text="Administrative Advisor:")
        self.continue_button_advisors = tk.Button(
            self.advisor_selection_frame,
            text="Continue.",
            command=self.show_game_screen
        )
        self.military_advisor_level = tk.IntVar(value=0)
        self.diplomatic_advisor_level = tk.IntVar(value=0)
        self.administrative_advisor_level = tk.IntVar(value=0)
        self.military_dropdown = tk.OptionMenu(
            self.advisor_selection_frame,
            self.military_advisor_level,
            0, 1, 2, 3,
            command=self.update_advisor_cost
        )
        self.diplomatic_dropdown = tk.OptionMenu(
            self.advisor_selection_frame,
            self.diplomatic_advisor_level,
            0, 1, 2, 3,
            command=self.update_advisor_cost
        )
        self.administrative_dropdown = tk.OptionMenu(
            self.advisor_selection_frame,
            self.administrative_advisor_level,
            0, 1, 2, 3,
            command=self.update_advisor_cost
        )
        self.advisor_cost_label = tk.Label(
            self.advisor_selection_frame,
            text="Total monthly advisor cost: 0 ducats"
        )
        self.mil_advisor_label.grid(row=0, column=0)
        self.military_dropdown.grid(row=0, column=1)
        self.dip_advisor_label.grid(row=1, column=0)
        self.diplomatic_dropdown.grid(row=1, column=1)
        self.admin_advisor_label.grid(row=2, column=0)
        self.administrative_dropdown.grid(row=2, column=1)
        self.advisor_cost_label.grid(row=3, column=0)
        self.continue_button_advisors.grid(row=4, column=0)

    def build_game_screen(self):
        self.month_label = tk.Label(self.game_frame, text="Month: 0")
        self.chosen_country_label = tk.Label(
            self.game_frame,
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.first_country_ducats = tk.Label(
            self.game_frame,
            text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats"
        )
        self.second_country_ducats = tk.Label(
            self.game_frame,
            text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats"
        )
        self.first_country_troops_label = tk.Label(
            self.game_frame,
            text=f"{self.countries[0].name} has {self.countries[0].troops} troops"
        )
        self.second_country_troops_label = tk.Label(
            self.game_frame,
            text=f"{self.countries[1].name} has {self.countries[1].troops} troops"
        )
        self.title_label = tk.Label(
            self.game_frame,
            text="Python EU4 Simulator"
        )
        self.title_label.pack()
        self.month_label.pack()
        self.first_country_ducats.pack()
        self.second_country_ducats.pack()
        self.first_country_troops_label.pack()
        self.second_country_troops_label.pack()
        self.next_month_button = self.create_button(
            self.game_frame,
            "Next Month",
            self.next_month
        )

    def build_recruiting_screen(self):
        self.recruitment_question = tk.Label(
            self.recruitment_frame,
            text="How many troops in thousands do you wanna recruit? Type in the box below."
        )
        self.recruitment_entry = tk.Entry(self.recruitment_frame)
        self.incorrect_input_warning_recruitment = tk.Label(
            self.recruitment_frame,
            text="Please only input whole numbers."
        )
        self.invalid_amount_recruitment = tk.Label(
            self.recruitment_frame,
            text="Please only input positive numbers."
        )
        self.too_expensive_recruitment = tk.Label(
            self.recruitment_frame,
            text="You can't afford to recruit this many stacks of troops!"
        )
        self.recruitment_entry_submit_button = tk.Button(
            self.recruitment_frame,
            text="Submit",
            command=self.apply_recruitment
        )
        self.recruitment_button = self.create_button(
            self.recruitment_frame,
            "Recruit Troops",
            self.show_recruitment_if_yes
        )
        self.recruitment_cancel_button = self.create_button(
            self.recruitment_frame,
            "Cancel",
            self.cancel_recruitment
        )

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

    def build_pause_menu(self, event=None):
        pause_menu_continue_button = self.create_button(
            self.pause_menu_frame,
            "Continue",
            self.continue_game_from_pause_menu
        )
        pause_menu_save_button = self.create_button(
            self.pause_menu_frame,
            "Save Game",
            self.save_load_ui.show_save_screen
        )
        pause_menu_load_button = self.create_button(
            self.pause_menu_frame,
            "Load Game",
            self.save_load_ui.show_load_screen
        )
        pause_menu_exit = self.create_button(
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

    def set_loaded_game(self, loaded_game, loaded_countries):
        self.game = loaded_game
        self.countries = loaded_countries

    def get_game_state(self):
        return self.game, self.countries

    # ---------- Month Flow ----------
    def next_month(self):
        self.game.advance_month(self.countries)
        self.refresh_display()
        month_status = self.game.get_month_action()
        if month_status == "event":
            self.show_event_screen()
        elif month_status == "recruitment":
            self.show_recruitment_screen()

    # ---------- Recruitment ----------
    def show_recruitment_screen(self):
        self.can_pause = False
        self.show_only_frame(self.recruitment_frame)

    def show_recruitment_if_yes(self):
        self.recruitment_button.pack_forget()
        self.recruitment_cancel_button.pack_forget()
        self.recruitment_question.pack()
        self.recruitment_entry.pack()
        self.recruitment_entry_submit_button.pack()

    def apply_recruitment(self):
        country = self.get_player_country()
        requested_stacks = self.recruitment_entry.get()
        result = country.recruit_troops(requested_stacks)
        if result == "invalid_input":
            self.incorrect_input_warning_recruitment.pack()
            self.too_expensive_recruitment.pack_forget()
            self.invalid_amount_recruitment.pack_forget()
        elif result == "too_expensive":
            self.too_expensive_recruitment.pack()
            self.incorrect_input_warning_recruitment.pack_forget()
            self.invalid_amount_recruitment.pack_forget()
        elif result == "invalid_amount":
            self.invalid_amount_recruitment.pack()
            self.too_expensive_recruitment.pack_forget()
            self.incorrect_input_warning_recruitment.pack_forget()
        elif result == "success":
            self.cancel_recruitment()

    def cancel_recruitment(self):
        for widget in self.recruitment_frame.winfo_children():
            widget.pack_forget()
        self.recruitment_entry.delete(0, tk.END)
        self.recruitment_button.pack()
        self.recruitment_cancel_button.pack()
        self.show_only_frame(self.game_frame)
        self.refresh_display()
        self.can_pause = True

    # ---------- Events ----------
    def show_event_screen(self):
        self.can_pause = False
        selected_event_text = random.choice(list(self.event_sys.events.keys()))
        options = list(self.event_sys.events[selected_event_text].values())

        self.event_text.config(text=selected_event_text)
        self.event_choice_one.config(
            text=f"{options[0]} Consequence: {self.event_sys.event_consequences[options[0]]['description']}",
            command=lambda: self.choose_event_option(options[0])
        )
        self.event_choice_two.config(
            text=f"{options[1]} Consequence: {self.event_sys.event_consequences[options[1]]['description']}",
            command=lambda: self.choose_event_option(options[1])
        )

        self.show_only_frame(self.event_frame)

    def choose_event_option(self, choice):
        recruitment_country = self.get_player_country()
        self.event_sys.apply_event_choice(recruitment_country, choice)

        self.show_only_frame(self.game_frame)
        self.refresh_display()
        self.can_pause = True

    # ---------- Country / Advisors ----------
    def select_country(self, country_name):
        self.game.picked_country_name = country_name
        self.country_confirmation_label.config(
            text=f"You have chosen {country_name}"
        )
        self.country_confirmation_label.pack()
        self.window.after(500, self.show_advisor_screen)

    def show_advisor_screen(self):
        self.can_pause = False
        self.show_only_frame(self.advisor_selection_frame)

    def update_advisor_cost(self, selected_level=None):
        military_level = self.military_advisor_level.get()
        diplomatic_level = self.diplomatic_advisor_level.get()
        administrative_level = self.administrative_advisor_level.get()
        mil_advisor_cost = self.game.advisor_costs[military_level]
        dip_advisor_cost = self.game.advisor_costs[diplomatic_level]
        admin_advisor_cost = self.game.advisor_costs[administrative_level]
        self.total_advisor_cost = mil_advisor_cost + dip_advisor_cost + admin_advisor_cost
        self.advisor_cost_label.config(
            text=f"The total advisor cost for your country is: {self.total_advisor_cost}"
        )

    def show_game_screen(self):
        self.game.monthly_advisor_expenses = self.total_advisor_cost
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.chosen_country_label.pack()
        self.show_only_frame(self.game_frame)
        self.can_pause = True

    # ---------- Display / Helpers ----------
    def get_player_country(self):
        for country in self.countries:
            if country.name == self.game.picked_country_name:
                return country

    def refresh_display(self):
        self.month_label.config(text=f"Month: {self.game.months_passed}")
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.first_country_ducats.config(
            text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats"
        )
        self.second_country_ducats.config(
            text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats"
        )
        self.first_country_troops_label.config(
            text=f"{self.countries[0].name} has {self.countries[0].troops} troops"
        )
        self.second_country_troops_label.config(
            text=f"{self.countries[1].name} has {self.countries[1].troops} troops"
        )
