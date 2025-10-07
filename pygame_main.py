from random import choice
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
from pygame.time import Clock

from pygame_helper import button

from view.star import Star
from view.planet import PlanetView
from view.production import ProductionView

from src.planet import Planet, Focus
from src.race import *
from src.empire import Empire
from src.buildings import IndustrialCenter

def random_star_name() -> str:
    name_list:list[str] = []
    with open("src/names.txt", "r") as names:
        name_list = [name.strip() for name in names.readlines()]
        return choice(name_list).capitalize()

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("King of the Galaxy")
planet_group: list[PlanetView] = []
with open("src/races.dat", "r") as f:
    races: list[Race] = [eval(line) for line in f.readlines()]
player_empire = Empire("Blorg", "Glorp")
player_empire.add_planet(Planet(f"{random_star_name()} I", races[0], 1, 50, Focus.INDUSTRY))

production_view = ProductionView(player_empire)

planet_group.append(PlanetView(30, pygame.Color(20, 255, 20), player_empire.planets[0]))

star: Star = Star(800, 450, 10, pygame.Color(255, 0, 0), planet_group)
stars: list[Star] = []
stars.append(star)
planet_view_group: list[PlanetView] = []
widgets = pygame.sprite.Group()
current_view: pygame.sprite.Sprite | None = None
def toggle_production_view() -> None:
    global current_view
    if current_view == production_view:
        current_view = None
    else:
        current_view = production_view

production_button = button.ImageButton(pygame.Color("black"), pygame.image.load("images/production_icon.png"), 150, 50, action=toggle_production_view)
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

clock = Clock()

while True:
    for event in pygame.event.get():
        widgets.update(event)
        for planet in planet_group:
            planet.update(event)
        
        if current_view:
            current_view.update(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                clicked_star = [s for s in stars if s.rect.collidepoint(event.pos)][0]
                planet_view_group = []
                for planet in clicked_star.planets:
                    planet_view_group.append(planet)
            except IndexError:
                pass
    

    for planet in planet_group:
        planet.observer_update()

    screen.fill("black")

    for index, planet in enumerate(planet_view_group):
        planet.move(1400, index)

    for star in stars:
        star.draw(screen)

    if planet_view_group:
        pygame.draw.rect(screen, (50, 50, 50), pygame.rect.Rect(1400, 50, 350, 900))
        for planet_view in planet_view_group:
            planet_view.draw(screen)
    
    if current_view:
        current_view.draw(screen)
        try:
            current_view.set_current_planet(planet_view_group[0].planet)
        except IndexError:
            pass

        current_view.observer_update()
    
    for widget in widgets:
        widget.move(0, 0)
        widget.draw(screen)

    pygame.display.flip()
    clock.tick(60)