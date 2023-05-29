from dice import Dice
from caracter import Caracter, Warrior, Wizard, Thief, Archer, Paladin, Necromancer
from rich import print
import pygame

default_path = "./dice_warrior/sound/choose.mp3"


def play_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()


if __name__ == "__main__":
    pygame.init()

    print("[bold yellow]Welcome to the Battle Game![/bold yellow]")
    print("In this game, all characters will battle against each other.")
    print("Each character has different attributes and abilities.")
    print("Let's see who comes out victorious!\n")

    characters = [
        Warrior("Lancelot", 18, 6, 3, Dice(6)),
        Wizard("Eleanor", 16, 6, 3, Dice(6)),
        Thief("Ezio", 17, 7, 3, Dice(6)),
        Archer("Oliver", 16, 7, 3, Dice(6)),
        Paladin("Isabella", 20, 6, 4, Dice(6)),
        Necromancer("Bob", 18, 6, 2, Dice(6))
    ]

    stats = {}

    print("[underline]Available characters:[/underline]")
    play_sound(default_path)
    for i, character in enumerate(characters):
        print(f"[bold]{i+1}. {character.get_type()}[/bold]")

    while True:
        try:
            choice = int(input("Select character 1: "))
            if 1 <= choice <= len(characters):
                car_1 = characters[choice - 1]
                characters.remove(car_1)
                car_1.play_sound(car_1.file_path)
                break
            else:
                print("Invalid choice. Please select a valid character.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

    print("\n[underline]Remaining characters:[/underline]")
    for i, character in enumerate(characters):
        print(f"[bold]{i+1}. {character.get_type()}[/bold]")

    while True:
        try:
            choice = int(input("Select character 2: "))
            if 1 <= choice <= len(characters):
                car_2 = characters[choice - 1]
                break
            else:
                print("Invalid choice. Please select a valid character.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

    stats[car_1.get_type()] = 0
    stats[car_2.get_type()] = 0

    for i in range(0, 100):
        car_1.regenerate()
        car_2.regenerate()
        while car_1.is_alive() and car_2.is_alive():
            car_1.attack(car_2)
            car_2.attack(car_1)
        if car_1.is_alive():
            stats[car_1.get_type()] += 1
        else:
            stats[car_2.get_type()] += 1

    print("\n[underline]Battle stats:[/underline]")
    for character_type, count in stats.items():
        print(f"{character_type}: {count} wins")

    max_wins = max(stats.values())
    winners = [character_type for character_type,
               count in stats.items() if count == max_wins]
    if len(winners) == 1:
        print(f"\nThe winner is: {winners[0]}")
    else:
        print("There is a tie between the following characters:")
        for winner in winners:
            print(winner)
