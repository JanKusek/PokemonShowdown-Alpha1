import asyncio
from poke_env.player import RandomPlayer


async def main():
    player_1 = RandomPlayer(
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