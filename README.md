Pycards 0.5
============

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
- [Licence](#licence)
- [Chancelog](#changelog)

## Pycards[↑][top]
### Introduction[↑][top]
*pycards* is an engine with different frontends to memorize things using
[flashcards][1]. *pycards* is written in [Python 3][2] and uses a [sqlite][3]
database to store all the data. It is starting to get a little usable.

### Requirements[↑][top]
- [Python 3][2]

### Todo[↑][top]
- Web interface
- Curses interface
- Graphical user interface

### Troubleshooting[↑][top]
If the program misbehaves at a certain point please make sure before posting an
issue that you run it with [Python 3][2].

## Documentation[↑][top]
### Leitner system[↑][top]
The [Leitner-system][4] is a system of repeating flashcards and works with
boxes. Our implementation has 5 boxes. Cards go up a box if you answer them
correct and go down in box when you answer them incorrect. A card can not go
lower then box 1 nor can it go higher then box 5.

Cards in box 1 are asked every session, cards in box 2 are asked every other
session, cards in box 3 are asked once every 3 sessions, cards in box 4 are
asked once in every 4 sessions and cards in box 5 are never asked again.

### Usage of `cli.py`[↑][top]
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
	
		Use the [leitner-system][4].
	- `-r`, `--random`
	
		Randomize the questions.
	- `-i`, `--inverse`
	
		Inverse the question and the answer.
	- `deckname`
	
		Name of the deck to start the session with

## Licence[↑][top]
See `LICENCE` file.

## Changelog[↑][top]
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
