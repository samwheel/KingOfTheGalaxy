from flask import Flask, jsonify
from flask_cors import CORS

from src.planet import Planet, planet_environments
from src.star import Star
from rich import print
from src.tech_tree import make_tech_tree
from src.technology import Technology
from src.name_generator import generate_name, train_model, read_names
from random import randint, choice, choices
from src.roman import int_to_roman

def get_closest_star(star: Star, stars: list[Star]) -> Star | None:
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

def get_unconnected_stars(star, stars: list[Star]) -> list[Star]:
    return [other_star for other_star in stars if other_star != star and other_star not in star.star_lane_connections]

tech_tree: list[Technology] = make_tech_tree()

starmap: list[Star] = []
star_name_examples = read_names("src/star_names.txt")
star_name_model = train_model(star_name_examples, order=2)
cluster_names = [generate_name(star_name_model, order=2, min_len=3, max_len=8) for _ in range(randint(1, 10))]

star_clusters: list[list[Star]] = []

cluster_coordinates = (0, 0)
for cluster_name in cluster_names:
    cluster_coordinates = (cluster_coordinates[0] + randint(-100, 100), cluster_coordinates[1] + randint(-100, 100))
    index_string = "αβεγλμηξδνθω"
    index_offset: int = randint(0, len(index_string) - 1)
    star_cluster: list[Star] = []
    for index in range(randint(1, 7)):
        star_name: str = f"{index_string[(index + index_offset) % len(index_string)]} {cluster_name}"
        star_coordinates: tuple[int, int] = (cluster_coordinates[0] + randint(-20, 20), cluster_coordinates[1] + randint(-20, 20))

        star_cluster.append(
            Star(
                star_name,
                star_coordinates,
                [
                    Planet(
                        f"{star_name} {int_to_roman(planet_index)}",
                        0,
                        choice(planet_environments),
                    )
                    for planet_index in range(1, randint(1, 6))
                ],
            )
        )
    for star in star_cluster:
        unconnected_stars = get_unconnected_stars(star, star_cluster)
        if unconnected_stars:
            other_star = get_closest_star(star, unconnected_stars)
            if other_star:
                star.star_lane_connections.append(other_star)
                other_star.star_lane_connections.append(star)

            for _ in range(randint(0, 1)):
                other_star = choice(unconnected_stars)
                star.star_lane_connections.append(other_star)
                other_star.star_lane_connections.append(star)

    star_clusters.append(star_cluster)
    starmap.extend(star_cluster)

for cluster_index, star_cluster in enumerate(star_clusters):
    connected_clusters = [cluster for cluster in star_clusters if cluster != star_cluster and any(star.star_lane_connections for star in cluster)]
    for _ in range(randint(1, 2)):
        try:
            star = choice(star_cluster)
            other_stars = [star for star in starmap if star not in star_cluster and star not in connected_clusters]
            other_star = get_closest_star(star, other_stars)
            if star and other_star and other_star not in star.star_lane_connections:
                star.star_lane_connections.append(other_star)
                other_star.star_lane_connections.append(star)

        except IndexError:
            break

disconnected_clusters = star_clusters.copy()
while disconnected_clusters:
    cluster = disconnected_clusters.pop(0)
    connected_clusters = [other_cluster for other_cluster in star_clusters if other_cluster != cluster and any(star.star_lane_connections for star in other_cluster)]
    if connected_clusters:
        continue

    try:
        star = choice(cluster)
        other_stars = [star for cluster in disconnected_clusters for star in cluster]
        other_star = get_closest_star(star, other_stars)
        if star and other_star and other_star not in star.star_lane_connections:
            star.star_lane_connections.append(other_star)
            other_star.star_lane_connections.append(star)
    except IndexError:
        break


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.route("/starmap")
    def get_starmap():
        return jsonify([star.to_dict() for star in starmap])

    @app.route("/tech_tree")
    def get_tech_tree():
        return jsonify([tech.to_dict() for tech in tech_tree])

    return app

print(f"[bold green]Game generated with {len(starmap)} stars and {len(tech_tree)} technologies.[/bold green]")

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)