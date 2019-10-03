#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * other, self.y * other)

    def length(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def int_pair(self):
        """текущие координато вектора"""
        return (int(self.x), int(self.y))


class Polyline():
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_points(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = Vec2d(
                self.points[p].x + self.speeds[p].x, self.points[p].y + self.speeds[p].y)
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p][0], self.speeds[p][1])
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        for p in points:
            pygame.draw.circle(gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def add_point(self, point, speed):
        super().add_points(point, speed)
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, basePoints):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(basePoints, alpha=(i * alpha)))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(
            ), points[p_n + 1].int_pair(), width)


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline()
    knot = Knot(steps)
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_r:
                    polyline = Polyline()
                    knot = Knot(steps)

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.add_points(Vec2d(event.pos[0], event.pos[1]), Vec2d(
                    random.random() * 2, random.random() * 2))
                knot.add_point(Vec2d(event.pos[0], event.pos[1]), Vec2d(
                    random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points(polyline.points)
        knot.draw_points(knot.get_knot(), 3, color)
        if not pause:
            polyline.set_points()
            knot.set_points()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
