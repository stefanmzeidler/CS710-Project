
Toy python project for testing AI for the Sushi Go card game

```
usage: sushi_arena.py [-h] -p {rand1,rand2} [{rand1,rand2} ...] [-n N] [-r R]                      [-v]
Run a series of games between a set of AIs

optional arguments:
  -h, --help            show this help message and exit
  -p {rand1,rand2} [{rand1,rand2} ...], --players {rand1,rand2} [{rand1,rand2} ...]
                        <Requires 2-5> AI types for players
  -n N                  Number of games to run
  -r R                  Set random seed
  -v                    Print output of each round
```

# Reference
  * Game Site: https://gamewright.com/product/Sushi-Go
  * Game Rules: https://gamewright.com/pdfs/Rules/SushiGoTM-RULES.pdf

# Todo
  * Add maki logic to minmax1 AI, chopsticks?, test to make sure it works
  * Add some smarter AIs
  * Add series of AIs with simple hierarchy of preffered cards
  * Better way to store stats to aggregate accross runs
  * Logging, and documentation
  * Think about not rotating the state for each AI and instead passing in an index
  * Organize into python package with dependancies, setup, subfolders and way of importing external AI's
  * Add API to allow GUI for human players, or non-python AIs
