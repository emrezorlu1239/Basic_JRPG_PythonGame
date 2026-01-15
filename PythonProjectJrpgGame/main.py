import time
import sys


class GameCharacter:
    def __init__(self, name, health, speed, shield, damage, position, attack_range):
        self.name = name
        self.health = health
        self.max_health = health
        self.speed = speed
        self.shield = shield
        self.damage = damage
        self.position = position
        self.attack_range = attack_range
        self.is_alive = True
        self.inventory = {
            "health_potion": 1,
            "strength_potion": 1,
            "speed_potion": 1
        }
        self.potion_used = False

    def get_distance(self, target):
        return abs(self.position - target.position)

    def move(self, amount):
        actual_move = min(abs(amount), self.speed)
        if amount < 0:
            self.position -= actual_move
        else:
            self.position += actual_move
        print(f"-> {self.name} moved to position {self.position}")

    def basic_attack(self, target):
        distance = self.get_distance(target)
        if distance <= self.attack_range:
            print(f">>> {self.name} attacks {target.name}!")
            target.take_damage(self.damage)
        else:
            print(f"[!] {target.name} is too far! (Distance: {distance}, Range: {self.attack_range})")

    def use_potion(self, potion_type):
        if self.potion_used:
            print("Already used a potion in this match!")
            return False

        if self.inventory.get(potion_type, 0) > 0:
            if potion_type == "health_potion":
                self.health = min(self.health + 50, self.max_health)
                print("Potion Used: Healed 50 HP!")
            elif potion_type == "strength_potion":
                self.damage += 15
                print("Potion Used: Damage increased by 15!")
            elif potion_type == "speed_potion":
                self.speed += 5
                print("Potion Used: Speed increased by 5!")

            self.inventory[potion_type] -= 1
            self.potion_used = True
        else:
            print("Potion not available!")

    def take_damage(self, incoming_damage):
        if self.shield > 0:
            if self.shield > incoming_damage:
                self.shield -= incoming_damage
                print(f"Shield absorbed damage! Remaining Shield: {self.shield}")
            elif self.shield == incoming_damage:
                self.shield = 0
                print("Shield broken!")
            else:
                leftover_damage = incoming_damage - self.shield
                self.shield = 0
                self.health -= leftover_damage
                print(f"Shield broken! {leftover_damage} damage taken to health.")
        else:
            self.health -= incoming_damage
            print(f"Direct hit! Remaining Health: {self.health}")

        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"XXX {self.name} has been defeated! XXX")


class Knight(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 150, 5, 100, 20, position, attack_range=2)

    def shield_bash(self, target):
        if self.get_distance(target) <= 4:
            print(f"[*] {self.name} uses SHIELD BASH!")
            target.take_damage(self.damage + 10)
        else:
            print("Target too far for Shield Bash!")

    def iron_skin(self, target=None):
        self.shield += 40
        print(f"[*] {self.name} uses IRON SKIN! Shield reinforced.")


class Archer(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 80, 12, 20, 15, position, attack_range=15)

    def double_shot(self, target):
        if self.get_distance(target) <= self.attack_range:
            print(f"[*] {self.name} uses DOUBLE SHOT!")
            target.take_damage(self.damage)
            target.take_damage(self.damage)
        else:
            print(f"Target too far for Double Shot!")

    def focus_aim(self, target=None):
        self.attack_range += 5
        self.damage += 10
        print(f"[*] {self.name} is focusing! Range and Damage increased.")


class Mage(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 70, 7, 30, 40, position, attack_range=12)

    def fireball(self, target):
        if self.get_distance(target) <= 15:
            print(f"[*] {self.name} casts FIREBALL!")
            target.take_damage(self.damage + 20)
        else:
            print("Target too far!")

    def mana_shield(self, target=None):
        self.shield += 60
        print(f"[*] {self.name} activated Mana Shield!")


class Assassin(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 90, 15, 10, 30, position, attack_range=3)

    def backstab(self, target):
        if self.get_distance(target) <= 2:
            print(f"[*] {self.name} performs BACKSTAB!")
            target.take_damage(self.damage * 3)
        else:
            print("Target too far!")

    def shadow_step(self, target):
        self.position = target.position - 1
        print(f"[*] {self.name} teleported behind {target.name}!")


class Paladin(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 130, 6, 60, 25, position, attack_range=4)

    def holy_light(self, target=None):
        self.health = min(self.health + 30, self.max_health)
        print(f"[*] {self.name} used Holy Light! Healed self.")

    def retribution(self, target):
        if self.get_distance(target) <= self.attack_range:
            damage_to_deal = self.damage + (self.max_health - self.health) * 0.5
            print(f"[*] {self.name} uses Retribution!")
            target.take_damage(damage_to_deal)
        else:
            print("Target too far!")


