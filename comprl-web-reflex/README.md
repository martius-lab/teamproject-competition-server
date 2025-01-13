CompRL Web Interface with Reflex
================================

comprl-web-reflex is a re-implementation of the original web interface that was
done with Node.js.  It uses [reflex](reflex.dev), a Python framework for
building web applications.  The benefit of using Python is that it directly use
components of the comprl package (e.g.  for database access), thus reducing the
need for redundant code.  Further, it is easier to maintain as everything is
done with one language (Python).


## Features

- User registration
- Users statistics (number of played games, etc.)
- Leaderboard


## Requirements

To install the requirements (best do this in a virtual environment):
```
pip install ../comprl
pip install -r requirements.txt
```

The web interface needs an additional database table to manage login sessions.
To add it to an existing comprl database, run the following command:
```
python3 ./create_database_tables.py path/to/comprl/database.db
```


## Run

The path to the comprl config file needs to be specified via an environment
variable:
```
# Path to the database
export COMPRL_CONFIG_PATH="/path/to/comprl/config.toml"

reflex run
```

## Run with Apptainer

Build the Apptainer image:
```
apptainer build comprl-web-reflex.sif ./comprl-web-reflex.def
```

For running, you'll need to use a writable overlay (as Reflex will do some
installation and building stuff when being run).  The example below simply uses
an overlay directory.  It might be better to use an overlay image in some
cases, please refer to the Apptainer documentation.
```
sudo apptainer run -ec --overlay /tmp/overlay \
    --bind /path/to/your/comprl-database:/comprl-config \
    --env API_URL=http://your-server.de \
    comprl-web-reflex.sif
```

In the example above, `/path/to/your/comprl-database` is expected to be a
directory on the host system, that contains the comprl config file.  It is
expected to be called "config.toml".  You can set a different name by adding the
following argument: ```
--env COMPRL_CONFIG_PATH=/comprl-config/my_config.toml
```

Note from the [Reflex container example, which was used as a base for
this](https://github.com/reflex-dev/reflex/tree/main/docker-example/simple-two-port):

> This container should be used with an existing load balancer or reverse proxy
> to route traffic to the appropriate port inside the container.
>
> For example, the following Caddyfile can be used to terminate TLS and forward
> traffic to the frontend and backend from outside the container.
>
>     my-domain.com
>
>     encode gzip
>
>     @backend_routes path /_event/* /ping /_upload /_upload/*
>     handle @backend_routes {
>         reverse_proxy localhost:8000
>     }
>
>     reverse_proxy localhost:3000
