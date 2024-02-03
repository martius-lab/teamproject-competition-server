from comprl.client import Agent

bob = Agent()


@bob.event
def get_step(obv: list[float]):
    return [float(input("enter action: "))]


bob.run(["HelloWorld", "HelloMoon"][int(input("enter agent: "))])
