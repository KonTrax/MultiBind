# MultiBind (sublime text plugin)

This is currently only a prototype written without ever having used python before this point. Will keep adding to it as my requirements expand and is very much a work in progress.

## Usage

Toggle:

	{"keys":["whatever"], "command":"multibind_toggle", "args":{ "layout": "BARRIERNAME" }}

Barrier:

	... "context": [{"key":"multibind.BARRIERNAME"}] ...

## Usage Example
	// Toggle "wasd" layout
	{ "keys": ["alt+\\"],
		"command": "multibind_toggle",
		"args"   : { "layout": "wasd" }
	},

	// Show current layout in statusbar
	{ "keys": ["ctrl+shift+\\"],
		"command": "multibind_show",
		"args"   : {  }
	},

	// Bind [wasd] keys as normal
	// and add multibind layout context
	{ "keys": ["a"],
		"command": "move",
		"args"   : {"by": "characters", "forward": false},
		"context": [
		{	"key": "multibind.wasd" }
	]},
	{ "keys": ["d"],
		"command": "move",
		"args"   : {"by": "characters", "forward": true},
		"context": [
		{	"key": "multibind.wasd" }
	]},
	{ "keys": ["w"],
		"command": "move",
		"args"   : {"by": "lines", "forward": false},
		"context": [
		{	"key": "multibind.wasd" }
	]},
	{ "keys": ["s"],
		"command": "move",
		"args"   : {"by": "lines", "forward": true},
		"context": [
		{	"key": "multibind.wasd" }
	]},

## Installation

[to come]

## License

[to come]