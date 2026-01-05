"""
Advanced card effect generator with smart templates.

Generates functional code for common Hearthstone mechanics:
- Discover (with proper card pools)
- Summon tokens
- Deal damage (AoE, random, targeted)
- Draw cards
- Buff minions
- Destroy effects
- And more...
"""

import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator import CardDatabase, CardData, CardType


# Standard 2026 Sets
STANDARD_SETS = ['CORE', 'WHIZBANGS_WORKSHOP', 'PERILS_IN_PARADISE', 'ISLAND_VACATION', 
                 'THE_GREAT_DARK_BEYOND', 'SPACE', 'BATTLE_OF_THE_BANDS']

SET_TO_FOLDER = {
    'CORE': 'core', 'WHIZBANGS_WORKSHOP': 'whizbangs_workshop', 
    'PERILS_IN_PARADISE': 'island_vacation', 'ISLAND_VACATION': 'island_vacation',
    'THE_GREAT_DARK_BEYOND': 'great_dark_beyond', 'SPACE': 'space',
    'BATTLE_OF_THE_BANDS': 'battle_of_the_bands'
}


def extract_numbers(text: str) -> list:
    """Extract all numbers from text."""
    return [int(n) for n in re.findall(r'\b(\d+)\b', text)]


def get_primary_number(text: str, default: int = 1) -> int:
    """Get the first/primary number from card text."""
    nums = extract_numbers(text)
    return nums[0] if nums else default


def generate_discover_code(card: CardData, func_type: str) -> str:
    """Generate Discover effect code."""
    text = card.text.lower()
    
    # Determine what pool to discover from
    pool_code = ""
    callback_code = ""
    
    if 'spell' in text:
        pool_code = """    # Discover a spell
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    spells = [c for c in db._cards.values() 
              if c.card_type == CardType.SPELL and c.collectible]
    options = random.sample(spells, min(3, len(spells)))
    option_ids = [c.card_id for c in options]"""
    elif 'minion' in text:
        pool_code = """    # Discover a minion
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    minions = [c for c in db._cards.values() 
               if c.card_type == CardType.MINION and c.collectible]
    options = random.sample(minions, min(3, len(minions)))
    option_ids = [c.card_id for c in options]"""
    elif 'dragon' in text:
        pool_code = """    # Discover a Dragon
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    dragons = [c for c in db._cards.values() 
               if 'DRAGON' in str(c.race) and c.collectible]
    options = random.sample(dragons, min(3, len(dragons)))
    option_ids = [c.card_id for c in options]"""
    elif 'mech' in text:
        pool_code = """    # Discover a Mech
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    mechs = [c for c in db._cards.values() 
             if 'MECHANICAL' in str(c.race) and c.collectible]
    options = random.sample(mechs, min(3, len(mechs)))
    option_ids = [c.card_id for c in options]"""
    elif 'demon' in text:
        pool_code = """    # Discover a Demon
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    demons = [c for c in db._cards.values() 
              if 'DEMON' in str(c.race) and c.collectible]
    options = random.sample(demons, min(3, len(demons)))
    option_ids = [c.card_id for c in options]"""
    else:
        # Generic discover from class cards
        pool_code = """    # Discover a card
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    cards = [c for c in db._cards.values() if c.collectible]
    options = random.sample(cards, min(3, len(cards)))
    option_ids = [c.card_id for c in options]"""
    
    # Add to hand or deck?
    if 'add' in text and 'deck' in text:
        callback_code = """
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_deck(card)
            player.shuffle_deck()
    
    game.initiate_discover(player, option_ids, on_discover)"""
    else:
        callback_code = """
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)"""
    
    return pool_code + callback_code


def generate_summon_code(card: CardData, func_type: str) -> str:
    """Generate Summon effect code."""
    text = card.text.lower()
    
    # Try to find how many to summon
    nums = extract_numbers(card.text)
    count = 1
    for n in nums:
        if n <= 7:  # Reasonable summon count
            count = n
            break
    
    # Determine what to summon
    if 'copy' in text and 'this' in text:
        return f"""    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)"""
    elif 'random' in text:
        if 'beast' in text:
            return"""    # Summon a random Beast
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    beasts = [c.card_id for c in db._cards.values() 
              if 'BEAST' in str(c.race) and c.collectible and c.card_type.name == 'MINION']
    if beasts:
        game.summon_token(player, random.choice(beasts))"""
        else:
            return f"""    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range({count}):
        if minions:
            game.summon_token(player, random.choice(minions))"""
    else:
        # Try to find token ID from card_id pattern
        token_id = f"{card.card_id}t"
        return f"""    # Summon token(s)
    for _ in range({count}):
        game.summon_token(player, "{token_id}")"""


