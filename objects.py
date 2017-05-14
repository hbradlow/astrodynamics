import numpy as np
import pygame.draw

class Planet:
    
    def __init__(self, radius, position, center):
        self.radius = radius
        self.position = position
        self.mu = 2.0e6
        self.scale = 1.0
        self.center = center

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), 
            (self.center + (self.position - self.center) * self.scale).astype(int), 
            int(self.radius * self.scale))

class Satellite:

    def __init__(self, position, velocity, planet, center):
        self.position = position
        self.velocity = velocity
        self.planet = planet

        self.radius = 5

        self.path_p = None
        self.path_e = None

        self.scale = 1.0
        self.center = center

    def r(self):
        return self.position - self.planet.position

    def specific_energy(self):
        return np.dot(self.velocity, self.velocity)/2.0 - self.planet.mu/np.linalg.norm(self.r())

    def a(self):
        return - self.planet.mu / (2.0 * self.specific_energy())

    def c(self):
        return np.linalg.norm(self.e()) * self.a()

    def b(self):
        return np.sqrt(self.a() ** 2 - self.c() ** 2)

    def h(self):
        return np.cross(self.r(), self.velocity)

    def e(self):
        t1 = np.dot(self.velocity, self.velocity) - self.planet.mu/np.linalg.norm(self.r())
        t2 = np.dot(self.r(), self.velocity)
        return (t1 * self.r() - t2 * self.velocity) / self.planet.mu

    def p(self):
        return np.dot(self.h(), self.h()) / self.planet.mu

    def draw(self, screen, color=(255, 255, 255)):
        pygame.draw.circle(screen, color,
            (self.center + (self.position - self.center) * self.scale).astype(int), 
            int(self.radius * self.scale))

    def update_path_params(self):
        self.path_p = self.p()
        self.path_e = self.e()

    def draw_path(self, screen, color=(255, 255, 255)):
        if self.path_p is None or self.path_e is None:
            return

        prev_p = None
        for v in np.arange(0,np.pi*2.3, np.pi/50):
            r = self.path_p / (1 + np.linalg.norm(self.path_e) * np.cos(v))

            M = np.array([[np.cos(v), -np.sin(v)], [np.sin(v),  np.cos(v)]])
            p = self.planet.position + r * np.dot(M, (self.path_e/np.linalg.norm(self.path_e)))

            p = self.center + (p - self.center) * self.scale

            if prev_p is not None:
                pygame.draw.line(screen, color, prev_p, p, 1)

            prev_p = p

    def update(self, dt):
        self.velocity -= self.planet.mu * dt * self.r() / np.linalg.norm(self.r())**3
        self.position += dt * self.velocity
        if self.path_e is None or self.path_e is None:
            self.update_path_params()

    def burn(self, dv):
        self.velocity += self.velocity * dv / np.linalg.norm(self.velocity)
        self.update_path_params()