class Healer(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 80, 8, 40, 10, position, attack_range=10)

    def divine_heal(self, target):
        heal_amount = 50
        target.health = min(target.health + heal_amount, target.max_health)
        print(f"[*] {self.name} healed {target.name} for {heal_amount} HP!")

    def holy_barrier(self, target):
        target.shield += 30
        print(f"[*] {self.name} placed a barrier on {target.name}!")


class Berserker(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 120, 10, 0, 35, position, attack_range=3)

    def blood_lust(self, target):
        if self.get_distance(target) <= self.attack_range:
            missing_health = self.max_health - self.health
            bonus_damage = missing_health * 0.4
            print(f"[*] {self.name} uses BLOOD LUST!")
            target.take_damage(self.damage + bonus_damage)
        else:
            print("Target too far!")

    def reckless_swing(self, target):
        if self.get_distance(target) <= self.attack_range:
            print(f"[*] {self.name} uses Reckless Swing!")
            self.health -= 10
            target.take_damage(self.damage + 25)
        else:
            print("Target too far!")


class Guardian(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 200, 4, 150, 15, position, attack_range=2)

    def taunt(self, target):
        print(f"[*] {self.name} taunted {target.name}! Enemy focus shifted.")

    def fortress_mode(self, target=None):
        self.shield += 100
        self.speed = 0
        print(f"[*] {self.name} entered Fortress Mode! Cannot move but massive shield added.")


