from dice import Dice, WoodDice, RiggedDice
from rich import print
import pygame


class Health:
    pass


class Action:
    pass


class Messages:
    pass


class Caracter:
    type = "Caracter"
    icon = ""
    file_path = "./dice_warrior/sound/default.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        self.name = name
        self.max_health = max_health
        self.health = self.max_health
        self.attack_value = attack
        self.defense_value = defense
        self.dice: Dice = dice

    def __str__(self):
        return f"I'm {self.name} a {type(self).type} with {self.health}/{self.max_health} points of health, {self.attack_value} points of attack and {self.defense_value} points in defense."

    def get_type(self):
        return type(self).type

    def regenerate(self):
        self.health = self.max_health
        return self.health

    def is_alive(self):
        return self.health > 0

    def show_healthbar(self):
        return print(f"{self.name} [{'💚'*self.health}{'🤍'*(self.max_health-self.health)}] {self.health}/{self.max_health}hp \n")

    def decrease_health(self, amount):
        self.health -= amount
        # Fix temporaire - classe health nécessaire à l'avenir
        if (self.health < 0):
            self.health = 0
        self.show_healthbar()

    def compute_damages(self, roll, target=None):
        damages = self.attack_value + roll
        return damages

    def attack(self, target):
        if (self.is_alive() and target.is_alive()):
            roll = self.dice.roll()
            damages = self.compute_damages(roll, target)
            print(
                f"{type(self).icon} {type(self).type} {self.name} attack {target.name} with {damages} damages (attack: {self.attack_value} + roll {roll})")
            target.defend(damages, self)

    def compute_wounds(self, damages, roll, attacker=None):
        wounds = damages - self.defense_value - roll
        if (wounds < 0):
            wounds = 0
        return wounds

    def defend(self, damages, attacker=None):
        roll = self.dice.roll()
        wounds = self.compute_wounds(damages, roll, attacker)
        print(
            f"{type(self).icon} {type(self).type} {self.name} defend against {attacker.name} with {damages} damages and takes {wounds} wounds (damages: {damages} - defense {self.defense_value} - roll: {roll})")
        self.decrease_health(wounds)

    def play_sound(self, file_path):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()


class Warrior(Caracter):
    type = "[bold red]Warrior[/bold red]"
    icon = "⚔️ "
    file_path = "./dice_warrior/sound/warrior.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        super().__init__(name, max_health, attack, defense, dice)
        self.bonus_damage = 0

    def compute_damages(self, roll, target=None):
        return super().compute_damages(roll) + self.bonus_damage

    def reset_power(self):
        self.bonus_damage = 0

    def attack(self, target):
        if (self.is_alive()):
            self.power()
            return super().attack(target)

    def power(self):
        power_dice = Dice(20)
        roll = power_dice.roll()
        if roll > 10 and roll < 20:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} wields a mighty axe, dealing extra damage")
            self.bonus_damage = 1
        elif roll == 1:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} delivers a devastating critical strike, dealing more damage")
            self.bonus_damage = 3
        elif roll == 20:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} misses the mark and deals regular damage")
            self.bonus_damage = 0


class Wizard(Caracter):
    type = "[bold blue]Wizard[/bold blue]"
    icon = "🪄 "
    file_path = "./dice_warrior/sound/wizard.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        super().__init__(name, max_health, attack, defense, dice)
        self.bonus_defense = 0

    def compute_wounds(self, damages, roll, attacker=None):
        return super().compute_wounds(damages, roll, attacker) - self.bonus_defense

    def reset_power(self):
        self.bonus_defense = 0

    def defend(self, damages, attacker=None):
        self.power()
        super().defend(damages, attacker)
        self.reset_power()

    def power(self):
        power_dice = Dice(20)
        roll = power_dice.roll()
        if roll > 10 and roll < 20:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} harnesses the power of arcane magic, enhancing their defense by 2")
            self.bonus_defense = 2
        elif roll == 1:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} conjures a devastating spell, amplifying their defense by 3")
            self.bonus_defense = 3
        elif roll == 20:
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} fails to cast a spell, resulting in no additional defense")
            self.bonus_defense = 0


