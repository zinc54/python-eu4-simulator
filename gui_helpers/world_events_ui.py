import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class WorldEventsUI:
    def __init__(
        self,
        parent,
        get_event_log,
    ):
        self.parent = parent
        self.get_event_log = get_event_log

        self.panel = tk.Frame(
            self.parent,
            borderwidth=2,
            relief="raised",
            background="beige",
        )

        self.event_text = ScrolledText(
            self.panel,
            wrap=tk.WORD,
        )
        self.event_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        self.close_button = tk.Button(
            self.panel,
            text="Close",
            command=self.hide,
        )
        self.close_button.pack(pady=5)

    def hide(self) -> None:
        self.panel.place_forget()