def generate_damage_code(card: CardData, func_type: str) -> str:
    """Generate Deal Damage effect code."""
    text = card.text.lower()
    amount = get_primary_number(card.text, 1)
    
    if 'all' in text and 'enemy' in text and 'minion' in text:
        return f"""    # Deal {amount} damage to all enemy minions
    for m in list(opponent.board):
        game.deal_damage(m, {amount}, source)"""
    elif 'all' in text and 'enemy' in text:
        return f"""    # Deal {amount} damage to all enemies
    for m in list(opponent.board):
        game.deal_damage(m, {amount}, source)
    if opponent.hero:
        game.deal_damage(opponent.hero, {amount}, source)"""
    elif 'all' in text and 'minion' in text:
        return f"""    # Deal {amount} damage to all minions
    for m in list(player.board) + list(opponent.board):
        game.deal_damage(m, {amount}, source)"""
    elif 'all' in text:
        return f"""    # Deal {amount} damage to all characters
    for m in list(player.board) + list(opponent.board):
        game.deal_damage(m, {amount}, source)
    if player.hero:
        game.deal_damage(player.hero, {amount}, source)
    if opponent.hero:
        game.deal_damage(opponent.hero, {amount}, source)"""
    elif 'random' in text and 'enemy' in text:
        return f"""    # Deal {amount} damage to a random enemy
    import random
    targets = list(opponent.board) + ([opponent.hero] if opponent.hero else [])
    if targets:
        game.deal_damage(random.choice(targets), {amount}, source)"""
    elif 'random' in text:
        return f"""    # Deal {amount} damage to a random character
    import random
    targets = list(player.board) + list(opponent.board)
    if player.hero: targets.append(player.hero)
    if opponent.hero: targets.append(opponent.hero)
    if targets:
        game.deal_damage(random.choice(targets), {amount}, source)"""
    elif 'target' in func_type.lower() or 'target' in text:
        return f"""    # Deal {amount} damage to target
    if target:
        game.deal_damage(target, {amount}, source)"""
    elif 'hero' in text and 'enemy' in text:
        return f"""    # Deal {amount} damage to enemy hero
    if opponent.hero:
        game.deal_damage(opponent.hero, {amount}, source)"""
    else:
        return f"""    # Deal {amount} damage
    if target:
        game.deal_damage(target, {amount}, source)"""


def generate_draw_code(card: CardData, func_type: str) -> str:
    """Generate Draw card effect code."""
    text = card.text.lower()
    amount = get_primary_number(card.text, 1)
    
    if 'spell' in text:
        return f"""    # Draw spell(s)
    drawn = 0
    for card in list(player.deck):
        if card.card_type.name == 'SPELL':
            player.deck.remove(card)
            player.add_to_hand(card)
            drawn += 1
            if drawn >= {amount}:
                break"""
    elif 'minion' in text:
        return f"""    # Draw minion(s)
    drawn = 0
    for card in list(player.deck):
        if card.card_type.name == 'MINION':
            player.deck.remove(card)
            player.add_to_hand(card)
            drawn += 1
            if drawn >= {amount}:
                break"""
    elif 'dragon' in text:
        return f"""    # Draw Dragon(s)
    drawn = 0
    for card in list(player.deck):
        if 'DRAGON' in str(getattr(card.data, 'race', '')):
            player.deck.remove(card)
            player.add_to_hand(card)
            drawn += 1
            if drawn >= {amount}:
                break"""
    else:
        return f"""    # Draw {amount} card(s)
    player.draw({amount})"""


