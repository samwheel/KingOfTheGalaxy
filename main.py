from random import choice, randint
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.time import Clock

from pygame_helper import button

from view.star import StarView
from view.planet import PlanetView
from view.production import ProductionView
from view.ship_command import ShipCommandView
from view.view_control import ViewController

from src.planet import Planet, planet_types
from src.race import *
from src.empire import Empire
from src.create_races import create_races
from src.resource_helper import resourcePath
from src.star import Star

def random_star_name() -> str:
    name_list:list[str] = []
    with open(resourcePath("src/names.txt"), "r") as names:
        name_list = [name.strip() for name in names.readlines()]
        return choice(name_list).capitalize()

pygame.init()
pygame.display.set_icon(pygame.image.load("images/KingOfTheGalaxy.png"))

screen: pygame.Surface = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("King of the Galaxy")

races: list[Race] = create_races()
player_empire = Empire("Blorg", "Glorp", "blue")
player_empire.add_planet(Planet(f"", races[0].prefered_planet, races[0], 3))

production_view = ProductionView(player_empire)

stars: list[Star] = []
current_position: tuple[int, int] = (0, 0)
for _ in range(3):
    current_position = (0, current_position[1] + randint(150, 350))
    for _ in range(5):
        current_position = (current_position[0] + randint(150, 350), current_position[1])
        stars.append(Star(random_star_name(), (current_position[0] + randint(-50, 50), current_position[1] + randint(-50, 150)), [Planet("", choice(planet_types)) for _ in range(randint(0, 3))]))

homeplanet_index: int = randint(0, len(stars) - 1)
stars[homeplanet_index] = Star(random_star_name(), stars[homeplanet_index].position, [player_empire.planets[0]])

view_controller = ViewController()
view_controller.planet_view_group = [player_empire.planets[0]]
view_controller.current_view = None

def toggle_production_view() -> None:
    global view_controller
    if view_controller.current_view == production_view:
        view_controller.current_view = None
    else:
        view_controller.current_view = production_view

widgets = pygame.sprite.Group()

production_button = button.ImageButton(pygame.Color("black"), pygame.image.load(resourcePath("images/production_icon.png")), 150, 50, action=toggle_production_view)
turn_button = button.Button(
    pygame.Color("black"), 
    f'Turn (1)', 
    10, 
    50, 
    action=player_empire.year_handler.next_year, 
    update_function=lambda: setattr(turn_button, 'text', f'Turn ({player_empire.year_handler.year})'))
player_empire.year_handler.add_observer(turn_button)
widgets.add(production_button)
widgets.add(turn_button)
show_planet_view = True

clock = Clock()

while True:
    for event in pygame.event.get():
        widgets.update(event)
        for index, planet in enumerate(view_controller.planet_view_group):
            planet_view = PlanetView(planet)
            planet_view.move(1400, index)
            planet_view.update(event)
        
        if view_controller.current_view and show_planet_view:
            view_controller.current_view.update(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                clicked_star: Star = [s for s in stars if StarView(s).rect.collidepoint(event.pos)][0]
                view_controller.planet_view_group = []
                for planet in clicked_star.planets:
                    view_controller.planet_view_group.append(planet)
                view_controller.show_planet_view = True
                if isinstance(view_controller.current_view, ShipCommandView):
                    view_controller.current_view.ship.destination = clicked_star
            except IndexError as e:
                if event.pos[0] > 200 and event.pos[0] < 1400:
                    if view_controller.current_view == None:
                        view_controller.show_planet_view = False
                    elif isinstance(view_controller.current_view, ShipCommandView):
                        view_controller.current_view = None

    screen.fill("black")

    view_controller.update_views(stars, player_empire, screen, widgets)

    pygame.display.flip()
    clock.tick(60)