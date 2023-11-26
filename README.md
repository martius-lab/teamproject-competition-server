# Willkommen zum Teamprojekt "Competition Server for Reinforcement Agents"!

In diesem Github Repository wird ein großer Teil Eurer Arbeit stattfinden.
Bitte stellt sicher, dass Ihr

>  [Anforderungen im Teamprojekt](COURSE-DESCRIPTION.md)

lest.

## GitHub Tour

- In [Issues](../../issues) könnt Ihr entdeckte Fehler (Bugs), User Stories und andere
  Tickets festhalten, damit ihr nicht vergesst diese zu bearbeiten.

- [Pull Requests](../../pulls) sind spezielle Issues, die dazu verwendet werden, um Code
  Reviews durchzuführen.

- In [Projects](../../projects) könnt Ihr Euch ein Sprint Board anlegen, um die nächste
  Iteration zu planen und Euren Fortschritt nachzuvollziehen. Eine Vorlage kann
  [hier](https://github.com/se-tuebingen/teamprojekt-vorlage/projects/1) gefunden
  werden.

- Das [Wiki](../../wiki)  kann genutzt werden, um zum Beispiel weitere inhaltliche
  Anforderungen zu erfassen, die Definition-of-Done zu dokumentieren oder Protokolle und
  Entscheidungen des Teams festzuhalten.

- [Actions](../../actions) erlauben Euch Continuous Integration (CI) und automatisiertes
  Testen für jeden Pull Request und jedes Release einzurichten.

# General
  To run the server use:
  ```
  python -m teamprojekt_competition_server.server.main
  ```
  To run the client use:
  ```
  python -m teamprojekt_competition_server.client.main
  ```

  ## Naming-Conventions
  This project follows the [Google-Styleguide](https://google.github.io/styleguide/)

  ## External-Librarys
  - [Twisted](https://twisted.org): We are using th AMP-Protocol 
    - [docs1](https://amp-protocol.net/), [docs2](https://twisted.org/documents/13.1.0/api/twisted.protocols.amp.html), 
    - [Developer Guide](https://docs.twisted.org/en/twisted-18.4.0/core/howto/amp.html)
    - [API Documentation](https://docs.twisted.org/en/twisted-18.4.0/core/howto/amp.html)
    - [AMP Exampels](https://docs.twisted.org/en/twisted-18.4.0/core/examples/index.html#amp-server-client-variants)
  - [Gymnasium](https://gymnasium.farama.org) (maybe?)

 