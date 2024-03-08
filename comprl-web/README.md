# Welcome to COMPRL-Frontend!

This Repository contains the web interface for the [comprl](https://github.com/martius-lab/teamproject-competition-server) server.
This repository eventually will be deleted or moved if we can decide on a fitting location.
## Development

From your terminal:

```sh
npm run dev
```

This starts your app in development mode, rebuilding assets on file changes.

## Deployment

First, build your app for production:

```sh
npm run build
```

Then run the app in production mode:

```sh
npm start
```

Now you'll need to pick a host to deploy it to.

## Config File
The `user_db_path`, the `user_db_name` and the `key` are defined in the config file `config.ts`.
The current key is `1234`.