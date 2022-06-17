# Create a simulation of the solar system
# based on the tutorial https://www.youtube.com/watch?v=WTLPmUHTPqo
# import modules and setup the project

# Hint: F = G * (Mn/r^2)
#       F is the gravitational force of attraction between two objects of mass M and n. G is the gravitational constant
#       r is the distance between the objects

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 12)
SPEED_SCALE = 1


class Planet:
    # Astronomical unit
    AU = 149.6e6 * 1000
    # Gravitational constant
    G = 6.67428e-11
    SCALE = 250 / AU  # 1Au circa 100 Pixels
    TIMESTEP = (3600*24) / SPEED_SCALE  # 1 day in seconds

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        # in pygame the coordinate 0,0 is at the top left of the screen
        # in order to draw at the center we need to had the half of the width and height to x,y coordinates
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
                # print(updated_points[0])

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", True, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + self.radius))
            planet_name = FONT.render(self.name, True, WHITE)
            win.blit(planet_name, (x - distance_text.get_width() / 4, y - distance_text.get_height()*2))

    def attraction(self, other):
        """Calculate the force of attraction between two objects. Split the straight force of attraction between the
        object in the F_x (force along the x-axis) F_y (force along the y-axis) components"""

        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        # in order to split the gravitational force into an x and y component we need to calculate the angle theta
        # of a triangle were the hypotenus is the distance between the two objects
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            # calculate the force of attraction to all other planets except itself
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Calculate the acceleration (a) as we know that F = m * a (force is equal mass times acceleration)
        # hence a = F / m. By multiplying a times the timestep we keep a constant over the timestep.
        # The a is changing constantly as the distance to the sun and the other planets changes.
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    pause = False
    clock = pygame.time.Clock()
    earth_days = 0

    sun = Planet('Sun', 0, 0, 30, YELLOW, 1.98892 * 10**30)
    # sun.y_vel = 29.783 * 100
    sun.sun = True

    earth = Planet('Earth', -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet('Mars', -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet('Mercury', 0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet('Venus', 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(20)
        # by each reiteration reset the screen in order to get ride of the old positions of the planets
        WIN.fill((0, 0, 0))

        # Add a pause functionality
        # pause not working
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = True

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
        earth_days += 1
        pygame.display.set_caption(f"Planet Simulation: {round(earth_days / SPEED_SCALE)} Earth days")
        # earth_days_text = FONT.render(f"{round(earth_days/SPEED_SCALE)} Earth days", 1, RED)
        # text_rect = earth_days_text.get_rect()
        # text_rect.topleft = (10, 10)
        # WIN.blit(earth_days_text, (200, 200))
        # print(round(earth_days/SPEED_SCALE))
        # print(pause)
        # print(earth_days_text)

    pygame.quit()


main()
