from random import choice
import os

from src.race import Race
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
from pygame.time import Clock

from pygame_helper import button

from view.star import StarView
from view.planet import PlanetView
from view.production import ProductionView

from src.planet import Planet, Focus
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

screen: pygame.Surface = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("King of the Galaxy")

races: list[Race] = create_races()
player_empire = Empire("Blorg", "Glorp")
player_empire.add_planet(Planet(f"", races[0], 3, races[0].prefered_planet, Focus.INDUSTRY))

production_view = ProductionView(player_empire)

stars: list[StarView] = []
stars.append(StarView(Star(random_star_name(), (800, 450), [player_empire.planets[0]]), 10, pygame.Color(255, 0, 0)))

planet_view_group: list[PlanetView] = []
widgets = pygame.sprite.Group()
current_view: pygame.sprite.Sprite | None = None
def toggle_production_view() -> None:
    global current_view
    if current_view == production_view:
        current_view = None
    else:
        current_view = production_view

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
show_planet_view = False

clock = Clock()

while True:
    for event in pygame.event.get():
        widgets.update(event)
        for planet in planet_view_group:
            planet.update(event)
        
        if current_view and show_planet_view:
            current_view.update(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                clicked_star: StarView = [s for s in stars if s.rect.collidepoint(event.pos)][0]
                planet_view_group = []
                for planet in clicked_star.star.planets:
                    planet_view_group.append(PlanetView(planet))
                show_planet_view = True
            except IndexError:
                if event.pos[0] > 200 and event.pos[0] < 1400:
                    if current_view == None:
                        show_planet_view = False
    

    for planet in planet_view_group:
        planet.observer_update()

    screen.fill("black")

    for index, planet in enumerate(planet_view_group):
        planet.move(1400, index)

    for star in stars:
        star.draw(screen)

    if show_planet_view:
        pygame.draw.rect(screen, (50, 50, 50), pygame.rect.Rect(1400, 50, 350, 900))
        for planet_view in planet_view_group:
            planet_view.draw(screen)
    
    if current_view:
        current_view.draw(screen)
        current_view.set_current_planet(None)
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