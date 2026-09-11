import asyncio

from poke_env.player import RandomPlayer # type: ignore
from poke_env.player import Player # type: ignore


class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)


async def main():
    player_1 = RandomPlayer(max_concurrent_battles=1)
    player_2 = MaxDamagePlayer(max_concurrent_battles=1)

    for i in range(0,100):
        await player_1.battle_against(player_2, n_battles=1)

    print(f"Finished battles: {player_1.n_finished_battles}")
    print(f"Player 1 wins: {player_1.n_won_battles}")


if __name__ == "__main__":
    asyncio.run(main())
