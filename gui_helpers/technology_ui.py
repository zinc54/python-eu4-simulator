import tkinter as tk
from tkinter import messagebox, ttk

class TechnologyUI:
    def __init__(
        self,
        technology_frame,
        show_only_frame,
        show_game_frame,
        get_player_country,
        create_button,
    ):
        self.technology_frame = technology_frame
        self.show_only_frame = show_only_frame
        self.show_game_frame = show_game_frame
        self.get_player_country = get_player_country
        self.create_button = create_button
        self.build_technology_screen()

    def build_technology_screen(self):
        self.military_button = tk.Button(
            self.technology_frame,
            text="Military Technology",
            width=35,
            height=4,
            command=lambda: self.attempt_upgrade("mil"),
        )
        self.military_progress_bar = ttk.Progressbar(
            self.technology_frame,
            maximum=100,
            length=300,
            mode="determinate",
        )
        self.diplomatic_button = tk.Button(
            self.technology_frame,
            text="Diplomatic Technology",
            width=35,
            height=4,
            command=lambda: self.attempt_upgrade("dip"),
        )
        self.diplomatic_progress_bar = ttk.Progressbar(
            self.technology_frame,
            maximum=100,
            length=300,
            mode="determinate",
        )
        self.admin_button = tk.Button(
            self.technology_frame,
            text="Administrative Technology",
            width=35,
            height=4,
            command=lambda: self.attempt_upgrade("admin"),
        )
        self.admin_progress_bar = ttk.Progressbar(
            self.technology_frame,
            maximum=100,
            length=300,
            mode="determinate",
        )

        self.military_button.pack(padx=20, pady=(15, 4))
        self.military_progress_bar.pack(pady=(0, 10))
        self.diplomatic_button.pack(padx=20, pady=(5, 4))
        self.diplomatic_progress_bar.pack(pady=(0, 10))
        self.admin_button.pack(padx=20, pady=(5, 4))
        self.admin_progress_bar.pack(pady=(0, 10))
        self.create_button(
            self.technology_frame,
            "Back",
            self.show_game_frame,
        )

    def show_technology_screen(self):
        self.refresh_technology_display()
        self.show_only_frame(self.technology_frame)

    def refresh_technology_display(self):
        country = self.get_player_country()

        if country is None:
            return

        self.military_button.config(
            text=f"Military Technology - Level {country.technology['mil']}"
        )
        self.diplomatic_button.config(
            text=f"Diplomatic Technology - Level {country.technology['dip']}"
        )
        self.admin_button.config(
            text=f"Administrative Technology - Level {country.technology['admin']}"
        )

        military_progress = country.calculate_technology_progress("mil")
        diplomatic_progress = country.calculate_technology_progress("dip")
        admin_progress = country.calculate_technology_progress("admin")

        if isinstance(military_progress, float):
            self.military_progress_bar["value"] = military_progress
        if isinstance(diplomatic_progress, float):
            self.diplomatic_progress_bar["value"] = diplomatic_progress
        if isinstance(admin_progress, float):
            self.admin_progress_bar["value"] = admin_progress

    def attempt_upgrade(self, power_type):
        country = self.get_player_country()
        if country is None:
            return

        result = country.upgrade_technology(power_type)
        if result == "not_enough_points":
            self.refresh_technology_display()
            messagebox.showinfo(
                "Not Enough Monarch Points",
                "You do not have enough monarch points to buy this technology.",
                parent=self.technology_frame,
            )
        elif result == "success":
            self.refresh_technology_display()
            messagebox.showinfo(
                "Technology Upgraded",
                f"Successfully upgraded {power_type} technology!",
                parent=self.technology_frame,
            )