class Thief(Caracter):
    type = "[bold magenta]Thief[/bold magenta]"
    icon = "🥷 "
    file_path = "./dice_warrior/sound/thief.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        super().__init__(name, max_health, attack, defense, dice)
        self.reset_power()

    def reset_power(self):
        self.bonus_damage = 0

    def attack(self, target):
        if (self.is_alive()):
            self.power(target)
            return super().attack(target)

    def compute_damages(self, roll, target=None):
        return super().compute_damages(roll, target) + self.bonus_damage

    def power(self, target):
        power_dice = Dice(20)
        roll = power_dice.roll()
        if roll > 10 and roll < 20:
            self.bonus_damage = round(target.defense_value / 4)
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} skillfully exploits the enemy's defense, breaking through for extra damage")
        elif roll == 1:
            self.bonus_damage = target.defense_value
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} perfectly exploits the enemy's weakness, dealing extra damage")
        elif roll == 20:
            self.bonus_damage = 0
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} fails to break the defense and deals regular damage")


class Archer(Caracter):
    type = "[bold cyan]Archer[/bold cyan]"
    icon = "🏹 "
    file_path = "./dice_warrior/sound/archer.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        super().__init__(name, max_health, attack, defense, dice)
        self.reset_power()

    def reset_power(self):
        self.bonus_attack = 0

    def attack(self, target):
        if (self.is_alive()):
            self.power()
            return super().attack(target)

    def compute_damages(self, roll, target=None):
        return super().compute_damages(roll) + self.bonus_attack

    def power(self):
        power_dice = Dice(20)
        roll = power_dice.roll()
        if roll > 10 and roll < 20:
            self.bonus_attack = 1
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} gains +1 attack for the next attack")
        elif roll == 1:
            self.bonus_attack = 2
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} lands a perfect shot and gains +2 attack for the next attack")
        elif roll == 20:
            self.bonus_attack = -2
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} has bad aim and loses 2 attack for the next attack")


class Paladin(Caracter):
    type = "[bold green]Paladin[/bold green]"
    icon = "⚜️ "
    file_path = "./dice_warrior/sound/paladin.mp3"

    def attack(self, target):
        if (self.is_alive()):
            self.power()
            return super().attack(target)

    def check_health(self):
        if (self.health >= self.max_health):
            self.health = self.max_health

    def power(self):
        heal_dice = Dice(20)
        roll = heal_dice.roll()
        if roll > 16 and roll < 20:
            self.health += 1
            self.check_health()
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} is blessed and regains 1 HP")
            self.show_healthbar()
        elif roll == 1:
            self.health += 2
            self.check_health()
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} is divinely favored and regains 2 HP")
            self.show_healthbar()
        elif roll == 20:
            self.health -= 2
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} is unfortunate and accidentally injures himself, losing 2 HP")
            self.show_healthbar()


class Necromancer (Caracter):
    type = "[bold yellow]Necromancer[/bold yellow]"
    icon = "☠️ "
    file_path = "./dice_warrior/sound/necromancer.mp3"

    def __init__(self, name, max_health, attack, defense, dice):
        super().__init__(name, max_health, attack, defense, dice)
        self.reset_power()

    def defend(self, damages, attacker=None):
        self.power()
        super().defend(damages, attacker)
        self.reset_power()

    def reset_power(self):
        self.defense_ratio = 1

    def compute_wounds(self, damages, roll, attacker=None):
        return round(super().compute_wounds(damages, roll, attacker) * self.defense_ratio)

    def power(self):
        summon_dice = Dice(20)
        roll = summon_dice.roll()
        if roll > 10 and roll < 20:
            self.defense_ratio = 0.2
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} invokes dark magic and reduces damage taken by 80%")
        elif roll == 1:
            self.defense_ratio = 0
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} is surrounded by an impenetrable aura and avoids all damage")
        elif roll == 20:
            self.defense_ratio = 2
            print(
                f"Bonus: {type(self).icon} {type(self).type} {self.name} is unlucky and attracts the wrath of the underworld, taking double damage")


if (__name__ == "__main__"):
    pass
