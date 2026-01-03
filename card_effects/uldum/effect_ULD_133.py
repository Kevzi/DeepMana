"""Effect for ULD_133 in ULDUM"""
def setup(game, source):
    def on_end(game, trig_src, turn_count):
        # Desert Hare or similar card logic
        pass
    game.register_trigger('on_turn_end', source, on_end)