# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- BREAKING: Removed option to use separate databases for user and game tables.
- BREAKING: Removed option to configure database table names.
- BREAKING: Database is not automatically created anymore.  Use
  `comprl.scripts.create_database`.
- BREAKING: New config option `data_dir` to specify output directory for game actions.
  This is a required setting (no default value), hence a breaking change.

## Added
- Script `list_games` to list all games from the database on the terminal.


## [0.1.0]

This is the final version of the University team project.

---
[Unreleased]: https://github.com/martius-lab/teamproject-competition-server/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/martius-lab/teamproject-competition-server/releases/tag/v0.1.0
