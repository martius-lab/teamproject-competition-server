import random
import logging as log

from comprl.client import Agent

log.basicConfig(level=log.DEBUG)
bob = Agent()


@bob.event
def get_step(obv: list[float]):
    return [float(random.randint(0, 3))]


@bob.event
def on_start_game(game_id: int):
    print("game started")


@bob.event
def on_end_game(result, stats):
    print("game ended")


bob.run(["HelloWorld", "HelloMoon"][int(input("enter agent: "))])
