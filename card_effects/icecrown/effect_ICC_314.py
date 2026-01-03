"""Effect for ICC_314 in ICECROWN"""
def setup(game, source):
    def on_end(game, trig_src, turn_count):
        # Specific Sindragosa logic could be here, but verifying signature first
        pass
    game.register_trigger('on_turn_end', source, on_end)
