import tkinter as tk

class AdvisorUI:
    def __init__(
        self,
        advisor_selection_frame,
        game,
        show_only_frame,
        show_game_screen,
        set_can_pause
    ):
        self.advisor_selection_frame = advisor_selection_frame
        self.game = game
        self.show_only_frame = show_only_frame
        self.show_game_screen = show_game_screen
        self.set_can_pause = set_can_pause

    def set_game(self, game):
        self.game = game

    def show_advisor_screen(self):
        self.set_can_pause(False)
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
    def finish_advisor_selection(self):
        self.game.monthly_advisor_expenses = self.total_advisor_cost
        self.show_game_screen()
    def build_advisor_screen(self):
        self.total_advisor_cost = 0
        self.mil_advisor_label = tk.Label(self.advisor_selection_frame, text="Military Advisor:")
        self.dip_advisor_label = tk.Label(self.advisor_selection_frame, text="Diplomatic Advisor:")
        self.admin_advisor_label = tk.Label(self.advisor_selection_frame, text="Administrative Advisor:")
        self.continue_button_advisors = tk.Button(
            self.advisor_selection_frame,
            text="Continue.",
            command=self.finish_advisor_selection
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
