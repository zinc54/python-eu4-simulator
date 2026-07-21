import unittest
import os
import json
import tempfile

from country import Country
from battle import Battle
from game import Game
from event_system import EventSystem
from save_repository import SaveRepository
from country_data_loader import CountryDataLoader
from ai_controller import AIController
from game_event import GameEvent

class CountryTests(unittest.TestCase):
    def test_discipline_conversion(self):
        country = Country(
            "Testland",
            3,
            "105%",
            0,
            {"mil": 3, "dip": 3, "admin": 3},
            50,
            0
        )

        self.assertEqual(country.discipline, 1.05)

    def test_damage_calculation(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        self.assertEqual(country.calculate_damage(), 10000)
    def test_recruiting(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        old_monthly_costs = country.monthly_expenses
        country.recruit_troops(5)
        self.assertEqual(country.monthly_expenses - old_monthly_costs, 1)
        self.assertEqual(country.troops, 15000)
        self.assertEqual(country.ducats, 50)
        self.assertEqual(country.recruit_troops("bruh"), "invalid_input")
        self.assertEqual(country.recruit_troops(-2), "invalid_amount")
        self.assertEqual(country.recruit_troops(999), "too_expensive")
    def test_monthly_economy_processing(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        ducats_before = country.ducats
        advisor_costs = 3
        # -3 ducats every month for advisors and -2 every month for soldiers
        country.process_monthly_economy(
            advisor_costs,
            country.name,
            0,
        )
        self.assertEqual(ducats_before - country.ducats, 5)
    def test_loan_processing(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            105,
            0
        )
        interest_before = country.monthly_interest_payments
        advisor_costs = 80
        event_log = country.process_monthly_economy(
            advisor_costs,
            country.name,
            0,
        )
        self.assertEqual(event_log[0].category, "loan")
        self.assertEqual(event_log[0].actor_name, country.name)
        self.assertEqual(event_log[0].month, 1)
        self.assertEqual(country.loans, 2)
        self.assertEqual(country.monthly_interest_payments - interest_before, 0.5)
        self.assertEqual(country.ducats, 73)
class BattleTests(unittest.TestCase):
    def setUp(self):
        self.weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        self.stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )

    def test_battles(self):
        weak_morale_before = self.weaker_country.morale
        strong_morale_before = self.stronger_country.morale
        weak_troops_before = self.weaker_country.troops
        strong_troops_before = self.stronger_country.troops
        test_battle = Battle(self.stronger_country, self.weaker_country)
        test_battle.resolve_battle()
        # Attacker does 66000 damage here.
        # Defender does 8000 damage here.
        self.assertTrue(test_battle.attacker_won)
        self.assertAlmostEqual(strong_morale_before - self.stronger_country.morale, 0.2)
        self.assertAlmostEqual(weak_morale_before - self.weaker_country.morale, 1)
        self.assertAlmostEqual(weak_troops_before - self.weaker_country.troops, 6600)
        self.assertAlmostEqual(strong_troops_before - self.stronger_country.troops, 8000 / 30)
    def test_battles_below_zero(self):
        zero_test_weak_country = self.weaker_country
        zero_test_strong_country = self.stronger_country
        zero_test_weak_country.troops = -5000
        zero_test_weak_country.morale = -4
        zero_test_battle = Battle(zero_test_weak_country, zero_test_strong_country)
        zero_test_battle.resolve_battle()
        self.assertGreaterEqual(zero_test_weak_country.troops, 0)
        self.assertGreaterEqual(zero_test_weak_country.morale, 0)
class GameFileTests(unittest.TestCase):
    def setUp(self):
        self.weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        self.stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        self.original_countries = [self.weaker_country, self.stronger_country]

    def test_month_passing(self):
        test_save = Game()
        test_save.picked_country_name = "Ottomans"
        test_save.monthly_advisor_expenses = 1
        for i in range(12):
            test_save.advance_month(self.original_countries)
        self.assertEqual(test_save.months_passed, 12)
        self.assertEqual(self.weaker_country.ducats, 76)
        self.assertEqual(self.stronger_country.ducats, 192)
    def test_event(self):
        event_sys = EventSystem()
        # Ducats of stronger country needs to be reduced by 50 ducats and the income raised by 2.
        old_ducats = self.stronger_country.ducats
        old_income = self.stronger_country.income
        event_sys.apply_event_choice(self.stronger_country, "We need to invest long term!")
        self.assertEqual(old_ducats - self.stronger_country.ducats, 50)
        self.assertEqual(self.stronger_country.income - old_income, 2)
    def test_sql_loading_saving(self):
        test_save_sql = Game()
        test_sql_system = SaveRepository(":memory:")
        test_save_sql.picked_country_name = "Ottomans"
        testing_save_id = test_sql_system.save_game("Testing module Save", test_save_sql, self.original_countries)
        loaded_countries, loaded_game_sql = test_sql_system.load_game(testing_save_id)
        for i in range(0, 2):
            self.assertEqual(loaded_game_sql.picked_country_name, test_save_sql.picked_country_name)
            self.assertEqual(loaded_game_sql.monthly_advisor_expenses, test_save_sql.monthly_advisor_expenses)
            self.assertEqual(loaded_game_sql.months_passed,  test_save_sql.months_passed)
            self.assertEqual(loaded_countries[i].name, self.original_countries[i].name)
            self.assertEqual(loaded_countries[i].morale, self.original_countries[i].morale)
            self.assertEqual(loaded_countries[i].discipline, self.original_countries[i].discipline)
            self.assertEqual(loaded_countries[i].troops, self.original_countries[i].troops)
            self.assertEqual(loaded_countries[i].technology, self.original_countries[i].technology)
            self.assertEqual(loaded_countries[i].ducats, self.original_countries[i].ducats)
            self.assertEqual(loaded_countries[i].income, self.original_countries[i].income)
            self.assertEqual(loaded_countries[i].monthly_interest_payments, self.original_countries[i].monthly_interest_payments)
            self.assertEqual(loaded_countries[i].loans, self.original_countries[i].loans)            

    def test_sql_delete_save(self):
        test_save_sql = Game()
        test_sql_system = SaveRepository(":memory:")
        test_save_sql.picked_country_name = "Ottomans"
        first_save_id = test_sql_system.save_game("First Save", test_save_sql, self.original_countries)
        second_save_id = test_sql_system.save_game("Second Save", test_save_sql, self.original_countries)

        test_sql_system.delete_save(first_save_id)
        remaining_saves = test_sql_system.list_saves()

        self.assertEqual(len(remaining_saves), 1)
        self.assertEqual(remaining_saves[0][0], second_save_id)
    def test_month_action_events(self):
        game = Game()

        game.months_passed = 12
        self.assertEqual(game.get_month_action(), "event")

        game.months_passed = 6
        self.assertEqual(game.get_month_action(), "recruitment")

        game.months_passed = 7
        self.assertEqual(game.get_month_action(), "continue")
    def test_valid_data_loads_correctly(self):
        test_data = {
            "country_data": {
                "Testland": {
                    "name": "Testland",
                    "morale": 4.0,
                    "discipline": "100%",
                    "troops": 10000,
                    "technology": {"mil": 3, "dip": 3, "admin": 3},
                    "ducats": 200,
                    "income": 0,
                }
            },
            "map_data": {
                "Testland": {
                    "x1": 100,
                    "y1": 100,
                    "x2": 200,
                    "y2": 200,
                    "color": "blue",
                }
            },
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as test_file:
            json.dump(test_data, test_file)
            test_filename = test_file.name
        self.addCleanup(os.unlink, test_filename)
        loader = CountryDataLoader(test_filename)
        country_data, map_data = loader.load_countries_data()
        self.assertEqual(len(country_data), 1)
        self.assertEqual(country_data[0].name, "Testland")
        self.assertEqual(country_data[0].troops, 10000)
        self.assertEqual(map_data["Testland"]["color"], "blue")
    def test_missing_required_field_raises(self):
        missing_field_test_data = {
            "country_data": {
                "Testland": {
                    "name": "Testland",
                    "morale": 4.0,
                    "troops": 10000,
                    "technology": {"mil": 3, "dip": 3, "admin": 3},
                    "ducats": 200,
                    "income": 0,
                }
            },
            "map_data": {
                "Testland": {
                    "x1": 100,
                    "y1": 100,
                    "x2": 200,
                    "y2": 200,
                    "color": "blue",
                }
            },
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as test_file_two:
            json.dump(missing_field_test_data, test_file_two)
            test_filename = test_file_two.name
        self.addCleanup(os.unlink, test_filename)

        with self.assertRaises(ValueError):
            CountryDataLoader(test_filename)
    def test_map_data_country_mismatch_raises(self):
        name_mismatch_test_data = {
            "country_data": {
                "Testland": {
                    "name": "Testland",
                    "morale": 4.0,
                    "discipline": "100%",
                    "troops": 10000,
                    "technology": {"mil": 3, "dip": 3, "admin": 3},
                    "ducats": 200,
                    "income": 0,
                }
            },
            "map_data": {
                "Otherland": {
                    "x1": 100,
                    "y1": 100,
                    "x2": 200,
                    "y2": 200,
                    "color": "blue",
                }
            },
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as test_file_three:
            json.dump(name_mismatch_test_data, test_file_three)
            test_filename = test_file_three.name
        self.addCleanup(os.unlink, test_filename)
        with self.assertRaises(ValueError):
            CountryDataLoader(test_filename)
class AIControllerTests(unittest.TestCase):
    def setUp(self):
        self.ai_controller = AIController()
        self.ai_country = Country(
            "AI Country",
            4.0,
            "105%",
            20000,
            {"mil": 4, "dip": 3, "admin": 3},
            300,
            5,
            charge_upfront=False,
        )
        self.weak_target = Country(
            "Weak Target",
            2.5,
            "95%",
            8000,
            {"mil": 3, "dip": 3, "admin": 3},
            100,
            2,
            charge_upfront=False,
        )
        self.strong_target = Country(
            "Strong Target",
            5.0,
            "110%",
            30000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            15,
            charge_upfront=False,
        )
        self.possible_targets = [self.strong_target, self.weak_target]

    def test_recruits_when_army_is_small_and_country_is_wealthy(self):
        self.ai_country.troops = 8000
        self.ai_country.ducats = 600
        returned_data, event_log = self.ai_controller.choose_action(self.ai_country, self.possible_targets)
        self.assertEqual(returned_data.action, "recruit")
        self.assertEqual(returned_data.recruit_stacks, 3)
        self.assertIsNone(returned_data.target)
        self.assertEqual(event_log[0].category, "recruitment")
        self.assertEqual(event_log[0].actor_name, self.ai_country.name)
    def test_attacks_when_much_stronger_than_target(self):
        self.ai_country.troops = 40000
        returned_data, event_log = self.ai_controller.choose_action(self.ai_country, self.possible_targets)
        self.assertEqual(returned_data.action, "attack")
        self.assertEqual(event_log[0].category, "battle")
        self.assertEqual(event_log[0].actor_name, self.ai_country.name)
        self.assertIs(returned_data.target, self.weak_target)
    def test_waits_when_no_other_action_is_suitable(self):
        self.ai_country.troops = 10000
        self.ai_country.ducats = 300
        returned_data, event_log = self.ai_controller.choose_action(self.ai_country, self.possible_targets)
        self.assertEqual(event_log, [])
        self.assertEqual(returned_data.action, "wait")
    def test_waits_when_no_targets_exist(self):
        returned_data, event_log = self.ai_controller.choose_action(self.ai_country, [])
        self.assertEqual(event_log, [])
        self.assertEqual(returned_data.action, "wait")
        self.assertIsNone(returned_data.target)
        self.assertEqual(returned_data.recruit_stacks, 0)
class EventLogTests(unittest.TestCase):
    def setUp(self):
        self.event_log_test_game = Game()
        self.ai_controller = AIController()
        self.mid_country = Country(
            "Mid Country",
            4.0,
            "105%",
            20000,
            {"mil": 4, "dip": 3, "admin": 3},
            300,
            5,
            charge_upfront=False,
        )
        self.weak_target = Country(
            "Weak Target",
            2.5,
            "95%",
            8000,
            {"mil": 3, "dip": 3, "admin": 3},
            100,
            2,
            charge_upfront=False,
        )
        self.strong_target = Country(
            "Strong Target",
            5.0,
            "110%",
            30000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            15,
            charge_upfront=False,
        )
        self.countries = [self.mid_country, self.weak_target, self.strong_target]
    def test_game_event_collection(self):
        self.event_log_test_game.advance_month(self.countries)
        old_event_log_length = len(self.event_log_test_game.event_log)
        self.assertGreater(old_event_log_length, 0)
        self.assertTrue(
            all(isinstance(event, GameEvent) for event in self.event_log_test_game.event_log)
        )
        self.assertTrue(
            all(event.month == 1 for event in self.event_log_test_game.event_log)
        )
        self.event_log_test_game.advance_month(self.countries)
        self.assertGreater(len(self.event_log_test_game.event_log), old_event_log_length)
if __name__ == "__main__":
    unittest.main()
