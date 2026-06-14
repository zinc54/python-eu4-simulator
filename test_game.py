import unittest
from unittest.mock import patch
from country import Country
from battle import Battle
from game import Game
from event_system import EventSystem

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
        country.process_monthly_economy(advisor_costs, country.name)
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
        country.process_monthly_economy(advisor_costs, country.name)
        self.assertEqual(country.loans, 2)
        self.assertEqual(country.monthly_interest_payments - interest_before, 0.5)
        self.assertEqual(country.ducats, 73)
class BattleTests(unittest.TestCase):
    def test_battles(self):
        weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        weak_morale_before = weaker_country.morale
        strong_morale_before = stronger_country.morale
        weak_troops_before = weaker_country.troops
        strong_troops_before = stronger_country.troops
        test_battle = Battle(stronger_country, weaker_country)
        test_battle.resolve_battle()
        # Attacker does 66000 damage here.
        # Defender does 8000 damage here.
        self.assertTrue(test_battle.attacker_won)
        self.assertAlmostEqual(strong_morale_before - stronger_country.morale, 0.2)
        self.assertAlmostEqual(weak_morale_before - weaker_country.morale, 1)
        self.assertAlmostEqual(weak_troops_before - weaker_country.troops, 6600)
        self.assertAlmostEqual(strong_troops_before - stronger_country.troops, 8000 / 30)
class GameFileTests(unittest.TestCase):
    def test_month_passing(self):
        weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        test_save = Game()
        test_save.picked_country_name = "Ottomans"
        test_save.monthly_advisor_expenses = 1
        countries = [weaker_country, stronger_country]
        for i in range(12):
            test_save.advance_month(countries)
        self.assertEqual(test_save.months_passed, 12)
        self.assertEqual(weaker_country.ducats, 76)
        self.assertEqual(stronger_country.ducats, 192)
    def test_saving(self):
        weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        original_countries = [weaker_country, stronger_country]
        test_save = Game()
        test_save.picked_country_name = "Ottomans"
        test_save.monthly_advisor_expenses = 14
        test_save.months_passed = 12
        stronger_country.recruit_troops(2)
        test_save.save_game(original_countries, True)
        loaded_countries = []
        loaded_countries = test_save.load_game(True)
        for i in range(0, 2):
            self.assertEqual(test_save.picked_country_name, "Ottomans")
            self.assertEqual(test_save.monthly_advisor_expenses, 14)
            self.assertEqual(test_save.months_passed, 12)
            self.assertEqual(loaded_countries[i].name, original_countries[i].name)
            self.assertEqual(loaded_countries[i].morale, original_countries[i].morale)
            self.assertEqual(loaded_countries[i].discipline, original_countries[i].discipline)
            self.assertEqual(loaded_countries[i].troops, original_countries[i].troops)
            self.assertEqual(loaded_countries[i].technology, original_countries[i].technology)
            self.assertEqual(loaded_countries[i].ducats, original_countries[i].ducats)
            self.assertEqual(loaded_countries[i].income, original_countries[i].income)
            self.assertEqual(loaded_countries[i].monthly_interest_payments, original_countries[i].monthly_interest_payments)
            self.assertEqual(loaded_countries[i].loans, original_countries[i].loans)
    def test_event(self):
        weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        original_countries = [weaker_country, stronger_country]
        test_save = Game()
        event_sys = EventSystem()
        # Ducats of stronger country needs to be reduced by 50 ducats and the income raised by 2.
        old_ducats = stronger_country.ducats
        old_income = stronger_country.income
        event_sys.apply_event_choice(stronger_country, "We need to invest long term!")
        self.assertEqual(old_ducats - stronger_country.ducats, 50)
        self.assertEqual(stronger_country.income - old_income, 2)
    def test_pause_menu(self):
        test_save = Game()
        weaker_country = Country(
            "France",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        stronger_country = Country(
            "Ottomans",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0
        )
        original_countries = [weaker_country, stronger_country]
        input_one_result = test_save.pause_menu(1, original_countries, True)
        self.assertEqual(input_one_result, None)
        test_save.picked_country_name = "Ottomans"
        test_save.monthly_advisor_expenses = 14
        test_save.months_passed = 12
        stronger_country.recruit_troops(2)
        test_save.pause_menu(2, original_countries, True)
        loaded_countries = []
        loaded_countries = test_save.pause_menu(3, original_countries, True)
        for i in range(0, 2):
            self.assertEqual(test_save.picked_country_name, "Ottomans")
            self.assertEqual(test_save.monthly_advisor_expenses, 14)
            self.assertEqual(test_save.months_passed, 12)
            self.assertEqual(loaded_countries[i].name, original_countries[i].name)
            self.assertEqual(loaded_countries[i].morale, original_countries[i].morale)
            self.assertEqual(loaded_countries[i].discipline, original_countries[i].discipline)
            self.assertEqual(loaded_countries[i].troops, original_countries[i].troops)
            self.assertEqual(loaded_countries[i].technology, original_countries[i].technology)
            self.assertEqual(loaded_countries[i].ducats, original_countries[i].ducats)
            self.assertEqual(loaded_countries[i].income, original_countries[i].income)
            self.assertEqual(loaded_countries[i].monthly_interest_payments, original_countries[i].monthly_interest_payments)
            self.assertEqual(loaded_countries[i].loans, original_countries[i].loans)
        with self.assertRaises(SystemExit):
            test_save.pause_menu(4, original_countries, True)
        self.assertFalse(test_save.running)

if __name__ == "__main__":
    unittest.main()
