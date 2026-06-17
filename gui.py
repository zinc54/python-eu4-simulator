import tkinter as tk
from game import Game
from country import Country
from event_system import EventSystem
from save_repository import SaveRepository
import random

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
        self.build_start_screen()
        self.build_country_screen()
        self.build_game_screen()
        self.build_advisor_screen()
        self.build_event_screen()
        self.build_recruiting_screen()
        self.build_pause_menu()
        self.window.bind("<Escape>", self.show_pause_menu)
        self.build_pre_saving()
    def build_pre_saving(self):
        self.save_name_input = tk.Entry(self.pre_save_frame)
        self.save_selected_name_button = tk.Button(
            self.pre_save_frame,
            text = "Save Game",
            command=self.pause_menu_save
        )
        self.save_name_input.pack()
        self.save_selected_name_button.pack()
    def build_pause_menu(self, event=None):
        pause_menu_continue_button = tk.Button(
            self.pause_menu_frame,
            text="Continue",
            command=self.continue_game_from_pause_menu
        )
        pause_menu_save_button  = tk.Button(
            self.pause_menu_frame,
            text="Save Game",
            command=self.show_pre_saved_game
        )
        pause_menu_load_button = tk.Button(
            self.pause_menu_frame,
            text="Load Game",
            command=self.show_pre_loaded_game
        )
        pause_menu_exit = tk.Button(
            self.pause_menu_frame,
            text="Exit Game",
            command=self.exit_game
        )
        pause_menu_continue_button.pack()
        pause_menu_save_button.pack()
        pause_menu_load_button.pack()
        pause_menu_exit.pack()
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
    def build_recruiting_screen(self):
        self.recruitment_question = tk.Label(self.recruitment_frame, text="How many troops in thousands do you wanna recruit? Type in the box below.")
        self.recruitment_entry = tk.Entry(self.recruitment_frame)
        self.incorrect_input_warning_recruitment = tk.Label(
            self.recruitment_frame,
            text=f"Please only input whole numbers."
        )
        self.invalid_amount_recruitment = tk.Label(
            self.recruitment_frame,
            text=f"Please only input positive numbers."
        )
        self.too_expensive_recruitment = tk.Label(
            self.recruitment_frame,
            text = "You can't afford to recruit this many stacks of troops!"
        )
        self.recruitment_entry_submit_button = tk.Button(
            self.recruitment_frame,
            text = "Submit",
            command = self.apply_recruitment
        )
        self.recruitment_button = tk.Button(
            self.recruitment_frame,
            text="Recruit Troops",
            command=self.show_recruitment_if_yes
        )
        self.recruitment_cancel_button = tk.Button(
            self.recruitment_frame,
            text="Cancel",
            command=self.cancel_recruitment
        )
        self.recruitment_button.pack()
        self.recruitment_cancel_button.pack()
    def build_country_screen(self):
        self.ottomans_button = tk.Button(
            self.country_selection_frame,
            text="Ottomans",
            command=lambda: self.select_country("Ottomans")
        )
        self.france_button = tk.Button(
            self.country_selection_frame,
            text="France",
            command=lambda: self.select_country("France")
        )
        self.country_confirmation_label = tk.Label(self.country_selection_frame, text = "")
        self.ottomans_button.pack()
        self.france_button.pack()
    def show_start_screen(self):
        self.show_only_frame(self.start_frame)
    def build_start_screen(self):
        self.new_game_button = tk.Button(
            self.start_frame,
            text="New Game",
            command=self.start_new_game
        )
        self.load_game_button = tk.Button(
            self.start_frame,
            text="Load Game",
            command=self.show_pre_loaded_game
        )
        self.exit_game_button = tk.Button(
            self.start_frame,
            text="Exit game",
            command=self.exit_game
        )
        self.new_game_button.pack()
        self.load_game_button.pack()
        self.exit_game_button.pack()
        self.show_start_screen()
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
    def build_game_screen(self):
        self.month_label = tk.Label(self.game_frame, text="Month: 0")
        self.chosen_country_label = tk.Label(self.game_frame, text = f"You are playing as {self.game.picked_country_name}")
        self.first_country_ducats = tk.Label(self.game_frame, text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats")
        self.second_country_ducats = tk.Label(self.game_frame, text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats")
        self.first_country_troops_label = tk.Label(self.game_frame, text = f"{self.countries[0].name} has {self.countries[0].troops} troops")
        self.second_country_troops_label = tk.Label(self.game_frame, text = f"{self.countries[1].name} has {self.countries[1].troops} troops")
        self.title_label = tk.Label(
            self.game_frame,
            text="Python EU4 Simulator"
        )
        self.next_month_button = tk.Button(
            self.game_frame,
            text="Next Month",
            command=self.next_month
        )
        self.title_label.pack()
        self.month_label.pack()
        self.first_country_ducats.pack()
        self.second_country_ducats.pack()
        self.first_country_troops_label.pack()
        self.second_country_troops_label.pack()
        self.next_month_button.pack()
    def build_advisor_screen(self):
        self.total_advisor_cost = 0
        self.mil_advisor_label = tk.Label(self.advisor_selection_frame, text = "Military Advisor:")
        self.dip_advisor_label = tk.Label(self.advisor_selection_frame, text = "Diplomatic Advisor:")
        self.admin_advisor_label = tk.Label(self.advisor_selection_frame, text = "Administrative Advisor:")
        self.continue_button_advisors = tk.Button(self.advisor_selection_frame, text = "Continue.", command=self.show_game_screen)
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
            command = self.update_advisor_cost
        )
        self.advisor_cost_label = tk.Label(self.advisor_selection_frame, text=f"Total monthly advisor cost: 0 ducats")
        self.mil_advisor_label.grid(row=0, column = 0)
        self.military_dropdown.grid(row=0, column=1)
        self.dip_advisor_label.grid(row=1, column = 0)
        self.diplomatic_dropdown.grid(row=1, column=1)
        self.admin_advisor_label.grid(row=2, column=0)
        self.administrative_dropdown.grid(row=2, column=1)
        self.advisor_cost_label.grid(row=3, column=0)
        self.continue_button_advisors.grid(row=4, column=0)
    def show_only_frame(self, frame_to_show):
        for frame in self.frames:
            frame.pack_forget()
        frame_to_show.pack()
    def show_pre_loaded_game(self):
        for widget in self.pre_load_frame.winfo_children():
            widget.destroy()
        saves = self.save_rep.list_saves()
        if len(saves) == 0:
            no_saves_explanation = tk.Label(
                self.pre_load_frame,
                text="You have no existing saves to load."
            )
            go_back_button = tk.Button(
                self.pre_load_frame,
                text="Back",
                command=self.show_start_screen
            )
            no_saves_explanation.pack()
            go_back_button.pack()
        for index, save in enumerate(saves, start=1):
            save_id, save_name, player_country, month = save
            button_text = f"{index}: {save_name} - {player_country} - Month {month}"
            save_button = tk.Button(
                self.pre_load_frame,
                text=button_text,
                command=lambda chosen_save_id=save_id: self.show_loaded_game(chosen_save_id)
            )
            delete_button = tk.Button(
                self.pre_load_frame,
                text=f"Delete save {index}",
                command=lambda chosen_save_id=save_id: self.show_delete_save(chosen_save_id)
            )
            save_button.pack()
            delete_button.pack()
        self.show_only_frame(self.pre_load_frame)
    def show_delete_save(self, save_id):
        self.save_rep.delete_save(save_id)
        self.show_pre_loaded_game()
    def show_pre_saved_game(self):
        self.show_only_frame(self.pre_save_frame)
    def show_loaded_game(self, save_id):
        self.countries, self.game = self.save_rep.load_game(save_id)
        self.refresh_display()
        self.chosen_country_label.pack()
        self.can_pause = True
        self.show_only_frame(self.game_frame)
    def get_player_country(self):
        for country in self.countries:
            if country.name == self.game.picked_country_name:
                return country
    def next_month(self):
        self.game.advance_month(self.countries)
        self.refresh_display()
        if self.game.months_passed % 12 == 0:
            self.show_event_screen()
        elif self.game.months_passed % 6 == 0:
            self.show_recruitment_screen()
    def show_recruitment_screen(self):
        self.can_pause = False
        self.show_only_frame(self.recruitment_frame)
    def show_recruitment_if_yes(self):
        self.recruitment_button.pack_forget()
        self.recruitment_cancel_button.pack_forget()
        self.recruitment_question.pack()
        self.recruitment_entry.pack()
        self.recruitment_entry_submit_button.pack()
    def show_pause_menu(self, event=None):
        if not self.can_pause:
            return
        self.show_only_frame(self.pause_menu_frame)
    def continue_game_from_pause_menu(self):
        self.show_only_frame(self.game_frame)
    def pause_menu_save(self):
        chosen_save_name = self.save_name_input.get()
        self.save_rep.save_game(chosen_save_name, self.game, self.countries)
        self.show_only_frame(self.game_frame)
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
    def refresh_display(self):
        self.month_label.config(text=f"Month: {self.game.months_passed}")
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.first_country_ducats.config(text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats")
        self.second_country_ducats.config(text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats")
        self.first_country_troops_label.config(text=f"{self.countries[0].name} has {self.countries[0].troops} troops")
        self.second_country_troops_label.config(text=f"{self.countries[1].name} has {self.countries[1].troops} troops")
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
        self.advisor_cost_label.config(text=f"The total advisor cost for your country is: {self.total_advisor_cost}")
    def show_game_screen(self):
        self.game.monthly_advisor_expenses = self.total_advisor_cost
        self.chosen_country_label.config(
            text=f"You are playing as {self.game.picked_country_name}"
        )
        self.chosen_country_label.pack()
        self.show_only_frame(self.game_frame)
        self.can_pause = True
    def start_new_game(self):
        self.show_only_frame(self.country_selection_frame)
    def exit_game(self):
        self.window.destroy()
    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    weaker_country = Country(
        "France",
        4.0,
        "100%",
        10000,
        {"mil": 3, "dip": 3, "admin": 3},
        200,
        0
    )
    stronger_country = Country(
        "Ottomans",
        5.0,
        "110%",
        40000,
        {"mil": 5, "dip": 3, "admin": 3},
        700,
        0
    )
    countries = [weaker_country, stronger_country]
    test_save = Game()
    test_save.picked_country_name = "StrongCountry"
    test_save.monthly_advisor_expenses = 0
    gui = GameGUI(test_save, countries)
    gui.run()
