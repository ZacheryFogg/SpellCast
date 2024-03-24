## What the program is

Python program to cheat in the Discord Activity SpellCast against Kalvin. Only used to cheat against Kalvin, never in online play 

Program accepts a 25 character string representing a game board, and then searches all possible combination of letters on that board for valid scrabble words up to a specified length

Program will print out each new highest point scoring word as it searches and will print out the top highest scoring words after it terminates 

Program can optionally search for words that are possible if one letter is swapped, although this greatly increases processing time. Program will output top 10 point scoring "Swap words" at end of program termination

Program can account for Double Word bonuses, but not Triple or Double Letter bonues.

Program had a 4 different vocabulary sizes available to search against: 
- All ~120,000 valid scrabble words
- ~20,000 most common English words
- ~15,000 most common English words
- ~8,000 most common English words

Program is optionally multithreaded and can take advantage of as many threads as are available (defaults to 2 threads)

## How to run the program 

`python3 solve.py --max_length=7 --puzzle="abcdefghijklmnopqrstuvwxy"`

#### Arguments: 

- --threads: How many threads to use. No min, no max. Definetly increase if swap checking is enabled. Default 2. 
- --max_length: Max length of possible word to search for. Negatively correlated with performance, especially if swaps are enabled. Default 7.
- --puzzle: the 25 character string that represents the puzzle. Capitalize the letter in the string that represents a Double Word bonus tile
- --vocab_size: Searching over larger vocabularies increasing processing time. Also the using the common English word vocabs will ensure that returned words are believable so that Kalvin does not get suspicious... although he is pretty slow, so he may not notice either way. Possible values: "small" --> 8k vocab, "medium" --> 15k vocab (default), "large" --> 20k vocab, "full" --> 120k all valid scrabble words. 
- --do_swap: Should the program search for possible swap words. Greatly impacts processing time. `--do_swap=1` will enable swap checking, any other value will not.


#### Example usages:

`python3 solve.py --max_length=8 --do_swap=1 --vocab_size="large" --threads=20 --puzzle="aBcdefghijklmnopqrstuvwxy"`
`python3 solve.py --max_length=6 --puzzle="abcdefghijklmnopqrstuvwxy" --threads=1 --vocab_size="full"`

### Only cheat against Kalvin, although, maybe not even him since he has never won a game to begin with. 

