import pygame
from pygame.time import Clock
from view.star import Star
from view.planet import PlanetView
from src.planet import Planet, Focus
from src.race import *

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((1280,720))
pygame.display.set_caption("King of the Galaxy")
planet_group = pygame.sprite.Group()
with open("src/races.dat", "r") as f:
    races = [eval(line) for line in f.readlines()]
    planet_group.add(PlanetView(30, pygame.Color(20, 255, 20), Planet("Earth", races[0], 1, Focus.INDUSTRY)))
    planet_group.add(PlanetView(30, pygame.Color(72, 25, 5), Planet("Mars", races[0], 1, Focus.INDUSTRY)))
star: Star = Star(640, 360, 10, pygame.Color(255, 0, 0), planet_group)
stars: pygame.sprite.Group = pygame.sprite.Group()
stars.add(star)
planet_view_group = pygame.sprite.Group()

clock = Clock()

while True:
    for event in pygame.event.get():
        planet_group.update(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_stars = [s for s in stars if s.rect.collidepoint(event.pos)]
            if clicked_stars:
                planet_view_group.empty()
                planet_view_group.add([star.planets for star in clicked_stars])
        

    screen.fill("black")

    for index, planet in enumerate(planet_view_group):
        planet.move(900, index)

    stars.draw(screen)

    if planet_view_group:
        pygame.draw.rect(screen, (50, 50, 50), pygame.rect.Rect(900, 50, 350, 600))
        for planet_view in planet_view_group:
            planet_view.draw(screen)

    pygame.display.flip()
    clock.tick(60)