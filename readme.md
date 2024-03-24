## What the program is

Python program to cheat in the Discord Activity SpellCast against Kalvin. Only use to cheat against Kalvin, never in online play 

Program accepts a 25 character string representing a game board, and then searches all possible combination of letters on that board for valid scrabble words up to a specified length

Program will print out each new highest point scoring word as it searches and will print out the top highest scoring words after it terminates 

Program can optionally search for words that are possible if one letter is swapped, although this greatly increases processing time. Program will output top 10 point scoring "Swap words" at end of program termination

Program can account for Double Word bonuses, but not Triple or Double Letter bonues, or gems.

Program had a 4 different vocabulary sizes available to search against: 
- All ~120,000 valid scrabble words
- ~20,000 most common English words
- ~15,000 most common English words
- ~8,000 most common English words

Program is optionally multithreaded and can take advantage of as many threads as are available (defaults to 2 threads)

Program also outputs the (row,col) path on the board that comprises the outputed words
## How to run the program 

`python3 solve.py --max_length=7 --puzzle="abcdefghijklmnopqrstuvwxy"`

Enter the letters on the board as you would read a book. Left to right, top to bottom:
[Row 1, Col 1], [Row 1, Col 2] ,..., [Row 1, Col 5] , [Row 2, Col 1] ,..., [Row 5, Col 4] , [Row 5, Col 5].

For example, the below board would be entered as such (notice the capitalized letter corresponding to the Double Word bonus): `--puzzle="enreirryurrelmoglythtHtni"` 

![SpellCast Board](/assets/SpellCast_Board.PNG)

### Arguments: 

- --threads: How many threads to use. No min, no max. Definetly increase if swap checking is enabled. Default 2. 
- --max_length: Max length of possible word to search for. Negatively correlated with performance, especially if swaps are enabled. Default 7.
- --puzzle: the 25 character string that represents the puzzle. Capitalize the letter in the string that represents a Double Word bonus tile
- --vocab_size: Searching over larger vocabularies increasing processing time. Also the using the common English word vocabs will ensure that returned words are believable so that Kalvin does not get suspicious... although he is pretty slow, so he may not notice either way. Possible values: "small" --> 8k vocab, "medium" --> 15k vocab, "large" --> 20k vocab (default), "full" --> 120k all valid scrabble words. 
- --do_swap: Should the program search for possible swap words. Greatly impacts processing time. `--do_swap=1` will enable swap checking, any other value will not.


### Example usages:

- `python3 solve.py --max_length=8 --do_swap=1 --vocab_size="large" --threads=20 --puzzle="aBcdefghijklmnopqrstuvwxy"`
- `python3 solve.py --max_length=6 --puzzle="abcdefghijklmnopqrstuvwxy" --threads=1 --vocab_size="full"`


## Example output: 

```
$ python3 solve.py --puzzle="enreirryurrelmoglythtHtni" --threads=12 --do_swap=1 --max_length=7
New Max: rye - 7 points
New Max: rule - 10 points
New Max: ruler - 12 points
New Max: rumor - 13 points
New Max: muller - 27 points
New Max: myth - 28 points
---------------------------------------
Elapsed time of: 2.589602470397949s for max depth: 7
---------------------------------------

--------------------
Top 10 Scoring Words
--------------------

----        ------       ----
Word        Points       Path
----        ------       ----

myth          28         (3,4) --> (4, 3) --> (5, 3) --> (5, 2)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (2, 1)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (2, 2)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (3, 1)
motley        25         (3,4) --> (3, 5) --> (4, 4) --> (3, 3) --> (3, 2) --> (2, 3)
motley        25         (3,4) --> (3, 5) --> (4, 4) --> (3, 3) --> (3, 2) --> (4, 3)
thy           20         (5,1) --> (5, 2) --> (4, 3)
thy           20         (5,3) --> (5, 2) --> (4, 3)
multi         14         (3,4) --> (2, 4) --> (3, 3) --> (4, 4) --> (5, 5)
myth          14         (3,4) --> (4, 3) --> (4, 4) --> (4, 5)

---------------------------------------
Words that require a character swapped
---------------------------------------

----------               ------  ---------           ----
Swap Words               Points  Char Swap           Path
----------               ------  ---------           ----

ghythm --> rhythm        50      swap g for r        (4,1) --> (5, 2) --> (4, 3) --> (4, 4) --> (4, 5) --> (3, 4)
lhythm --> rhythm        50      swap l for r        (4,2) --> (5, 2) --> (4, 3) --> (4, 4) --> (4, 5) --> (3, 4)
thythm --> rhythm        50      swap t for r        (5,1) --> (5, 2) --> (4, 3) --> (4, 4) --> (4, 5) --> (3, 4)
thythm --> rhythm        50      swap t for r        (5,3) --> (5, 2) --> (4, 3) --> (4, 4) --> (4, 5) --> (3, 4)
myhtle --> myrtle        42      swap h for r        (3,4) --> (4, 3) --> (5, 2) --> (5, 1) --> (4, 2) --> (3, 2)
myhtle --> myrtle        42      swap h for r        (3,4) --> (4, 3) --> (5, 2) --> (5, 3) --> (4, 2) --> (3, 2)
elghty --> eighty        40      swap l for i        (3,2) --> (4, 2) --> (4, 1) --> (5, 2) --> (5, 3) --> (4, 3)
mullh --> mulch          40      swap l for c        (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (5, 2)
mulyh --> mulch          40      swap y for c        (3,4) --> (2, 4) --> (3, 3) --> (4, 3) --> (5, 2)
lymyh --> lymph          38      swap y for p        (3,3) --> (2, 3) --> (3, 4) --> (4, 3) --> (5, 2)
```


```
$ python3 solve.py --puzzle="enreirryurrelmoglythtHtni" --threads=1 --do_swap=0 --max_length=8
New Max: err - 5 points
New Max: rye - 7 points
New Max: rule - 10 points
New Max: ruler - 12 points
New Max: rumor - 13 points
New Max: muller - 27 points
New Max: myth - 28 points
---------------------------------------
Elapsed time of: 1.4854660034179688s for max depth: 8
---------------------------------------

--------------------
Top 10 Scoring Words
--------------------

----        ------       ----
Word        Points       Path
----        ------       ----

myth          28         (3,4) --> (4, 3) --> (5, 3) --> (5, 2)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (2, 1)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (2, 2)
muller        27         (3,4) --> (2, 4) --> (3, 3) --> (4, 2) --> (3, 2) --> (3, 1)
motley        25         (3,4) --> (3, 5) --> (4, 4) --> (3, 3) --> (3, 2) --> (2, 3)
motley        25         (3,4) --> (3, 5) --> (4, 4) --> (3, 3) --> (3, 2) --> (4, 3)
thy           20         (5,1) --> (5, 2) --> (4, 3)
thy           20         (5,3) --> (5, 2) --> (4, 3)
multi         14         (3,4) --> (2, 4) --> (3, 3) --> (4, 4) --> (5, 5)
myth          14         (3,4) --> (4, 3) --> (4, 4) --> (4, 5)

---------------------------------------
```

## Runtime

Program runs relatively quickly, especially if swapping is not enabled.

On Ryzen 7900x (12 core / 24 threads), vobab_size = large:

- 1 thread, no swap, max_length=8: 1.4 seconds 
- 6 threads, swap, max_length=7: 2.5 seconds
- 12 threads, swap, max_length=8: 8.4 seconds




## Only cheat against Kalvin, although, maybe not even him since he has never won a game to begin with. 


