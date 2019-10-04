from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstarctEffect(ABC, Hero):

    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects

    @abstractmethod
    def get_stats(self):
        return self.stats


class AbstarctPositive(AbstarctEffect):

    def __init__(self, base):
        self.base = base

    def get_stats(self):
        return self.base.get_stats()

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Berserk(AbstarctPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        stats["HP"] += 50

        return stats.copy()

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Berserk"]


class Blessing(AbstarctPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Perception"] += 2
        stats["Endurance"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2

        return stats.copy()

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Blessing"]


class AbstractNegative(AbstarctEffect):

    def __init__(self, base):
        self.base = base

    def get_stats(self):
        return self.base.get_stats()

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Weakness(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4

        return stats.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Weakness"]


class EvilEye(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10

        return stats.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["EvilEye"]


class Curse(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Perception"] -= 2
        stats["Endurance"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2

        return stats.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Curse"]


hero = Hero()
print(hero.get_stats())
print(hero.get_negative_effects())
print(hero.get_positive_effects())

brs1 = Berserk(hero)
print(brs1.get_stats())
print(brs1.get_positive_effects())
print(brs1.get_negative_effects())

brs2 = Berserk(brs1)

cur1 = Curse(brs2)
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())

# block Berserk effects
cur1.base = brs1
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())
