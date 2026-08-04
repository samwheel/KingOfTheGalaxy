#! /Users/Samwise/Projects/Python/KingOfTheGalaxy/.venv/bin/python

from flask import Flask, jsonify
from flask_cors import CORS
from rich import print

from src.standard_game_factory import StandardGameFactory
from src.empire import Empire

game_factory = StandardGameFactory()
current_game = game_factory.create_game()

player_empire = Empire("Terran Imperium", "blue")
homeplanet = game_factory.create_homeplanet(current_game)
homeplanet.statistics["population"] = 1
player_empire.planets.append(homeplanet)

empires = [player_empire]

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.route("/starmap")
    def get_starmap():
        return jsonify([star.to_dict() for star in current_game.starmap])
    
    @app.route("/starmap/<star_name>")
    def get_star(star_name: str):
        star = next((s for s in current_game.starmap if s.name == star_name), None)
        if star:
            star_dict = star.to_dict()
            star_dict["planets"] = [planet.to_dict() for planet in star.planets]
            return jsonify(star_dict)
        return jsonify({"error": "Star not found"}), 404

    @app.route("/tech_tree")
    def get_tech_tree():
        return jsonify([tech.to_dict() for tech in current_game.tech_tree])

    @app.route("/empires")
    def get_empires():
        return jsonify([empire.to_dict() for empire in empires])

    return app

print(f"[bold green]Game generated with {len(current_game.starmap)} stars and {len(current_game.tech_tree)} technologies.[/bold green]")

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)