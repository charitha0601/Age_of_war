from itertools import permutations

# Class advantage mapping
ADVANTAGE_MAP = {
    "Militia": ["Spearmen", "LightCavalry"],
    "Spearmen": ["LightCavalry", "HeavyCavalry"],
    "LightCavalry": ["FootArcher", "CavalryArcher"],
    "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
    "CavalryArcher": ["Spearmen", "HeavyCavalry"],
    "FootArcher": ["Militia", "CavalryArcher"]
}

class Platoon:
    def __init__(self, unit_class, count):
        self.unit_class = unit_class
        self.count = count

    def effective_strength(self, opponent):
        """
        Returns effective strength of the platoon against an opponent.
        Strength is doubled if class advantage applies.
        """
        if opponent.unit_class in ADVANTAGE_MAP.get(self.unit_class, []):
            return self.count * 2
        return self.count

    def __str__(self):
        return f"{self.unit_class}#{self.count}"

class Army:
    def __init__(self, platoons):
        self.platoons = platoons

    @staticmethod
    def from_string(data):
        units = []
        for part in data.strip().split(";"):
            unit, count = part.split("#")
            units.append(Platoon(unit.strip(), int(count.strip())))
        return Army(units)

class Battlefield:
    def __init__(self, own_army, opponent_army):
        self.own_army = own_army
        self.opponent_army = opponent_army

    def compare_platoons(self, own, opponent):
        """
        Compares two platoons and returns:
        1 → Win, 0 → Draw, -1 → Loss
        """
        own_strength = own.effective_strength(opponent)
        opp_strength = opponent.effective_strength(own)
        if own_strength > opp_strength:
            return 1
        elif own_strength == opp_strength:
            return 0
        else:
            return -1

    def count_outcomes(self, results):
        return results.count(1), results.count(0), results.count(-1)

    def find_winning_order(self):
        own = self.own_army.platoons
        opp = self.opponent_army.platoons
        min_wins = len(own) // 2 + 1

        # Try all permutations of your army
        for perm in permutations(own):
            results = [self.compare_platoons(a, b) for a, b in zip(perm, opp)]
            wins, draws, losses = self.count_outcomes(results)

            if wins >= min_wins:
                print("\nBattle Outcomes:")
                for i, (own_p, opp_p) in enumerate(zip(perm, opp), 1):
                    result = self.compare_platoons(own_p, opp_p)
                    outcome = "Win" if result == 1 else "Draw" if result == 0 else "Loss"
                    print(f"Battle {i}: {own_p} vs {opp_p} → {outcome}")
                order_str = ";".join(str(p) for p in perm)
                return order_str, wins, draws, losses

        return "There is no chance of winning", 0, 0, 0

def main():
    print("Battle Strategy Planner")

    print("Enter your army:")
    own_input = input().strip()
    print("Enter opponent army:")
    opp_input = input().strip()

    try:
        own_army = Army.from_string(own_input)
        opp_army = Army.from_string(opp_input)
    except Exception as e:
        print("Invalid input format. Please follow Class#Count;Class#Count;...")
        return

    battle = Battlefield(own_army, opp_army)
    result, wins, draws, losses = battle.find_winning_order()

    print("\nResult:")
    print(result)
    print(f"Wins: {wins}, Draws: {draws}, Losses: {losses}")

if __name__ == "__main__":
    main()