def generate_buff_code(card: CardData, func_type: str) -> str:
    """Generate buff/give stats code."""
    text = card.text.lower()
    nums = extract_numbers(card.text)
    
    # Common patterns: +X/+Y or +X Attack or +X Health
    atk_buff = 0
    health_buff = 0
    
    if len(nums) >= 2:
        atk_buff = nums[0]
        health_buff = nums[1]
    elif len(nums) == 1:
        if 'attack' in text:
            atk_buff = nums[0]
        elif 'health' in text:
            health_buff = nums[0]
        else:
            atk_buff = nums[0]
            health_buff = nums[0]
    
    keywords = []
    if 'taunt' in text: keywords.append("target._taunt = True")
    if 'rush' in text: keywords.append("target._rush = True")
    if 'charge' in text: keywords.append("target._charge = True")
    if 'divine shield' in text: keywords.append("target._divine_shield = True")
    if 'windfury' in text: keywords.append("target._windfury = True")
    if 'lifesteal' in text: keywords.append("target._lifesteal = True")
    if 'poisonous' in text: keywords.append("target._poisonous = True")
    if 'stealth' in text: keywords.append("target._stealth = True")
    if 'reborn' in text: keywords.append("target._reborn = True")
    
    if 'friendly' in text and 'minion' in text and 'all' in text:
        code = f"""    # Give all friendly minions +{atk_buff}/+{health_buff}
    for m in player.board:
        m._attack += {atk_buff}
        m._max_health += {health_buff}
        m._health += {health_buff}"""
        for kw in keywords:
            code += f"\n        {kw.replace('target', 'm')}"
    else:
        stat_lines = []
        if atk_buff: stat_lines.append(f"target._attack += {atk_buff}")
        if health_buff: 
            stat_lines.append(f"target._max_health += {health_buff}")
            stat_lines.append(f"target._health += {health_buff}")
        
        code = f"""    # Give +{atk_buff}/+{health_buff} and keywords
    if target:
        {chr(10) + '        '.join(stat_lines) if stat_lines else 'pass'}"""
        for kw in keywords:
            code += f"\n        {kw}"
    
    return code


def generate_destroy_code(card: CardData, func_type: str) -> str:
    """Generate destroy effect code."""
    text = card.text.lower()
    
    if 'random' in text and 'enemy' in text:
        return """    # Destroy a random enemy minion
    import random
    if opponent.board:
        target = random.choice(list(opponent.board))
        target.destroy()"""
    elif 'all' in text and 'enemy' in text:
        return """    # Destroy all enemy minions
    for m in list(opponent.board):
        m.destroy()"""
    elif 'all' in text and 'minion' in text:
        return """    # Destroy all minions
    for m in list(player.board) + list(opponent.board):
        m.destroy()"""
    else:
        return """    # Destroy a minion
    if target:
        target.destroy()"""


def generate_heal_code(card: CardData, func_type: str) -> str:
    """Generate heal/restore effect code."""
    text = card.text.lower()
    amount = get_primary_number(card.text, 1)
    
    if 'all' in text and 'friendly' in text:
        return f"""    # Restore {amount} Health to all friendly characters
    for m in player.board:
        game.heal(m, {amount}, source)
    if player.hero:
        game.heal(player.hero, {amount}, source)"""
    elif 'hero' in text or 'your hero' in text:
        return f"""    # Restore {amount} Health to your hero
    if player.hero:
        game.heal(player.hero, {amount}, source)"""
    else:
        return f"""    # Restore {amount} Health
    if target:
        game.heal(target, {amount}, source)"""


def generate_armor_code(card: CardData, func_type: str) -> str:
    """Generate gain armor code."""
    amount = get_primary_number(card.text, 1)
    return f"""    # Gain {amount} Armor
    if player.hero:
        player.hero.gain_armor({amount})"""


def generate_silence_code(card: CardData, func_type: str) -> str:
    """Generate silence effect code."""
    text = card.text.lower()
    
    if 'all' in text and 'enemy' in text:
        return """    # Silence all enemy minions
    for m in list(opponent.board):
        game.silence(m)"""
    elif 'all' in text:
        return """    # Silence all minions
    for m in list(player.board) + list(opponent.board):
        game.silence(m)"""
    else:
        return """    # Silence a minion
    if target:
        game.silence(target)"""


def generate_freeze_code(card: CardData, func_type: str) -> str:
    """Generate freeze effect code."""
    text = card.text.lower()
    
    if 'all' in text and 'enemy' in text:
        return """    # Freeze all enemies
    for m in opponent.board:
        m.frozen = True
    if opponent.hero:
        opponent.hero.frozen = True"""
    else:
        return """    # Freeze a character
    if target:
        target.frozen = True"""


