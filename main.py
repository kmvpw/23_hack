import random
from colorama import Fore, Style


CHARACTERS_NAMES = [
    'Thalior Windshade',
    'Brog Stonejaw',
    'Kaelen Duskwhisper',
    'Vark Grimtooth',
    'Elandor Silverleaf',
    'Marnak Firevein',
    'Torven Blackcloak',
    'Orik Ironfist',
    'Zeyrith Shadowborne',
    'Fenric Stormborn',
    'Lyara Moonfern',
    'Syris Ravenglade',
    'Maelis Thorneheart',
    'Velka the Pale',
    'Nymeria Starfire',
    'Rivena Nightshade',
    'Thessara Flamewind',
    'Kora Wyrmblood',
    'Alira Frostveil',
    'Ysolde Duskrunner',
]

THINGS_NAME = [
    'Blade of Eternal Flame',
    'Dagger of Silent Steps',
    'Thunderfang Axe',
    'Icebound Longsword',
    'Venomfang Kris',
    'Staff of Whispering Winds',
    'Hammer of the Fallen Star',
    'Bloodspike Mace',
    'Spear of Endless Hunt',
    'Bow of the Moonlit Vale',
    'Shield of Forgotten Kings',
    'Ironfang Helm',
    'Cloak of the Raven Lord',
    'Wyrmskin Armor',
    'Boots of the Ember Path',
    'Gauntlets of Crushing Earth',
    'Robes of Arcane Silence',
    'Helm of the Howling Wolf',
    'Plate of the Iron Oath',
    'Chainmail of Sacred Light',
    'Ring of the Shattered Realm',
    'Amulet of the Serpent’s Eye',
    'Talisman of Lost Souls',
    'Necklace of Lunar Blood',
    'Orb of Stolen Fire',
    'Crystal of Timeless Memory',
    'Bone Charm of the Ancients',
    'Sigil of Eternal Vigil',
    'Stone of Whispering Shadows',
    'Rune-etched Bracer',
    'Phoenix Feather Cloak',
    'Eye of the Void',
    'Lantern of Forgotten Paths',
    'Mirror of Illusory Doubles',
    'Horn of the Deepwood King',
    'Ashes of the First Flame',
    'Mask of the Hollow Watcher',
    'Scroll of Binding Echoes',
    'Grimoire of Endless Night',
    'Totem of Wild Fury',
]


"""Клас генерируемых вещей."""


class Thing:
    def __init__(self, name, protect, damage, hp):
        self.name = name
        self.protect = protect
        self.damage = damage
        self.hp = hp

    def __str__(self):
        return (
            f'{self.name}:'
            f' защита {self.protect}, '
            f' урон {self.damage}, HP {self.hp}'
        )

    @staticmethod
    def generate_random_things(count=40):
        things = []
        for i in range(count):
            name = random.choice(THINGS_NAME)
            protect = round(random.uniform(0, 0.1), 1)
            damage = random.randint(1, 15)
            hp = random.randint(0, 25)

            thing = Thing(name, protect, damage, hp)
            things.append(thing)
        return things


"""Базовый класс персонажа."""


class Person:
    def __init__(self, name, base_hp, base_damage, base_protect):
        self.name = name
        self.base_hp = base_hp
        self.base_damage = base_damage
        self.base_protect = base_protect
        self.things = []

        # Расчетные поля (после count_stats)
        self.current_hp = base_hp
        self.total_damage = base_damage
        self.total_protect = base_protect

    def set_things(self, things):
        count = random.randint(1, 4)
        self.things = random.sample(things, k=count)
        self.count_stats()

    def count_stats(self):
        bonus_hp = 0
        for thing in self.things:
            bonus_hp += thing.hp
        bonus_protect = 0
        for thing in self.things:
            bonus_protect += thing.protect
        bonus_damage = 0
        for thing in self.things:
            bonus_damage += thing.damage

        self.current_hp = self.base_hp + bonus_hp
        self.total_damage = self.base_damage + bonus_damage
        self.total_protect = self.base_protect + bonus_protect

    def is_alive(self):
        return self.current_hp > 0

    def recieve_damage(self, attack_damage):
        enemy_damage = round(
            attack_damage - (attack_damage * self.total_protect),
            2
        )
        self.current_hp -= enemy_damage
        return enemy_damage


"""Наследуемые калассы."""


class Paladin(Person):
    def __init__(self, name, base_hp, base_damage, base_protect):
        super().__init__(name, base_hp * 2, base_damage, base_protect * 2)


class Warrior(Person):
    def __init__(self, name, base_hp, base_damage, base_protect):
        super().__init__(name, base_hp, base_damage * 2, base_protect)


def main():
    """Основной цикл игры."""

    # Создание списка вещей
    things_list = Thing.generate_random_things()

    # Генерация участников битвы
    participants = []
    used_names = set()
    for _ in range(10):
        while True:
            name = random.choice(CHARACTERS_NAMES)
            if name not in used_names:
                used_names.add(name)
                break
        hp = 50
        damage = random.randint(10, 20)
        protect = round(random.uniform(0.01, 0.1), 1)
        character_class = random.choice([Paladin, Warrior])
        participant = character_class(name, hp, damage, protect)
        participants.append(participant)

    # Добавляем вещи персонажам
    for participant in participants:
        participant.set_things(things_list)

    # Логика боя
    count_round = 1
    alive = participants.copy()

    while len(alive) > 1:
        attacker, defender = random.sample(alive, 2)
        damage = attacker.total_damage
        get_damage = defender.recieve_damage(damage)

        print(
            f'{count_round}'
            f' Раунд: {attacker.name}'
            f' наносит удар по {defender.name}'
            f' на {get_damage:.1f} урона'
            )

        if not defender.is_alive():
            print(Fore.RED + f'{defender.name} погиб!' + Style.RESET_ALL)
            alive.remove(defender)

        count_round += 1

    winner = alive[0]
    print(Fore.GREEN + f'Победитель!! {winner.name}' + Style.RESET_ALL)


if __name__ == '__main__':
    main()
