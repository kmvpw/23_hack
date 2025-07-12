import random
from typing import List

NAMES: List[str] = [
    'Азмодан', 'Баал', 'Диабло', 'Мефисто', 'Андриэль',
    'Ракинош', 'Колен-Хан', 'Синклер', 'Гарбод', 'Эшра',
    'Кэйн', 'Частик', 'Атия', 'Золтан', 'Эйрея',
    'Деккард', 'Лиандра', 'Малтаэль', 'Джаззхар', 'Кормек',
]

THING_NAMES: List[str] = [
    'Кольцо Всевластия', 'Мифриловая броня', 'Палантир',
    'Посох Гэндальфа', 'Дневник Тома Реддла', 'Бузинная палочка',
    'Воскрешающий камень', 'Мантия-невидимка', 'Медальон Слизерина',
    'Меч Гриффиндора', 'Чаша Пуффендуй', 'Диадема Когтевран',
    'Кольцо Мраксов', 'Экскалибур', 'Кубок Огня',
    'Маховик времени', 'Зеркало Еиналеж', 'Философский камень',
    'Сапоги-скороходы', 'Кольцо Драупнир', 'Мьёльнир',
    'Копьё Гунгнир', 'Молния Зевса', 'Трезубец Посейдона',
    'Кифара Аполлона', 'Пояс Афродиты', 'Доспехи Ахиллеса',
    'Золотое руно', 'Ящик Пандоры', 'Сандалии Гермеса',
    'Скатерть-самобранка', 'Ковчег Завета', 'Хрустальный череп',
    'Нейтрализатор памяти', 'Волшебная лампа', 'Световой меч',
    'Костюм Вейдера', 'Щит Капитана Америки',
    'Адамантиевый скелет', 'Церебро',
]


class Thing:
    def __init__(self, name: str, defense_percent: float, attack: int,
                 health: int):
        self.name = name
        self.defense_percent = min(0.1, max(0.0, defense_percent))
        self.attack = max(0, attack)
        self.health = max(0, health)

    def __str__(self):
        return self.name


class Person:
    def __init__(self, name: str, hp: int, base_attack: int,
                 base_defense_percent: float):
        self.name = name
        self.hp = hp
        self.base_attack = base_attack
        self.base_defense_percent = base_defense_percent

    def set_things(self, things):
        self.things = things
        self.attack = self.base_attack
        self.defense_percent = self.base_defense_percent
        for thing in self.things:
            self.attack += thing.attack
            self.defense_percent += thing.defense_percent
        self.defense_percent = min(1.0, self.defense_percent)

    def take_damage(self, damage: float):
        actual_damage = damage * (1 - self.defense_percent)
        self.hp -= int(actual_damage)
        self.hp = max(0, self.hp)

    def is_alive(self):
        return self.hp > 0


class Paladin(Person):
    def __init__(self, name: str, hp: int, base_attack: int,
                 base_defense_percent: float):
        super().__init__(name, hp * 2, base_attack,
                         min(1.0, base_defense_percent * 2))


class Warrior(Person):
    def __init__(self, name: str, hp: int, base_attack: int,
                 base_defense_percent: float):
        super().__init__(name, hp, base_attack * 2, base_defense_percent)


def main():
    # Шаг 1: Создание вещей
    things = []
    for _ in range(40):
        name = random.choice(THING_NAMES)
        defense = round(random.uniform(0, 0.1), 2)
        attack = random.randint(1, 15)
        health = random.randint(0, 20)
        things.append(Thing(name, defense, attack, health))

    # Шаг 2: Создание персонажей
    fighters = []
    for _ in range(10):
        name = NAMES.pop(random.randint(0, len(NAMES) - 1))
        hp = 100
        attack = random.randint(10, 20)
        defense = round(random.uniform(0.05, 0.2), 2)

        if random.random() < 0.5:
            fighter = Paladin(name, hp, attack, defense)
        else:
            fighter = Warrior(name, hp, attack, defense)

    # Шаг 3: Получение вещей
        num_things = random.randint(1, 4)
        fighter.set_things(random.sample(things, num_things))
        fighters.append(fighter)

    # Шаг 4: Бой
    while len(fighters) > 1:
        attacker, defender = random.sample(fighters, 2)
        damage = attacker.attack * (1 - defender.defense_percent)
        defender.take_damage(damage)
        print(
            f'{attacker.name} наносит удар по '
            f'{defender.name} на {damage:.1f} урона'
        )
        fighters = [f for f in fighters if f.is_alive()]

    if fighters:
        print(f'Победитель: {fighters[0].name}')
    else:
        print('Идет бой')


if __name__ == "__main__":
    main()
