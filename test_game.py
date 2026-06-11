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
        self.assertEqual(country.calculateDamage(), 10000)
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
        oldMonthlyCosts = country.monthlyExpenses
        country.recruitTroops(5)
        self.assertEqual(country.monthlyExpenses - oldMonthlyCosts, 1)
        self.assertEqual(country.troops, 15000)
        self.assertEqual(country.ducats, 50)
    def test_monthlyEconomyProcessing(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        ducatsBefore = country.ducats
        advisorCosts = 3
        # -3 ducats every month for advisors and -2 every month for soldiers 
        country.processMonthlyEconomy(advisorCosts, country.name)
        self.assertEqual(ducatsBefore - country.ducats, 5)
    def test_loanProcessing(self):
        country = Country(
            "Testland",
            5.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            105,
            0
        )
        interestBefore = country.monthlyInterestPayments
        advisorCosts = 80
        country.processMonthlyEconomy(advisorCosts, country.name)
        self.assertEqual(country.loans, 2)
        self.assertEqual(country.monthlyInterestPayments - interestBefore, 0.5)
        self.assertEqual(country.ducats, 73)
class BattleTests(unittest.TestCase):
    def test_battles(self):
        weakerCountry = Country(
            "WeakCountry",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        strongerCountry = Country(
            "StrongCountry",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0           
        )
        weakMoraleBefore = weakerCountry.morale
        strongMoraleBefore = strongerCountry.morale
        weakTroopsBefore = weakerCountry.troops
        strongTroopsBefore = strongerCountry.troops
        testBattle = Battle(strongerCountry, weakerCountry)
        # Attacker does 66000 damage here.
        # Defender does 8000 damage here.
        self.assertTrue(testBattle.attackerWon)
        self.assertAlmostEqual(strongMoraleBefore - strongerCountry.morale, 0.2)
        self.assertAlmostEqual(weakMoraleBefore - weakerCountry.morale, 1)
        self.assertAlmostEqual(weakTroopsBefore - weakerCountry.troops, 6600)
        self.assertAlmostEqual(strongTroopsBefore - strongerCountry.troops, 8000 / 30)
class GameFileTests(unittest.TestCase):
    def test_monthPassing(self):
        weakerCountry = Country(
            "WeakCountry",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        strongerCountry = Country(
            "StrongCountry",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0           
        )
        testSave = Game()
        testSave.pickedCountryName = "StrongCountry"
        testSave.monthlyAdvisorExpenses = 1
        countries = [weakerCountry, strongerCountry]
        for i in range(12):
            testSave.advanceMonth(countries)    
        self.assertEqual(testSave.monthsPassed, 12)
        self.assertEqual(weakerCountry.ducats, 76)
        self.assertEqual(strongerCountry.ducats, 192)
    def test_Saving(self):
        weakerCountry = Country(
            "WeakCountry",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        strongerCountry = Country(
            "StrongCountry",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0           
        )
        originalCountries = [weakerCountry, strongerCountry]
        testSave = Game()
        testSave.pickedCountryName = "StrongCountry"
        testSave.monthlyAdvisorExpenses = 14
        testSave.monthsPassed = 12
        strongerCountry.recruitTroops(2)
        testSave.saveGame(originalCountries, True)
        loadedCountries = []
        loadedCountries = testSave.loadGame(True)
        for i in range(0, 2):
            self.assertEqual(testSave.pickedCountryName, "StrongCountry")
            self.assertEqual(testSave.monthlyAdvisorExpenses, 14)
            self.assertEqual(testSave.monthsPassed, 12)
            self.assertEqual(loadedCountries[i].name, originalCountries[i].name)
            self.assertEqual(loadedCountries[i].morale, originalCountries[i].morale)
            self.assertEqual(loadedCountries[i].discipline, originalCountries[i].discipline)
            self.assertEqual(loadedCountries[i].troops, originalCountries[i].troops)
            self.assertEqual(loadedCountries[i].technology, originalCountries[i].technology)
            self.assertEqual(loadedCountries[i].ducats, originalCountries[i].ducats)
            self.assertEqual(loadedCountries[i].income, originalCountries[i].income)
            self.assertEqual(loadedCountries[i].monthlyInterestPayments, originalCountries[i].monthlyInterestPayments)
            self.assertEqual(loadedCountries[i].loans, originalCountries[i].loans)
    def test_event(self):
        weakerCountry = Country(
            "WeakCountry",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        strongerCountry = Country(
            "StrongCountry",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0           
        )
        originalCountries = [weakerCountry, strongerCountry]
        testSave = Game()
        eventSys = EventSystem()
        # Ducats of stronger country needs to be reduced by 50 ducats and the income raised by 2.
        oldDucats = strongerCountry.ducats
        oldIncome = strongerCountry.income
        eventSys.applyEventChoice(strongerCountry, "We need to invest long term!")
        self.assertEqual(oldDucats - strongerCountry.ducats, 50)
        self.assertEqual(strongerCountry.income - oldIncome, 2)
    def test_pauseMenu(self):
        testSave = Game()
        weakerCountry = Country(
            "WeakCountry",
            4.0,
            "100%",
            10000,
            {"mil": 3, "dip": 3, "admin": 3},
            200,
            0
        )
        strongerCountry = Country(
            "StrongCountry",
            5.0,
            "110%",
            40000,
            {"mil": 5, "dip": 3, "admin": 3},
            700,
            0           
        )
        originalCountries = [weakerCountry, strongerCountry]
        inputOneResult = testSave.pauseMenu(1, originalCountries, True)
        self.assertEqual(inputOneResult, None)
        testSave.pickedCountryName = "StrongCountry"
        testSave.monthlyAdvisorExpenses = 14
        testSave.monthsPassed = 12
        strongerCountry.recruitTroops(2)
        testSave.pauseMenu(2, originalCountries, True)
        loadedCountries = []
        loadedCountries = testSave.pauseMenu(3, originalCountries, True)
        for i in range(0, 2):
            self.assertEqual(testSave.pickedCountryName, "StrongCountry")
            self.assertEqual(testSave.monthlyAdvisorExpenses, 14)
            self.assertEqual(testSave.monthsPassed, 12)
            self.assertEqual(loadedCountries[i].name, originalCountries[i].name)
            self.assertEqual(loadedCountries[i].morale, originalCountries[i].morale)
            self.assertEqual(loadedCountries[i].discipline, originalCountries[i].discipline)
            self.assertEqual(loadedCountries[i].troops, originalCountries[i].troops)
            self.assertEqual(loadedCountries[i].technology, originalCountries[i].technology)
            self.assertEqual(loadedCountries[i].ducats, originalCountries[i].ducats)
            self.assertEqual(loadedCountries[i].income, originalCountries[i].income)
            self.assertEqual(loadedCountries[i].monthlyInterestPayments, originalCountries[i].monthlyInterestPayments)
            self.assertEqual(loadedCountries[i].loans, originalCountries[i].loans)
        with self.assertRaises(SystemExit):
            testSave.pauseMenu(4, originalCountries, True)
        self.assertFalse(testSave.running)

if __name__ == "__main__":
    unittest.main()