from src.game import Game
from src.tech_tree import make_tech_tree
from src.star import Star
from src.planet import Planet, planet_environments
from src.name_generator import generate_name_list, generate_prefix_list
from src.roman import int_to_roman

from random import Random

class StandardGameFactory:
    def __init__(self, seed: int | None = None):
        self.random = Random(seed)

    def _get_closest_star(self, star: Star, stars: list[Star]) -> Star | None:
        closest_star: Star | None = None
        closest_distance: float = float("inf")

        for other_star in stars:
            if other_star == star:
                continue

            distance = ((star.coordinates[0] - other_star.coordinates[0]) ** 2 + (star.coordinates[1] - other_star.coordinates[1]) ** 2) ** 0.5
            if distance < closest_distance:
                closest_distance = distance
                closest_star = other_star

        return closest_star

    def create_game(self) -> Game:
        starmap = []
        cluster_names = generate_name_list(self.random.randint(4, 20), self.random)
        current_coordinates = (0, 0)
        for cluster_name in cluster_names:
            prefixes = generate_prefix_list(self.random.randint(1, 10), self.random)
            for prefix in prefixes:
                x_direction = self.random.randint(0, 1) * 2 - 1
                y_direction = self.random.randint(0, 1) * 2 - 1
                x_increase = x_direction * self.random.randint(10, 20)
                y_increase = y_direction * self.random.randint(10, 20)
                current_coordinates = (current_coordinates[0] + x_increase, current_coordinates[1] + y_increase)

                planets = [Planet(f"{prefix} {cluster_name} {int_to_roman(index + 1)}", self.random.choice(planet_environments)) for index in range(self.random.randint(0, 5))]
                new_star = Star(f"{prefix} {cluster_name}", current_coordinates, planets)

                closest_star = self._get_closest_star(new_star, starmap)
                if closest_star:
                    new_star.star_lane_connections.append(closest_star)
                    closest_star.star_lane_connections.append(new_star)
                starmap.append(new_star)
                
        return Game(starmap, make_tech_tree())

    def create_homeplanet(self, game: Game) -> Planet:
        homestar = None
        while not homestar:
            star = self.random.choice(game.starmap)
            if star.planets:
                homestar = star

        return self.random.choice(homestar.planets)