class Necromancer(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 90, 6, 20, 25, position, attack_range=10)

    def life_steal(self, target):
        if self.get_distance(target) <= self.attack_range:
            damage = 30
            target.take_damage(damage)
            self.health = min(self.health + (damage // 2), self.max_health)
            print(f"[*] {self.name} stole life from {target.name}!")
        else:
            print("Target too far!")

    def soul_sacrifice(self, target=None):
        self.health -= 20
        self.damage += 20
        print(f"[*] {self.name} sacrificed health for dark power!")


class Rogue(GameCharacter):
    def __init__(self, name, position):
        super().__init__(name, 95, 14, 30, 22, position, attack_range=4)

    def poison_blade(self, target):
        if self.get_distance(target) <= self.attack_range:
            print(f"[*] {self.name} applied poison to {target.name}!")
            target.take_damage(self.damage + 15)
        else:
            print("Target too far!")

    def dodge(self, target=None):
        self.shield += 25
        self.speed += 5
        print(f"[*] {self.name} is preparing to dodge! Shield and Speed increased.")


AVAILABLE_CLASSES = (
    ("Knight", Knight, "Tank | High Shield, Short Range"),
    ("Archer", Archer, "Ranged | High Range, Medium Dmg"),
    ("Mage", Mage, "Magic | High Dmg, Low HP"),
    ("Assassin", Assassin, "Burst | Very High Dmg, Low Def"),
    ("Paladin", Paladin, "Hybrid | Heals Self & Tanks"),
    ("Healer", Healer, "Support | Heals & Buffs Allies"),
    ("Berserker", Berserker, "Fighter | Low HP = High Dmg"),
    ("Guardian", Guardian, "Super Tank | Massive HP, Slow"),
    ("Necromancer", Necromancer, "Dark | Lifesteal mechanics"),
    ("Rogue", Rogue, "Agile | Poison, Dodge")
)


def show_class_info():

    print("\n" + "=" * 70)
    print(f"{'No':<4} {'Class':<15} {'HP':<6} {'Shield':<8} {'Dmg':<6} {'Rng':<6} {'Spd':<5}")
    print("-" * 70)
    for idx, (name, cls, desc) in enumerate(AVAILABLE_CLASSES):
        dummy = cls("Info", 0)
        print(
            f"{idx + 1:<4} {name:<15} {dummy.max_health:<6} {dummy.shield:<8} {dummy.damage:<6} {dummy.attack_range:<6} {dummy.speed:<5}")
        print(f"     ↳ {desc}")
    print("=" * 70 + "\n")
    input("Press Enter to return to menu...")


def show_game_mechanics():
    print("\n" + "=" * 30 + " GAME MECHANICS " + "=" * 30)
    print("1. MOVEMENT:")
    print("   - You can move left (-) or right (+).")
    print("   - Max movement is limited by your Speed stat.")
    print("\n2. ATTACKING:")
    print("   - Basic Attacks deal damage based on your Damage stat.")
    print("   - You must be within Range to hit an enemy.")
    print("\n3. DEFENSE:")
    print("   - Damage hits Shield first. If Shield breaks, HP is taken.")
    print("   - When HP reaches 0, the character dies.")
    print("\n4. INVENTORY:")
    print("   - Each character has 1 Health, 1 Strength, and 1 Speed potion.")
    print("   - You can only use 1 potion per match per character.")
    print("\n5. VICTORY:")
    print("   - Defeat all 4 enemy characters to win.")
    print("=" * 76 + "\n")
    input("Press Enter to return to menu...")


def select_team(player_name, start_pos_base):
    team = []
    print(f"\n{'#' * 20} {player_name} TEAM SELECTION {'#' * 20}")
    print(f"{player_name}, please select 4 characters from the list.")

    while len(team) < 4:
        print(f"\n---> {player_name}, Select Character {len(team) + 1}:")

        for idx, (name, _, _) in enumerate(AVAILABLE_CLASSES):
            print(f"{idx + 1}. {name}")

        choice = input(f"Choice (1-10): ").strip()

        try:
            selection_idx = int(choice) - 1
            if 0 <= selection_idx < len(AVAILABLE_CLASSES):
                class_name, class_ref, _ = AVAILABLE_CLASSES[selection_idx]

                char_name = f"{player_name[:2]}_{class_name}_{len(team) + 1}"
                pos = start_pos_base + (len(team) * 3)

                new_char = class_ref(char_name, pos)
                team.append(new_char)
                print(f"✅ {class_name} added! (Pos: {pos})")
            else:
                print("❌ Please enter a number between 1 and 10.")
        except ValueError:
            print("❌ Invalid input! Enter a number.")

    return team


def get_special_skills(character):
    if isinstance(character, Knight):
        return [("Shield Bash", "shield_bash", 1), ("Iron Skin", "iron_skin", 0)]
    elif isinstance(character, Archer):
        return [("Double Shot", "double_shot", 1), ("Focus Aim", "focus_aim", 0)]
    elif isinstance(character, Mage):
        return [("Fireball", "fireball", 1), ("Mana Shield", "mana_shield", 0)]
    elif isinstance(character, Assassin):
        return [("Backstab", "backstab", 1), ("Shadow Step", "shadow_step", 1)]
    elif isinstance(character, Paladin):
        return [("Holy Light", "holy_light", 0), ("Retribution", "retribution", 1)]
    elif isinstance(character, Healer):
        return [("Divine Heal", "divine_heal", 1), ("Holy Barrier", "holy_barrier", 1)]
    elif isinstance(character, Berserker):
        return [("Blood Lust", "blood_lust", 1), ("Reckless Swing", "reckless_swing", 1)]
    elif isinstance(character, Guardian):
        return [("Taunt", "taunt", 1), ("Fortress Mode", "fortress_mode", 0)]
    elif isinstance(character, Necromancer):
        return [("Life Steal", "life_steal", 1), ("Soul Sacrifice", "soul_sacrifice", 0)]
    elif isinstance(character, Rogue):
        return [("Poison Blade", "poison_blade", 1), ("Dodge", "dodge", 0)]
    return []


def draw_battlefield(team1, team2):
    print("\n" + "=" * 25 + " BATTLEFIELD " + "=" * 25)
    line = ["."] * 51

    for c in team1:
        if c.is_alive:
            idx = max(0, min(50, int(c.position / 2)))
            line[idx] = "1"
    for c in team2:
        if c.is_alive:
            idx = max(0, min(50, int(c.position / 2)))
            line[idx] = "2"

    print("".join(line))
    print("0 (Left/P1)" + " " * 38 + "100 (Right/P2)")
    print("=" * 63 + "\n")


def battle_loop(team1, team2):
    turn = 1
    while True:
        if not any(c.is_alive for c in team1):
            print("\n" + "!" * 20 + " GAME OVER " + "!" * 20)
            print("🏆 PLAYER 2 WINS! 🏆")
            return
        if not any(c.is_alive for c in team2):
            print("\n" + "!" * 20 + " GAME OVER " + "!" * 20)
            print("🏆 PLAYER 1 WINS! 🏆")
            return

        current_team = team1 if turn % 2 != 0 else team2
        enemy_team = team2 if turn % 2 != 0 else team1
        p_name = "PLAYER 1" if turn % 2 != 0 else "PLAYER 2"

        print(f"\n>>> TURN {turn}: {p_name} <<<")
        draw_battlefield(team1, team2)

        alive_chars = [c for c in current_team if c.is_alive]
        print(f"{p_name}, select your character:")
        for i, c in enumerate(alive_chars):
            print(f"{i + 1}. {c.name} (HP:{c.health}/{c.max_health}, Shield:{c.shield}, Pos:{c.position})")

        try:
            char_choice_in = input("Select Character No: ")
            char_choice = int(char_choice_in) - 1
            if not (0 <= char_choice < len(alive_chars)):
                print("Invalid selection!");
                continue
            actor = alive_chars[char_choice]
        except:
            print("Invalid input!");
            continue

        print(f"\nSelected: {actor.name}")
        print("1. Move")
        print("2. Basic Attack")
        print("3. Use Potion")

        skills = get_special_skills(actor)
        if skills:
            print(f"4. Skill: {skills[0][0]}")
            print(f"5. Skill: {skills[1][0]}")
        print("6. Pass Turn")

        action = input("Select Action: ")

        if action == "1":
            try:
                dist = int(input(f"Enter Distance (Max Speed {actor.speed}): "))
                direction = input("Direction (1: Right/Forward, 2: Left/Back): ")
                move_amnt = dist if direction == "1" else -dist
                actor.move(move_amnt)
            except:
                print("Invalid movement input.")

        elif action == "2":
            print("\nSelect Target:")
            targets = [t for t in enemy_team if t.is_alive]
            for i, t in enumerate(targets):
                print(f"{i + 1}. {t.name} (HP:{t.health}, Dist: {actor.get_distance(t)})")

            try:
                t_sel = int(input("Target No: ")) - 1
                if 0 <= t_sel < len(targets):
                    actor.basic_attack(targets[t_sel])
                else:
                    print("Invalid target.")
            except:
                print("Error selecting target.")

        elif action == "3":
            print(f"Inventory: {actor.inventory}")
            pot = input("1:Health, 2:Strength, 3:Speed -> ")
            mapping = {"1": "health_potion", "2": "strength_potion", "3": "speed_potion"}
            if pot in mapping:
                actor.use_potion(mapping[pot])
            else:
                print("Invalid potion.")

        elif action == "4" or action == "5":
            idx = 0 if action == "4" else 1
            s_name, method_name, need_target = skills[idx]
            method = getattr(actor, method_name)

            if need_target == 1:
                print(f"\nSelect target for {s_name}:")
                all_targets = [t for t in enemy_team + current_team if t.is_alive and t != actor]
                for i, t in enumerate(all_targets):
                    role = "[ENEMY]" if t in enemy_team else "[ALLY]"
                    print(f"{i + 1}. {role} {t.name} (Dist: {actor.get_distance(t)})")

                try:
                    t_sel = int(input("Target No: ")) - 1
                    if 0 <= t_sel < len(all_targets):
                        method(all_targets[t_sel])
                    else:
                        print("Invalid target.")
                except:
                    print("Error.")
            else:
                try:
                    method()
                except TypeError:
                    method(None)

        print("\nEnd of Turn.")
        turn += 1
        time.sleep(1)


def main_menu():
    while True:
        print("\n" + "=" * 40)
        print("       CONSOLE BATTLE ARENA       ")
        print("=" * 40)
        print("1. All Character Info")
        print("2. Game Mechanics")
        print("3. START GAME")
        print("4. Exit Game")
        print("=" * 40)

        choice = input("Select Option (1-4): ")

        if choice == "1":
            show_class_info()
        elif choice == "2":
            show_game_mechanics()
        elif choice == "3":
            return True
        elif choice == "4":
            print("Exiting game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")


def game_over_menu():
    while True:
        print("\n" + "=" * 30)
        print("      MATCH FINISHED      ")
        print("=" * 30)
        print("1. Play Again")
        print("2. Main Menu")
        print("3. Exit Game")
        print("=" * 30)

        choice = input("Select Option (1-3): ")

        if choice == "1":
            return "restart"
        elif choice == "2":
            return "menu"
        elif choice == "3":
            print("Exiting game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.")


def main():
    while True:
        if main_menu():
            while True:
                p1_team = select_team("PLAYER 1", start_pos_base=0)
                print("\n" + "*" * 50 + "\n")
                p2_team = select_team("PLAYER 2", start_pos_base=90)

                print("\n⚠️  TEAMS READY! BATTLE STARTING... ⚠️")
                time.sleep(1)

                battle_loop(p1_team, p2_team)

                end_choice = game_over_menu()

                if end_choice == "menu":
                    break
                elif end_choice == "restart":
                    continue


if __name__ == "__main__":
    main()
