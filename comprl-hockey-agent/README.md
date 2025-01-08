RL Competition Hockey Agent
===========================

This package contains a simple example implementation for a client of the comprl hockey
game.  It wraps an agent from the `hockey` package and implements a `main()` function to
run it as a client that connects to the comprl server.

To run the example agent, you first need to install the package:
```
# call from the "comprl-hockey-agent" root directory
pip install .
```

This installs an exectuable `comprl-hockey-agent` which executes the `main()` function
which is implemented in `src/comprl_hockey_agent/__init__.py`.  It expects some
arguments for the server connection and the agent configuration.  For example to run the
strong version of the agent:
```
comprl-hockey-agent --server-url <URL> --server-port <PORT> \
    --token <YOUR ACCESS TOKEN> \
    --args --agent=strong
```

The server information can also be provided via environment variables, then they don't
need to be provided via the command line:
```
# put this in your .bashrc or some other file that is sourced before running the agent
export COMPRL_SERVER_URL=<URL>
export COMPRL_SERVER_PORT=<PORT>
export COMPRL_ACCESS_TOKEN=<YOUR ACCESS TOKEN>
```
Then just call
```
comprl-hockey-agent --args --agent=strong
```
