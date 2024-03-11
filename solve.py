import sys 
import copy
import time
import argparse
import math
from multiprocessing import Process, Manager


max_depth = 10
vowel_thershold = 3
consonant_threshold = 3 
point_threshold = None
num_threads = 4
puzzle = "abcdefghijklmnopqrstuvwxy"

# Parse input 
parser = argparse.ArgumentParser()

parser.add_argument("--threads", help="Number of threads to creat (Max 25)")
parser.add_argument("--max_length", help="Maximum search depth. Sole determinant of performance")
parser.add_argument("--puzzle", help="String of length 25 representing board")
parser.add_argument("--vocab_size", help ="Size of vocab to search over: small, large, full")
parser.add_argument("--point_threshold", help = "We only will validate a word if it would be worth > (current max point - point_threshold). 0 will only evaluate strictly better words. Default off")

args=parser.parse_args()

vocabs = {
    "small" : "common_8k",
    "medium" : "common_15k",
    "large" : "common_20k",
    "full" : "scrabble_120k"
}
vocab_file = vocabs["large"]
if args.vocab_size and args.vocab_size in vocabs.keys(): vocab_file = vocabs[args.vocab_size]
    

# Get valid words
valid_words = []
with open(f'vocabs/sorted/{vocab_file}_sorted.txt', "r") as f:
    word = f.readline()
    while word: 
        valid_words.append(word.strip('\n'))
        word = f.readline()


# Char to points mapping
char_values = {}
char_values['a'] = 1 
char_values['b'] = 4
char_values['c'] = 5
char_values['d'] = 3
char_values['e'] = 1
char_values['f'] = 5
char_values['g'] = 3
char_values['h'] = 4
char_values['i'] = 1
char_values['j'] = 7
char_values['k'] = 6
char_values['l'] = 3
char_values['m'] = 4
char_values['n'] = 2
char_values['o'] = 1
char_values['p'] = 4
char_values['q'] = 8
char_values['r'] = 2
char_values['s'] = 2
char_values['t'] = 2
char_values['u'] = 4
char_values['v'] = 5
char_values['w'] = 5
char_values['x'] = 7
char_values['y'] = 4
char_values['z'] = 8



def map_list_str_to_2d_list(mat_str) -> list:
    '''
    Accepts a string that represents a list and returns a 2D list of character that represents game board
    '''

    mat_str = mat_str[1:len(mat_str)-1]

    rows = mat_str[1:-1].split('],[')

    # Split each row into elements and strip whitespace
    list_2d_str = [[element.strip() for element in row.split(',')] for row in rows]

    # Add boolean representing validity of word 
    return [[element for element in sublist] for sublist in list_2d_str]
    
def map_str_to_2d_list(str) -> list:
    '''
    Accepts a string of letters and returns a 2D list of character that represents game board
    '''
    list_2d = []
    i = 1
    row = []
    row_counter = 0
    doubleLetter = None

    for char in str:
        # Track doubleLetter 
        if char.isupper(): doubleLetter = (row_counter, ((i-1)%5))
        row.append(char.lower())
        if i%5 == 0:
            list_2d.append(row)
            row = []
            row_counter+=1
        i+=1
    return list_2d, doubleLetter

def get_valid_adjacent(mask, row, col):
    '''
    Take in a row and column and return a list of tuples of indices for valid adjacent letters
    '''
    valid_adjacent = []
    
    for r in range(row - 1, row +2):
        if r >= 0 and r < len(grid):
            for c in range(col-1, col+2):
                if c >=0 and c < len(grid[0]):
                    if mask[r][c] == True:
                        valid_adjacent.append((r,c))
    return valid_adjacent

def get_point_score(str, contains_double_letter):
    '''
    Determine the point score of a word
    '''
    points = 0
    for char in str:
        points += char_values[char]
    if contains_double_letter: points *=2
    if len(str) > 5: points+=10
    return points

vowels = "aeiouy"
def contains_vowel(str): 
    return any(char in vowels for char in str)

consonants = "bcdfghjklmnpqrtsvwxyz"
def contains_consonants(str):
    return any(char in consonants for char in str)


# Create Grid as global var
if (args.max_length):max_depth = int(args.max_length)
if (args.threads): num_threads = int(args.threads)
if (args.puzzle): puzzle = args.puzzle

# Validate input
if len(puzzle) != 25:
    print(f'Error - Input string length is: {len(puzzle)}. It should be 25')
    exit()

grid, doubleLetter = map_str_to_2d_list(puzzle)
starting_bool_mask = [[True for pos in range(len(row))] for row in grid]


def recursive_search(str, mask, sequences, row, col):
    '''
    Starting with a string of 1 character, depth first search 
    all valid sequences in the grid up to a maximum sequence length
    '''
    # If new_depth exceeds max_depth, do not recurse any further
    if len(str) >= max_depth: return

    # Heuristic to restrict search to plausible words: If str is X long and had no vowels, it is probably not a plausbile word
    if (len(str) == vowel_thershold) and not contains_vowel(str): return
    if (len(str) == consonant_threshold) and not contains_consonants(str): return

    sequences.append((str, mask[doubleLetter[0]][doubleLetter[1]] == False if doubleLetter != None else False))

    # Recursively call search with all new char combinations of adjacent chars
    for index in get_valid_adjacent(mask, row, col):
        row, col = index[0],index[1]

        # Char that is currently being explore should be set to invalid
        mask[row][col]= False

        # Call recursive search with new string and new_mask
        recursive_search(str + grid[index[0]][index[1]], mask, sequences, index[0], index[1])

        # Now that we are done exploring this sequence, this char becomes valid
        mask[index[0]][index[1]] = True
        
    return 

def bin_search_valid_words(target):
    start = 0
    end = len(valid_words) - 1
    while start <= end:
        middle = (start + end)// 2
        midpoint = valid_words[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return midpoint

def search_worker(sequences, global_valid, max_points):

    found_words = []
    for seq in sequences:
        points = get_point_score(seq[0], seq[1])
        if ((points >= max_points["max"] - point_threshold ) if point_threshold else True) and len(seq[0]) > 2:
            if bin_search_valid_words(seq[0]):
                found_words.append((seq[0], points))
                if points > max_points["max"]: 
                    print(f'New Max: {seq[0]} - {points} points')
                    max_points["max"] = points
    global_valid+=found_words

if __name__ == '__main__':

    start = time.time()

    # Obtain all possible sequences on baord 
    global_sequences = []

    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            mask = copy.deepcopy(starting_bool_mask)
            mask[row_idx][col_idx] = False
            recursive_search(char, mask, global_sequences, row_idx, col_idx)

    
    with Manager() as manager:
        global_playable = manager.list()
        max_points = manager.dict()
        max_points["max"] = 0

        processes = []

        chunk_size = len(global_sequences) // num_threads

        idx = 0 
        
        for i in range(num_threads):
            search_seq = global_sequences[i * chunk_size: (i+1) * chunk_size if (i+1) * chunk_size < len(global_sequences) else -1]
            processes.append(Process(target = search_worker, args = (search_seq, global_playable, max_points) ))

        for p in processes: 
            p.start()

        # Wait for all starting position to be evaluated
        for p in processes:
            p.join()

        print(f'Elapsed time of: {time.time() - start}s for max depth: {max_depth}')

        # Print playable words in sorted order
        print_words = copy.deepcopy(global_playable)
        print_words.sort(key=lambda tup: tup[1], reverse = True)
        for word in print_words[0:15]:
            print(f'{word[0]} - {word[1]}')
        