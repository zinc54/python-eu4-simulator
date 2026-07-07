import json 
from country import Country

class CountryDataLoader():
    def __init__(self):
        with open("countries.json", "r") as file:
            self.data = json.load(file)
        self.validate_country_data()
        self.validate_map_data()
    def validate_country_data(self):
        required_country_keys = [
            "name",
            "morale",
            "discipline",
            "troops",
            "technology",
            "ducats",
            "income",
        ]
        if "country_data" not in self.data:
            raise ValueError("countries.json is missing country_data")
        if "map_data" not in self.data:
            raise ValueError("countries.json is missing map_data")
        for country_name, country_data in self.data["country_data"].items():
            for key in required_country_keys:
                if key not in country_data:
                    raise ValueError(f"{country_name} is missing {key}")
    def validate_map_data(self):
        required_map_keys = ["x1", "y1", "x2", "y2", "color"]
        for country_name in self.data["country_data"]:
            if country_name not in self.data["country_data"]:
                raise ValueError(f"{country_name} has map_data but no country_data")
            if country_name not in self.data["map_data"]:
                raise ValueError(f"{country_name} is missing map_data")
        for country_name, country_map_data in self.data["map_data"].items():
            for key in required_map_keys:
                if key not in country_map_data:
                    raise ValueError(f"{country_name} doesn't have the {key} in its map_data")
    def load_countries_data(self):
        countries_data_list = []
        for country in self.data["country_data"]:
            country_object = Country(
                self.data["country_data"][country]["name"],
                self.data["country_data"][country]["morale"],
                self.data["country_data"][country]["discipline"],
                self.data["country_data"][country]["troops"],
                self.data["country_data"][country]["technology"],
                self.data["country_data"][country]["ducats"],
                self.data["country_data"][country]["income"]
                )
            countries_data_list.append(country_object)
        map_data = self.data["map_data"]
        return countries_data_list, map_data
