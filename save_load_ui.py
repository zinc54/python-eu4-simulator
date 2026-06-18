import tkinter as tk


class SaveLoadUI:
    def __init__(
        self,
        save_repository,
        pre_load_frame,
        pre_save_frame,
        show_only_frame,
        show_start_screen,
        show_game_frame,
        set_loaded_game,
        get_game_state,
        create_button
    ):
        self.save_rep = save_repository
        self.pre_load_frame = pre_load_frame
        self.pre_save_frame = pre_save_frame
        self.show_only_frame = show_only_frame
        self.show_start_screen = show_start_screen
        self.show_game_frame = show_game_frame
        self.set_loaded_game = set_loaded_game
        self.get_game_state = get_game_state
        self.create_button = create_button

        self.save_name_input = tk.Entry(self.pre_save_frame)
        self.save_name_input.pack()
        self.create_button(
            self.pre_save_frame,
            "Save Game",
            self.save_current_game
        )

    def show_load_screen(self):
        for widget in self.pre_load_frame.winfo_children():
            widget.destroy()

        saves = self.save_rep.list_saves()
        if len(saves) == 0:
            no_saves_explanation = tk.Label(
                self.pre_load_frame,
                text="You have no existing saves to load."
            )
            no_saves_explanation.pack()
            self.create_button(
                self.pre_load_frame,
                "Back",
                self.show_start_screen
            )

        for index, save in enumerate(saves, start=1):
            save_id, save_name, player_country, month = save
            button_text = f"{index}: {save_name} - {player_country} - Month {month}"
            self.create_button(
                self.pre_load_frame,
                button_text,
                lambda chosen_save_id=save_id: self.load_selected_game(chosen_save_id)
            )
            self.create_button(
                self.pre_load_frame,
                f"Delete save {index}",
                lambda chosen_save_id=save_id: self.delete_save(chosen_save_id)
            )

        self.show_only_frame(self.pre_load_frame)

    def delete_save(self, save_id):
        self.save_rep.delete_save(save_id)
        self.show_load_screen()

    def show_save_screen(self):
        self.show_only_frame(self.pre_save_frame)

    def load_selected_game(self, save_id):
        loaded_countries, loaded_game = self.save_rep.load_game(save_id)
        self.set_loaded_game(loaded_game, loaded_countries)
        self.show_game_frame()

    def save_current_game(self):
        chosen_save_name = self.save_name_input.get()
        game, countries = self.get_game_state()
        self.save_rep.save_game(chosen_save_name, game, countries)
        self.show_game_frame()
