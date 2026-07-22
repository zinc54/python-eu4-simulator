import tkinter as tk
class RecruitmentUI:
    def __init__(
            self,
            recruitment_frame,
            show_only_frame,
            show_game_frame,
            get_player_country,
            recruit_player_troops,
            refresh_display,
            create_button,
            set_can_pause,
    ):
        self.recruitment_frame = recruitment_frame
        self.show_only_frame = show_only_frame
        self.show_game_frame = show_game_frame
        self.get_player_country = get_player_country
        self.recruit_player_troops = recruit_player_troops
        self.refresh_display = refresh_display
        self.create_button = create_button
        self.set_can_pause = set_can_pause
        self.build_recruiting_screen()
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
    def show_recruitment_screen(self):
        self.set_can_pause(False)
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
        result = self.recruit_player_troops(country, requested_stacks)
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
        self.show_game_frame()
        self.refresh_display()
        self.set_can_pause(True)
