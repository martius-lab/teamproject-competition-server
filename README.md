# COMPRL

## Description
**COMPRL** is a versatile Python package designed for hosting game-like competitions among multiple remote clients. It's designed for easy and fast integration of new game types.

## Table of Contents

- [Getting Started](#getting-started)
- [Examples](#examples)


## Getting Started

### Server

To host your competition, implement a new game by inheriting from the `IGame` class provided by the `comprl.server.interfaces` module. Once your game is fully implemented, use a configuration file or command-line arguments to start the server with the desired configuration.

```sh
#display all possible command line arguments
python -m comprl.server --h

#run server by providing a config file
python -m comprl.server --config="path/to/config.toml"
```

### Client

For implementing a new client, utilize the `comprl.client` package. Here, you can directly instantiate an `Agent` object or inherit from it. The only required implementation is the `get_step()` function, which is called with the corresponding action. Additionally, override other functions to receive and handle data about games being played or handle any errors that may occur. The flexibility provided by COMPRL allows you to tailor the client to your specific needs.

## Examples

### Simple

This is a very simple game which checks is the sum of all received actions is greater than 10, if so the game ends.
