import sqlite3
from game import Game
from country import Country
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
        self.save_id = self.cursor.lastrowid
        for country in countries:
            self.cursor.execute(
                """
                INSERT INTO countries (save_id, name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.save_id,
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
        self.cursor.execute("SELECT * FROM countries")
        saves = self.cursor.fetchall()
        for save in saves:
            print(save)
        self.connection.commit()
    def load_game(self, save_id):
        self.loaded_game = Game()
        self.cursor.execute(
            """
            SELECT id, save_name, month, player_country, monthly_advisor_expenses
            FROM saves
            where id = ?
            """,
            (save_id,)
        )
        save_data = self.cursor.fetchone()
        save_id, _, month, player_country, monthly_advisor_expenses = save_data
        self.loaded_game.months_passed = month
        self.loaded_game.picked_country_name = player_country
        self.loaded_game.monthly_advisor_expenses = monthly_advisor_expenses
        print(save_data)
        self.cursor.execute(
            """
            SELECT name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans
            FROM countries 
            WHERE save_id = ?
            """,
            (save_id,)
        )
        loaded_countries = []
        country_rows = self.cursor.fetchall()
        for country in country_rows:
            name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans = country
            technology = {
                "mil": mil_tech,
                "dip": dip_tech,
                "admin": admin_tech
                }
            countryObject = Country(name, morale, discipline, troops, technology, ducats, income, False)
            countryObject.loans = loans
            countryObject.monthly_interest_payments = monthly_interest_payments
            loaded_countries.append(countryObject)
            print(country)
        return loaded_countries, self.loaded_game
    def list_saves(self):
        self.cursor.execute(
            """
            SELECT id, save_name, player_country, month
            FROM saves
            ORDER BY id
            """
        )
        return self.cursor.fetchall()