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
    def refresh_events(self) -> None:
        events = self.get_event_log()

        self.event_text.config(state="normal")
        self.event_text.delete("1.0", tk.END)

        if not events:
            self.event_text.insert(tk.END, "No world events yet.")
        else:
            for event in events:
                event_line = f"Month {event.month}: {event.message}\n\n"
                self.event_text.insert(tk.END, event_line)

        self.event_text.config(state="disabled")
        self.event_text.see(tk.END)
    def show(self) -> None:
        self.refresh_events()

        self.panel.place(
            relx=0.96,
            rely=0.22,
            relwidth=0.35,
            relheight=0.55,
            anchor="ne",
        )
        self.panel.lift()
    def toggle(self) -> None:
        if self.panel.winfo_ismapped():
            self.hide()
        else:
            self.show()
    def hide(self) -> None:
        self.panel.place_forget()