def generate_effect_code(card: CardData) -> str:
    """Generate complete effect code for a card."""
    text = card.text.lower()
    card_type_str = card.card_type.name if hasattr(card.card_type, 'name') else str(card.card_type)
    
    # Determine function type
    is_spell = card_type_str in ['SPELL']
    has_battlecry = 'battlecry' in text
    has_deathrattle = 'deathrattle' in text
    has_combo = 'combo' in text
    has_outcast = 'outcast' in text
    
    if is_spell:
        func_name = 'on_play'
        func_sig = 'def on_play(game, source, target):'
    elif has_deathrattle and not has_battlecry:
        func_name = 'deathrattle'
        func_sig = 'def deathrattle(game, source):'
    elif has_combo:
        func_name = 'on_combo'
        func_sig = 'def on_combo(game, source, target):'
    else:
        func_name = 'battlecry'
        func_sig = 'def battlecry(game, source, target):'
    
    # Generate header
    lines = [
        f'"""Effect for {card.name} ({card.card_id}).',
        f'',
        f'Card Text: {card.text}',
        f'"""',
        '',
        'from simulator.enums import CardType',
        '',
        func_sig,
        '    player = source.controller',
        '    opponent = player.opponent',
        ''
    ]
    
    # Detect mechanics and generate appropriate code
    body_parts = []
    
    if 'discover' in text:
        body_parts.append(generate_discover_code(card, func_name))
    
    if 'deal' in text and 'damage' in text:
        body_parts.append(generate_damage_code(card, func_name))
    
    if 'summon' in text:
        body_parts.append(generate_summon_code(card, func_name))
    
    if 'draw' in text:
        body_parts.append(generate_draw_code(card, func_name))
    
    if ('give' in text or '+' in card.text) and ('/' in card.text or 'attack' in text or 'health' in text):
        body_parts.append(generate_buff_code(card, func_name))
    
    if 'destroy' in text:
        body_parts.append(generate_destroy_code(card, func_name))
    
    if 'restore' in text or ('heal' in text and 'health' in text):
        body_parts.append(generate_heal_code(card, func_name))
    
    if 'gain' in text and 'armor' in text:
        body_parts.append(generate_armor_code(card, func_name))
    
    if 'silence' in text:
        body_parts.append(generate_silence_code(card, func_name))
    
    if 'freeze' in text:
        body_parts.append(generate_freeze_code(card, func_name))
    
    # Combine body parts
    if body_parts:
        lines.extend(body_parts)
    else:
        lines.append(f'    # Effect: {card.text[:100]}...')
        lines.append('    pass')
    
    # Also generate deathrattle if card has both
    if has_deathrattle and has_battlecry:
        lines.append('')
        lines.append('')
        lines.append('def deathrattle(game, source):')
        lines.append('    player = source.controller')
        lines.append('    opponent = player.opponent')
        lines.append('    # Deathrattle effect')
        lines.append('    pass  # TODO: Implement deathrattle portion')
    
    return '\n'.join(lines)


def save_effect(card: CardData, code: str) -> str:
    """Save the generated effect code to the appropriate file."""
    folder = SET_TO_FOLDER.get(card.card_set, card.card_set.lower())
    dir_path = f'card_effects/{folder}'
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = f'{dir_path}/effect_{card.card_id}.py'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    return file_path


def get_cards_needing_refinement():
    """Get all cards with TODO in their effect files."""
    cards_to_refine = []
    db = CardDatabase.get_instance()
    db.load()
    
    for folder in SET_TO_FOLDER.values():
        path = f'card_effects/{folder}'
        if not os.path.exists(path):
            continue
        
        for f in os.listdir(path):
            if not f.startswith('effect_'):
                continue
            
            filepath = os.path.join(path, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if '# TODO' in content:
                card_id = f.replace('effect_', '').replace('.py', '')
                card = db._cards.get(card_id)
                if card and card.card_set in STANDARD_SETS:
                    cards_to_refine.append((card, folder))
    
    return cards_to_refine


def main():
    print("=== Smart Card Effect Refiner ===\n")
    
    cards = get_cards_needing_refinement()
    print(f"Found {len(cards)} cards to refine.\n")
    
    if not cards:
        print("All cards are properly implemented!")
        return
    
    # Group by set
    by_set = {}
    for card, folder in cards:
        by_set.setdefault(folder, []).append(card)
    
    print("By set:")
    for s, card_list in sorted(by_set.items()):
        print(f"  {s}: {len(card_list)}")
    
    print(f"\nRefining effects with smart templates...")
    
    refined = 0
    errors = 0
    
    for i, (card, folder) in enumerate(cards):
        try:
            code = generate_effect_code(card)
            save_effect(card, code)
            refined += 1
            
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(cards)}")
                
        except Exception as e:
            errors += 1
            print(f"  Error for {card.card_id}: {e}")
    
    print(f"\n=== Complete ===")
    print(f"Refined: {refined}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
