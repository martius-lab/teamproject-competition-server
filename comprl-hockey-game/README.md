CompRL Hockey Game
==================

Implementation of the Hockey game for the comprl server.

## Requirements

Before running, install the requirements:
```
pip install -r requirements.txt
```

And initialise the database:
```
python3 -m comprl.scripts.create_database ./config.toml
```


## Run the server

Call from this directory (otherwise relative paths in the config will not be resolved
correctly):
```
python3 -m comprl.server --config ./config.toml
```
