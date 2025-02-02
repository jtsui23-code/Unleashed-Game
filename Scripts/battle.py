class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.won = False
        self.battle_state = "player_turn"  # Track whose turn it is
        self.player_move = None
        self.enemy_move = None
        self.turn_complete = False

    def guard(self, entity):
        print(f"{entity.name} guarded!")
        return True

    def GameOver(self):
        print("Game Over!")
        return True

    def process_turn(self, pmov):
        # Handle player turn
        if self.battle_state == "player_turn":
            if self.player_move is None:
                return 1  # Still waiting for player input
            
            # Process player move
            # pmov = self.player_move
            if callable(pmov):
                pmov = pmov()
            
            if pmov == 0:
                self.guard(self.player)
            else:
                # Process player attack
                if self.enemy.TakeDmg(pmov) == 0:
                    self.won = True
                    return 0  # Battle is over
            
            # Switch to enemy turn
            self.battle_state = "enemy_turn"
            self.player_move = None
            return 1

        # Handle enemy turn
        elif self.battle_state == "enemy_turn":
            # Get enemy move
            emov = self.enemy.TakeTurn()
            
            if emov is None:
                emov = 0
            
            if callable(emov):
                emov = emov()

            if emov == 0:
                self.guard(self.enemy)
            else:
                # Process enemy attack
                if self.player.TakeDmg(emov) == 0:
                    self.GameOver()
                    return 0  # Battle is over

            # Reduce cooldowns
            for skill in self.player.Skills:
                skill.reduceCD()
            for skill in self.enemy.Skills:
                skill.reduceCD()

            # Switch back to player turn
            self.battle_state = "player_turn"
            return 1

    def fight(self, pmov):
        return self.process_turn(pmov)

    def set_player_move(self, move):
        """Set the player's chosen move"""
        self.player_move = move