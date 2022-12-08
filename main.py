from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color
from random import randint, uniform
from math import sqrt
import numpy as np

Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '600')

DELTA_TIME = 1.0 / 60.0
RADIUS = (20, 30, 40, 50)
COLOR = ((0.98, 0.46, 0.73, 0.8), (0.68, 0.44, 0.80, 0.8), (0.39, 0.37, 0.72, 0.8),
         (0.47, 0.83, 0.99, 0.8), (0.55, 0.92, 0.84, 0.8), (0.38, 0.86, 0.38, 0.8),
         (0.93, 1.00, 0.34, 0.8), (1.00, 0.80, 0.36, 0.93), (0.93, 0.38, 0.27, 0.93))

class BouncingBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    radius = NumericProperty(0)
    diameter = NumericProperty(0)

    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)
    color = ReferenceListProperty(r, g, b, a)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def intersects_ball(self, other):
        xdelta = abs(self.center_x - other.center_x)
        ydelta = abs(self.center_y - other.center_y)
        distance = sqrt(xdelta * xdelta + ydelta * ydelta)

        if distance < (self.radius + other.radius):
            # print(xdelta)
            # print(ydelta)
            print(f'radius: {self.radius}, {other.radius}')
            print(f'size: {self.size}, {other.size}')
            # print(distance)

        return distance <= (self.radius + other.radius)

    def change_velocity(self, other):
        # m1, m2 = 2700 * np.pi * 4.0 * self.radius**3 / 3.0, 2700 * np.pi * 4.0 * other.radius**3 / 3.0
        m1, m2 = self.radius**3, other.radius**3
        m = m1 + m2

        vx1, vx2 = self.velocity_x, other.velocity_x
        vy1, vy2 = self.velocity_y, other.velocity_y

        rx1, rx2 = self.center_x, other.center_x
        ry1, ry2 = self.center_y, other.center_y

        dx = np.linalg.norm(rx1 - rx2)**2
        dy = np.linalg.norm(ry1 - ry2) ** 2

        ux1 = (2 * m2 * vx2 + (m1 - m2) * vx1) / m
        ux2 = (2 * m1 * vx1 + (m1 - m2) * vx2) / m
        uy1 = (2 * m2 * vy2 + (m1 - m2) * vy1) / m
        uy2 = (2 * m1 * vy1 + (m1 - m2) * vy2) / m

        # ux1 = vx1 - (2 * m2 / m) * (np.dot(vx1 - vx2, rx1 - rx2) / dx) * (rx1 - rx2)
        # ux2 = vx2 - (2 * m1 / m) * (np.dot(vx2 - vx1, rx2 - rx1) / dx) * (rx2 - rx1)
        # uy1 = vy1 - (2 * m2 / m) * (np.dot(vy1 - vy2, ry1 - ry2) / dy) * (ry1 - ry2)
        # uy2 = vy2 - (2 * m1 / m) * (np.dot(vy2 - vy1, ry2 - ry1) / dy) * (ry2 - ry1)

        self.velocity_x = ux1
        other.velocity_x = ux2
        self.velocity_y = uy1
        other.velocity_y = uy2


class BouncingGame(Widget):
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    ball4 = ObjectProperty(None)
    ball5 = ObjectProperty(None)
    balls = ReferenceListProperty(ball1, ball2, ball3, ball4, ball5)
    # balls = ReferenceListProperty(ball1, ball2)

    def serve_balls(self):
        for i, ball in enumerate(self.balls):
            ball.velocity = Vector(uniform(0.5, 4), uniform(0.5, 4)).rotate(randint(0, 360))
            # ball.valocity = Vector(0, 0)

            start_coord = 50 + i * 100
            ball.center = Vector(start_coord, start_coord)

            ball.radius = RADIUS[randint(0, 3)]
            # ball.radius = 50
            ball.diameter = ball.radius * 2
            ball.size = (ball.diameter, ball.diameter)

            ball.color = COLOR[randint(0, 8)]

    def update(self, dt):
        for i, ball in enumerate(self.balls):
            # bounce off top and bottom
            if (ball.y < 0) or (ball.y + ball.diameter > self.height):
                ball.velocity_y *= -1

            # bounce off left and right
            if (ball.x < 0) or (ball.x + ball.diameter > self.width):
                ball.velocity_x *= -1

            for j in range(i + 1, len(self.balls)):
                if ball.intersects_ball(self.balls[j]):
                    ball.velocity_x *= -1
                    ball.velocity_y *= -1
                    self.balls[j].velocity_x *= -1
                    self.balls[j].velocity_y *= -1
                    # ball.change_velocity(self.balls[j])

            ball.move()

class BouncingApp(App):
    def build(self):
        game = BouncingGame()
        game.serve_balls()
        Clock.schedule_interval(game.update, DELTA_TIME)
        return game


if __name__ == '__main__':
    BouncingApp().run()
