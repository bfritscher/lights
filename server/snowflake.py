# -*- coding: utf-8 -*-
import itertools

import time

from neopixel import Color
from lights import setPixelColor, show


class Leds(object):
    def __init__(self, leds=[]):
        self.leds = leds

    def color(self, color):
        map(lambda i: setPixelColor(i, color),self.leds)
        show()
        time.sleep(1000 / 1000.0)


class Star(Leds):
    def __init__(self, start_led):
        super(Star, self).__init__()
        self.inner = Leds(range(start_led + 156, start_led + 180))
        outer = [range(start_led + 22 + (i*26), start_led + 26 + (i*26)) for i in range(6)]
        self.outer = Leds(list(itertools.chain.from_iterable(outer)))
        self.leds = self.inner.leds + self.outer.leds


class Trunk(Leds):
    def __init__(self, start_led):
        super(Trunk, self).__init__()
        self.bottom = Leds(range(start_led, start_led + 2) + range(start_led + 20, start_led + 22))
        self.top = Leds(range(start_led + 8, start_led + 14))
        self.leds = self.top.leds + self.bottom.leds


class Tree(Leds):
    def __init__(self, start_led):
        super(Tree, self).__init__()
        self.trunk = Trunk(start_led)
        self.leaf = Leds(range(start_led + 2, start_led + 8) + range(start_led + 14, start_led + 20))
        self.top = Leds(self.trunk.top.leds + self.leaf.leds)
        self.leds = self.trunk.leds + self.leaf.leds


class Trees(Leds):
    def __init__(self, start_led):
        super(Trees, self).__init__()
        self.trees = [Tree(start_led + i * 26) for i in range(6)]
        self.leds = list(itertools.chain.from_iterable([t.leds for t in self.trees]))
        self.leaf = Leds(list(itertools.chain.from_iterable([t.leaf.leds for t in self.trees])))
        self.top = Leds(list(itertools.chain.from_iterable([t.top.leds for t in self.trees])))
        self.trunk = Trunk(0)
        self.trunk.bottom = Leds(list(itertools.chain.from_iterable([t.trunk.bottom.leds for t in self.trees])))
        self.trunk.top = Leds(list(itertools.chain.from_iterable([t.trunk.top.leds for t in self.trees])))
        self.trunk.leds = list(itertools.chain.from_iterable([t.trunk.leds for t in self.trees]))

    def __getitem__(self, item):
        return self.trees[item]


class Snowflake(Leds):
    def __init__(self, start_led):
        super(Snowflake, self).__init__()
        self.star = Star(start_led)
        self.trees = Trees(start_led)
        self.leds = self.star.leds + self.trees.leds

    def test(self):
        self.color(Color(255, 0, 0))
        self.star.color(Color(0, 255, 0))
        self.star.inner.color(Color(0, 0, 255))
        self.star.outer.color(Color(0, 0, 255))

        self.trees[0].color(Color(0, 0, 255))
        self.trees[0].trunk.color(Color(0, 255, 0))
        self.trees[0].trunk.bottom.color(Color(255, 0, 0))
        self.trees[0].trunk.top.color(Color(255, 0, 0))
        self.trees[0].leaf.color(Color(255, 0, 0))
        self.trees[0].top.color(Color(0, 255, 0))

        self.trees.color(Color(0, 0, 255))
        self.trees.trunk.color(Color(0, 255, 0))
        self.trees.trunk.bottom.color(Color(255, 0, 0))
        self.trees.trunk.top.color(Color(255, 0, 0))
        self.trees.leaf.color(Color(255, 0, 0))
        self.trees.top.color(Color(0, 255, 0))
