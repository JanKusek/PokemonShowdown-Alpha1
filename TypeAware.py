import asyncio
from poke_env.data import GenData
from poke_env.player import Player, RandomPlayer


class TypeAwarePlayer(Player):

    def _boost_multiplier(self, stage):
        if stage >= 0:
            return (2 + stage) / 2
        return 2 / (2 - stage)

    def choose_move(self, battle):
        if not battle.available_moves:
            return self.choose_random_move(battle)

        gen_data = GenData.from_gen(9)
        type_chart = gen_data.type_chart

        attacker = battle.active_pokemon
        defender = battle.opponent_active_pokemon

        best_move = None
        best_score = -1

        for move in battle.available_moves:
            if move.base_power == 0:
                continue

            multiplier = move.type.damage_multiplier(
                defender.type_1,
                defender.type_2,
                type_chart=type_chart,
            )
            if multiplier == 0:
                continue  # immune -- never worth picking over a damaging move

            # STAB
            stab = 1.5 if move.type in attacker.types else 1.0

            if move.category.name == "PHYSICAL":
                atk_stat = attacker.stats.get("atk") or attacker.base_stats["atk"]
                atk_stat *= self._boost_multiplier(attacker.boosts.get("atk", 0))
                def_stat = defender.base_stats["def"]
                def_stat *= self._boost_multiplier(defender.boosts.get("def", 0))
            else:  # SPECIAL
                atk_stat = attacker.stats.get("spa") or attacker.base_stats["spa"]
                atk_stat *= self._boost_multiplier(attacker.boosts.get("spa", 0))
                def_stat = defender.base_stats["spd"]
                def_stat *= self._boost_multiplier(defender.boosts.get("spd", 0))

            stat_ratio = atk_stat / max(def_stat, 1)

            accuracy = 1.0 if move.accuracy is True else float(move.accuracy)

            expected_damage = (
                move.base_power * multiplier * stab * stat_ratio * accuracy
            )

            if expected_damage > best_score:
                best_score = expected_damage
                best_move = move

        if best_move is not None:
            return self.create_order(best_move)

        return self.choose_random_move(battle)


async def main():
    player_1 = TypeAwarePlayer(
        battle_format="gen9randombattle",
    )
    player_2 = RandomPlayer(
        battle_format="gen9randombattle",
    )

    await player_1.battle_against(player_2, n_battles=5)

    print(f"Player 1 won {player_1.n_won_battles} / {player_1.n_finished_battles} battles")
    print(f"Player 2 won {player_2.n_won_battles} / {player_2.n_finished_battles} battles")


if __name__ == "__main__":
    asyncio.run(main())