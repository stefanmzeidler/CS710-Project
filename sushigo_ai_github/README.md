
Toy python project for testing AI for the Sushi Go card game

To install requirements:
`pip3 install pydantic pandas pygame`

```
usage: sushi_arena.py [-h] -p
                      {rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui}
                      [{rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui} ...]
                      [-n N] [-r R] [-v] [-b]

Run a series of games between a set of AIs

optional arguments:
  -h, --help            show this help message and exit
  -p {rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui} [{rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui} ...], --players {rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui} [{rand1,rand2,pref1_pudding,pref1_wasabi,pref1_tempura,pref1_dumpling,pref1_maki3,minmax1,human_cli,human_gui} ...]
                        <Requires 2-5> AI types for players
  -n N                  Number of games to run
  -r R                  Set random seed
  -v                    Print output of each round
  -b                    Save each turn action for playback
```

To view the output of the `-b` option:

```
usage: playback_viewer.py [-h] play_file

View turns from a game playback JSON file

positional arguments:
  play_file   The file to open

optional arguments:
  -h, --help  show this help message and exit
```

# Reference
  * Game Site: https://gamewright.com/product/Sushi-Go
  * Game Rules: https://gamewright.com/pdfs/Rules/SushiGoTM-RULES.pdf

# Todo
  * Refactor to share code for human_gui and replay viewer
  * Check imports to make pygame optional
  * Add maki logic to minmax1 AI, chopsticks?, test to make sure it works
  * Add support for chopsticks in human GUI, other improvements
  * Add some smarter AIs
  * Add series of AIs with simple hierarchy of preffered cards
  * Better way to store stats to aggregate accross runs
  * Logging, and documentation
  * Think about not rotating the state for each AI and instead passing in an index
  * Organize into python package with dependancies, setup, subfolders and way of importing external AI's
