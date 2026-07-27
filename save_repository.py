import sqlite3
from game import Game
from country import Country
from game_event import GameEvent
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

                monarch_mil INTEGER,
                monarch_dip INTEGER,
                monarch_admin INTEGER,

                mil_advisor INTEGER,
                dip_advisor INTEGER,
                admin_advisor INTEGER,

                mil_points INTEGER,
                dip_points INTEGER,
                admin_points INTEGER,

                FOREIGN KEY (save_id) REFERENCES saves(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_events (
                id INTEGER PRIMARY KEY,
                save_id INTEGER,
                month INTEGER,
                actor_name TEXT,
                message TEXT,
                category TEXT,
                FOREIGN KEY (save_id) REFERENCES saves(id)
            )
        """)
        self.migrate_countries_table()
    def migrate_countries_table(self):
        required_new_columns = (
            "monarch_mil",
            "monarch_dip",
            "monarch_admin",
            "mil_advisor",
            "dip_advisor",
            "admin_advisor",
            "mil_points",
            "dip_points",
            "admin_points",
        )

        rows = self.cursor.execute(
            "PRAGMA table_info(countries)"
        ).fetchall()

        existing_columns = {
            row[1]
            for row in rows
        }
        for column_name in required_new_columns:
            if column_name not in existing_columns:
                self.cursor.execute(
                    f"""
                    ALTER TABLE countries
                    ADD COLUMN {column_name} INTEGER NOT NULL DEFAULT 0
                    """
                )
        self.connection.commit()
    def close(self):
        self.connection.close()
    def delete_save(self, save_id):
        self.cursor.execute(
            "DELETE FROM game_events WHERE save_id = ?",
            (save_id,)
        )
        self.cursor.execute(
            "DELETE FROM countries WHERE save_id = ?",
            (save_id,)
        )
        self.cursor.execute(
            "DELETE FROM saves WHERE id = ?",
            (save_id,)
        )
        self.connection.commit()
    def save_name_exists(self, save_name):
        self.cursor.execute(
            "SELECT save_name FROM saves WHERE save_name = ?",
            (save_name,)
        )
        existing_save_name = self.cursor.fetchone()
        if existing_save_name is None:
            return False
        else:
            return True
    def save_game(self, save_name, game, countries):
        event_log = game.event_log
        final_save_name = save_name
        number = 2
        while self.save_name_exists(final_save_name):
            final_save_name = f"{save_name}_{number}"
            number += 1
        self.cursor.execute(
            """
            INSERT INTO saves (save_name, month, player_country, monthly_advisor_expenses)
            VALUES (?, ?, ?, ?)
            """,
            (
                final_save_name,
                game.months_passed,
                game.picked_country_name,
                game.monthly_advisor_expenses,
            )
        )
        self.save_id = self.cursor.lastrowid
        for country in countries:
            self.cursor.execute(
                """
                INSERT INTO countries (save_id, name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans, monarch_mil, monarch_dip, monarch_admin, mil_advisor, dip_advisor, admin_advisor, mil_points, dip_points, admin_points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    country.monarch["mil"],
                    country.monarch["dip"],
                    country.monarch["admin"],
                    country.advisors["mil"],
                    country.advisors["dip"],
                    country.advisors["admin"],
                    country.monarch_points["mil"],
                    country.monarch_points["dip"],
                    country.monarch_points["admin"],
                )
            )
        for event in event_log:
            self.cursor.execute(
                """
                INSERT INTO game_events (save_id, month, actor_name, message, category)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.save_id,
                    event.month,
                    event.actor_name,
                    event.message,
                    event.category,
                )
            )
        self.connection.commit()
        return self.save_id
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
        self.cursor.execute(
            """
            SELECT name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans, monarch_mil, monarch_dip, monarch_admin, mil_advisor, dip_advisor, admin_advisor, mil_points, dip_points, admin_points
            FROM countries 
            WHERE save_id = ?
            """,
            (save_id,)
        )
        loaded_countries = []
        country_rows = self.cursor.fetchall()
        for country in country_rows:
            name, morale, discipline, troops, mil_tech, dip_tech, admin_tech, ducats, income, monthly_interest_payments, loans, monarch_mil, monarch_dip, monarch_admin, mil_advisor, dip_advisor, admin_advisor, mil_points, dip_points, admin_points = country
            technology = {
                "mil": mil_tech,
                "dip": dip_tech,
                "admin": admin_tech
                }
            monarch = {
                "mil": monarch_mil,
                "dip": monarch_dip,
                "admin": monarch_admin,
            }
            monarch_points = {
                "mil": mil_points,
                "dip": dip_points,
                "admin": admin_points,
            }
            advisors = {
                "mil": mil_advisor,
                "dip": dip_advisor,
                "admin": admin_advisor,
            }
            countryObject = Country(
                name,
                morale,
                discipline,
                troops,
                technology,
                ducats,
                income,
                charge_upfront=False,
                monarch=monarch,
                monarch_points=monarch_points,
                advisors=advisors,
            )
            countryObject.loans = loans
            countryObject.monthly_interest_payments = monthly_interest_payments
            loaded_countries.append(countryObject)
        self.cursor.execute(
            """
            SELECT month, actor_name, message, category
            FROM game_events
            WHERE save_id = ?
            ORDER BY id
            """,
            (save_id,)
        )
        loaded_game_events = []
        game_event_rows = self.cursor.fetchall()

        for event in game_event_rows:
            month, actor_name, message, category = event
            game_event_object = GameEvent(month, actor_name, message, category)
            loaded_game_events.append(game_event_object)

        self.loaded_game.event_log = loaded_game_events

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
