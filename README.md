# pycards 0.3

### Introduction
*pycards* is an engine with different frontends to memorize things using
[flashcards][1]. *pycards* is written in [Python 3][2] and uses a [sqlite][3]
database to store all the data. It is starting to get a little usable.

### Systems
Users have various ways to change the way the questions are asked. This is done
through three boolean flags:

- `-l`, `--leitner`
	
	leitner
- `-r`, `--random`
	
	random
- `-i`, `--inverse`

	inverse

### TODO, in order of importance
- Web interface
- Curses interface
- Graphical user interface

### Changelog
*[Version 0.3](https://github.com/dopefishh/pycards/releases/tag/v0.3)*
- [Leitner][4] system implemented.
- Changed systems so that the system is with flags instead of names. In this
  way one can do random-leitner-inverse for example.
- All queries parameterized where possible, also changed deck databases to be
  consisting of ids and ascii only to let names contain every character.

*[Version 0.2](https://github.com/dopefishh/pycards/releases/tag/v0.2)*
- List deck(s) either with or without all the entries.
- Remove a deck.
- Export to a file.
- Load a deck from tab separated files with two columns.
- Play a session with a deck and different systems: ordered, random.

*[Version 0.1](https://github.com/dopefishh/pycards/releases/tag/v0.1)*
- Initial version

### LICENCE
See `LICENCE` file.

[1]: https://en.wikipedia.org/wiki/Flashcard
[2]: https://www.python.org
[3]: https://www.sqlite.org
[4]: https://en.wikipedia.org/wiki/Leitner_system
