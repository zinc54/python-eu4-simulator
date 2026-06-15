import sqlite3

class SaveRepository:
    def __init__(self, database_name="eu4_saves.db"):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY,
                save_name TEXT,
                month INTEGER,
                player_country TEXT,
                monthly_advisor_expenses REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY,
                save_id INTEGER,
                name TEXT,
                morale REAL,
                discipline REAL,
                troops INTEGER,
                mil_tech INTEGER,
                dip_tech INTEGER,
                admin_tech INTEGER,
                ducats REAL,
                income REAL,
                monthly_interest_payments REAL,
                loans INTEGER,
                FOREIGN KEY (save_id) REFERENCES saves(id)
            )
        """)
    def close(self):
        self.connection.close()
    def save_game(self, save_name, game, countries):
        self.cursor.execute(
            """
            INSERT INTO saves (save_name, month, player_country, monthly_advisor_expenses)
            VALUES (?, ?, ?, ?)
            """,
            (save_name, game.months_passed, game.picked_country_name, game.monthly_advisor_expenses)
        )
        save_id = self.cursor.lastrowid
        for country in countries:
            self.cursor.execute(
                """
                INSERT INTO countries (save_id, name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    save_id,
                    country.name,
                    country.morale,
                    country.discipline,
                    country.troops,
                    country.technology["mil"],
                    country.technology["dip"],
                    country.technology["admin"],
                    country.ducats,
                    country.income,
                    country.monthly_interest_payments,
                    country.loans,
                )
            )
