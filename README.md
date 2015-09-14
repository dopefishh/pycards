`pycards` 0.5
===========
## Table of Contents
- [Table of contents](#table-of-contents)
- [Pycards](#pycards)
	- [Introduction](#introduction)
	- [Requirements](#requirements)
	- [Todo](#todo)
	- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
	- [Leitner system](#leitner-system)
	- [Usage `cli.py`](#usage-of-clipy)
	- [Usage `web.py`](#usage-of-webpy)
- [Licence](#licence)
- [Chancelog](#changelog)

## Pycards [↑][top][top][↑]
### Introduction<a href="#table-of-contents">↑</a>
*pycards* is an engine with different frontends to memorize things using
[flashcards][1]. *pycards* is written in [Python 3][2] and uses a [sqlite][3]
database to store all the data. It is starting to get a little usable.

### Requirements<a href="#table-of-contents">↑</a>
- [Python 3][2]

### Todo<a href="#table-of-contents">↑</a>
- Web interface
- Curses interface
- Graphical user interface

### Troubleshooting<a href="#table-of-contents">↑</a>
If the program misbehaves at a certain point please make sure before posting an
issue that you run it with [Python 3][2].

## Documentation<a href="#table-of-contents">↑</a>
### Leitner system<a href="#table-of-contents">↑</a>
TODO

### Usage of `cli.py`<a href="#table-of-contents">↑</a>
`cli.py [globaloptions] {list,load,remove,export,session} [options] [args]`

- `globaloptions`
	- `-h`, `--help`
	
		Show the help message and exit.
	- `-d DATABASE`, `--database DATABASE`
	
		Specify a custom database file. If not given `~/.pycards/pycards.db` is
		used.
	- `-l {INFO,DEBUG,SILENT}`, `--loglevel {INFO,DEBUG,SILENT}`
	
	  Specify a custom log level. If not given `SILENT` is used.
	- `-f LOGFILE`, `--logfile LOGFILE`
	
	  Specify a log file location. If not given stdout is used.
	- `--version`
	
		Show version number and exit
- `list`: `cli.py [globaloptions] list [options] [deckname [deckname ...]]`

	Show one or more decks from the database.
	- `-h`, `--help`
	
		Show the `list` specific help message and exit.
	- `-e`, `--show-entries`
	
		Flag to print all the individual entries
	
	- `deckname`
	
		Name of the deck to print. If not given, all decks will be printed.
- `load`:  `cli.py [globaloptions] load [options] deckname [filepath]`

	Load a deck from a file into a database. The input must be tab separated and
	two columns. The first column is the question and the second column is the
	answer.
	- `-h`, `--help`
	
		Show the `load` specific help message and exit.
	- `deckname`
	
		Name of the deck to load the entries in.
	- `filepath`
	
		Location to load the entries from. If not given stdin is used
- `remove`: `cli.py [globaloptions] remove [options] deckname [deckname ...]`

	Remove decks from the database.
	- `-h`, `--help`
	
		Show the `remove` specific help message and exit.
	- `deckname`
	
		Name of the deck to remove.
- `export`:  `cli.py [globaloptions] export [options] deckname [deckname ...]`

	Export decks from the database.
	- `-h`, `--help`
	
		Show the `export` specific help message and exit.
	- `-f`, `--filepath`
	
		Location to export to. If not given stdout is used
	- `deckname`
	
		Name of the deck to export.
- `session`: `cli.py [globaloptions] session [options] deckname`

	Run a session with a deck.
	- `-h`, `--help`
	
		Show the `session` specific help message and exit.
	- `-l`, `--leitner`
	
		Use the [leitner system][4].
	- `-r`, `--random`
	
		Randomize the questions.
	- `-i`, `--inverse`
	
		Inverse the question and the answer.
	- `deckname`
	
		Name of the deck to start the session with

### Usage of `web.py`<a href="#table-of-contents">↑</a>
NOT IMPLEMENTED YET

## Licence<a href="#table-of-contents">↑</a>
See `LICENCE` file.

## Changelog<a href="#table-of-contents">↑</a>
*[Version 0.5](https://github.com/dopefishh/pycards/releases/tag/v0.5)*
- Added statistics table.
- CRTL+C will interrupt but will write statistics first.

*[Version 0.4](https://github.com/dopefishh/pycards/releases/tag/v0.4)*
- Better command line parser, parser separated from main.
- List, export and remove accept multiple decknames now.
- Better error handling for malformed input files.
- Fancy menu in `README.md`

*[Version 0.3](https://github.com/dopefishh/pycards/releases/tag/v0.3)*
- [Leitner][4] system implemented.
- Changed systems so that the system is with flags instead of names. In this
  way one can do random-leitner-inverse for example.
- All queries parameterized where possible, also changed deck databases to be
  consisting of ids and ascii only to let names contain every character.
- Updated readme with help.
- Removed the need for a config file.
- Better time representation in `cli.py` while listing decks.

*[Version 0.2](https://github.com/dopefishh/pycards/releases/tag/v0.2)*
- List deck(s) either with or without all the entries.
- Remove a deck.
- Export to a file.
- Load a deck from tab separated files with two columns.
- Play a session with a deck and different systems: ordered, random.

*[Version 0.1](https://github.com/dopefishh/pycards/releases/tag/v0.1)*
- Initial version

[1]: https://en.wikipedia.org/wiki/Flashcard
[2]: https://www.python.org
[3]: https://www.sqlite.org
[4]: https://en.wikipedia.org/wiki/Leitner_system
[top]: #table-of-contents
