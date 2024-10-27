import random
import csv

class Robot:
    def __init__(self, name, hitpoints, damage, defense, crit, speed, ultimate_charge, ultimate_power):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage
        self.defense = defense
        self.crit = crit
        self.speed = speed
        self.ultimate_charge = ultimate_charge
        self.ultimate_power = ultimate_power
        self.curr_charge = 0
        self.speed_residue = 0
        self.basic_attack_count = 0
        self.ultimate_count = 0

    def attack(self, opponent):
        critical_hit = random.random() < self.crit  # bool, random.random() gives 0-1
        damage = random.randint(10, self.damage)

        if critical_hit:
            damage = 3 * damage // 2  # int

        final_damage = max(0, damage - opponent.defense)
        opponent.hitpoints -= final_damage
        self.basic_attack_count += 1  # Increment basic attack

        critical_msg = "Critical hit!" if critical_hit else ""
        print(f"{self.name} attacks {opponent.name} for {final_damage} damage! {critical_msg}")

    def ultimate(self, opponent):
        ultimate_damage = self.damage * self.ultimate_power
        final_damage = max(0, ultimate_damage - opponent.defense)
        opponent.hitpoints -= final_damage
        print(f"{self.name} uses their ULTIMATE!")
        print(f"{self.name}'s ultimate deals {final_damage} damage to {opponent.name}!")
        self.curr_charge = 0  # Reset ultimate charge
        self.ultimate_count += 1  # Increment ultimate


class Battle:
    def __init__(self, robot1, robot2):
        self.robot1, self.robot2 = (robot1, robot2) if robot1.speed >= robot2.speed else (robot2, robot1)

    def start_fight(self):
        print(f"\nBattle Start! {self.robot1.name} vs {self.robot2.name}\n")
        round = 1

        while self.robot1.hitpoints > 0 and self.robot2.hitpoints > 0:
            print(f"Round {round}:")

            self.set_round(self.robot1, self.robot2)  # Robot 1 attacks Robot 2 first
            if self.robot2.hitpoints <= 0:
                self.final_msg(self.robot1, self.robot2)
                return

            self.set_round(self.robot2, self.robot1)
            if self.robot1.hitpoints <= 0:
                self.final_msg(self.robot2, self.robot1)
                return

            print("")
            round += 1

    def set_round(self, attacker, opponent):
        attacker.speed_residue += attacker.speed - opponent.speed  # Add residue, from 0

        # Check ultimate
        attacker.curr_charge += 1  # Ultimate only charge once per round, even if it gets extra attack
        if attacker.curr_charge >= attacker.ultimate_charge:
            attacker.ultimate(opponent)
        else:
            attacker.attack(opponent)  # If ultimate not ready, do an attack

        # Extra attack based on residue
        if attacker.speed_residue >= opponent.speed:
            print(f"{attacker.name} gets an extra attack due to speed!")
            attacker.speed_residue = 0  # Reset residue for each extra attack
            attacker.attack(opponent)

    def final_msg(self, win, lose):
        print(f"\n{lose.name} is defeated!")
        print(f"{win.name} wins!")
        print("\n=============================")
        print(f"Remaining hitpoints for {win.name}: {win.hitpoints}\n")
        print(f"{win.name}\n> Basic attacks: {win.basic_attack_count} times.")
        print(f"> Ultimates: {win.ultimate_count} times.")
        print(f"{lose.name}\n> Basic attacks: {lose.basic_attack_count} times.")
        print(f"> Ultimates: {lose.ultimate_count} times.")
        print("=============================")


class Game:
    def __init__(self):
        self.robots = []

    def add_robot(self, robot):
        self.robots.append(robot)

    def load_robots(self, filename):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    name = row['name']
                    hitpoints = int(row['hitpoints'])
                    damage = int(row['damage'])
                    defense = int(row['defense'])
                    crit = float(row['crit'])
                    speed = int(row['speed'])
                    ultimate_charge = int(row['ultimate_charge'])
                    ultimate_power = int(row['ultimate_power'])
                    robot = Robot(name, hitpoints, damage, defense, crit, speed, ultimate_charge, ultimate_power)

                    self.add_robot(robot)
            print(f"Robots loaded from {filename}.")
        except Exception as e:
            print(f"File {filename} error: {e}")

    def save_robot(self, filename, robot):
        try:
            with open(filename, 'a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([robot.name, robot.hitpoints, robot.damage, robot.defense, robot.crit, robot.speed, robot.ultimate_charge, robot.ultimate_power])
            print(f"{robot.name} saved to {filename}.")
        except Exception as e:
            print(f"Error saving robot to {filename}: {e}")

    def create_robot(self):
        name = input("> Enter robot name: ")
        hitpoints = int(input("> Enter hitpoints: "))
        damage = int(input("> Enter attack damage: "))
        defense = int(input("> Enter defense: "))
        crit = float(input("> Enter critical hit (0-1): "))
        speed = int(input("> Enter speed: "))
        ultimate_charge = int(input("> Enter rounds to charge ultimate: "))
        ultimate_power = int(input("> Enter ultimate power multiplier: "))
        return Robot(name, hitpoints, damage, defense, crit, speed, ultimate_charge, ultimate_power)

    def display_robots(self):
        print("\nRobots available:")
        for i, robot in enumerate(self.robots):
            print(f"{i + 1}. {robot.name} (Hitpoints: {robot.hitpoints}, Attack: {robot.damage}, Defense: {robot.defense}, Speed: {robot.speed}, Ultimate Charge: {robot.ultimate_charge})")

    def choose_robot(self, text):
        choice = int(input(text)) - 1
        if choice in range(len(self.robots)):
            return self.robots[choice]
        else:
            print("Invalid choice, please select again.")
            return self.choose_robot()

    def start_game(self):
        self.display_robots()
        robot1 = self.choose_robot("> Select the first robot: ")
        robot2 = self.choose_robot("> Select the second robot: ")

        battle = Battle(robot1, robot2)
        battle.start_fight()


def main():
    game = Game()

    file = "robots.csv"
    game.load_robots(file)

    create_new_robot = str(input("Create a new robot? (y/n): ")).lower()
    yes = {'yes', 'y', 'ye', 'iya', 'ya'}
    if create_new_robot in yes:
        new_robot = game.create_robot()
        game.add_robot(new_robot)
        game.save_robot(file, new_robot)

    game.start_game()

main()
