import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulator import Game, Player, create_card, CardDatabase
from simulator.enums import Zone

# Setup
CardDatabase.get_instance().load()
p1 = Player("P1")
p2 = Player("P2")
game = Game()
game.setup(p1, p2)

print("\n--- Diagnostic Start ---")
champ = create_card("CS2_222", game) # Stormwind Champion
champ.controller = p1
p1.summon(champ)

print(f"Champion: {champ.name}, Zone: {champ.zone}, Controller: {champ.controller.name}")
print(f"Triggers for on_calculate_attack: {len(game._triggers.get('on_calculate_attack', []))}")

minion = create_card("CS2_120", game) # River Crocolisk
minion.controller = p1
p1.summon(minion)

print(f"Minion: {minion.name}, Attack (base): {minion._attack}")

# Manual trigger test
modifier = {"amount": minion._attack}
print("Firing on_calculate_attack manually...")
game.fire_event("on_calculate_attack", minion, modifier)
print(f"Modifier after manual fire: {modifier['amount']}")

print(f"Minion.attack property result: {minion.attack}")
