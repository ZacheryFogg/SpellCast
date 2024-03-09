import sys 
import copy
import time
from multiprocessing import Process, Manager


max_depth = 5
vowel_thershold = 3
consonant_threshold = 3 

# Get valid words
valid_words = []
with open("scrabble_words.txt", "r") as f:
    word = f.readline()
    i = 0
    while word: 
        i+=1
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

def get_point_score(str, mask):
    '''
    Determine the point score of a word
    '''
    points = 0
    for char in str:
        points += char_values[char]
    if doubleLetter != None and mask[doubleLetter[0]][doubleLetter[1]] == False: points *=2
    if len(str) > 5: points+=10
    return points

vowels = "aeiouy"
def contains_vowel(str): 
    return any(char in vowels for char in str)

consonants = "bcdfghjklmnpqrtsvwxyz"
def contains_consonants(str):
    return any(char in consonants for char in str)


# Create Grid as global var
mat_str = sys.argv[1]
grid, doubleLetter = map_str_to_2d_list(mat_str)


def recursive_search(str, mask, found_words, row, col, max_points):
    '''
    Starting with a string of 1 character, depth first search 
    all valid sequences in the grid up to a maximum sequence length
    '''

    # If current word is a valid scrabble word, add to accumulated list, along with point score
    if str in valid_words and len(str) > 2:
        # if len(str) > 4: print(str, handler.get_point_score(str, mask))
        points = get_point_score(str, mask)
        found_words.append((str, points))
        
        if points > max_points["max"]: 
            print(f'New Max: {str} - {points} points')
            max_points["max"] = points

    # If new_depth exceeds max_depth, do not recurse any further
    if len(str) >= max_depth: return

    # Heuristic to restrict search to plausible words: If str is X long and had no vowels, it is probably not a plausbile word
    if (len(str) == vowel_thershold) and not contains_vowel(str): return
    if (len(str) == consonant_threshold) and not contains_consonants(str): return

    # Recursively call search with all new char combinations of adjacent chars
    for index in get_valid_adjacent(mask, row, col):
        row, col = index[0],index[1]

        # Char that is currently being explore should be set to invalid
        mask[row][col]= False

        # Call recursive search with new string and new_mask
        recursive_search(str + grid[index[0]][index[1]], mask, found_words, index[0], index[1], max_points)

        # Now that we are done exploring this sequence, this char becomes valid
        mask[index[0]][index[1]] = True
        
    return 

def worker(char, mask, row, col, results, max_points):
    ''' 
    Worker for each thread to execute
    '''
    found_words = []
    recursive_search(char, mask, found_words, row, col, max_points)
    results.append(found_words) 

if __name__ == '__main__':

    starting_bool_mask = [[True for pos in range(len(row))] for row in grid]

    processes = []

    with Manager() as manager:
        results = manager.list()
        max_points = manager.dict() # make a dict so all threads can alter
        max_points["max"] = 0

        # Create search processes, one for each starting character
        for row_idx, row in enumerate(grid):
            for col, char in enumerate(row):
                new_mask = copy.deepcopy(starting_bool_mask)
                # Make starting letter invalid
                new_mask[row_idx][col] = False
                process = Process(target=worker, args=(char, new_mask, row_idx, col, results, max_points))
                processes.append(process)

        start = time.time()

        # Start Processes
        for p in processes: 
            p.start()

        # Wait for all starting position to be evaluated
        for p in processes:
            p.join()

        print(f'Elapsed time of: {time.time() - start}s for max depth: {max_depth}')
        
        # Compile results
        playable_words = []

        for result in results:
            playable_words += result

    # Print playable words in sorted order
    playable_words.sort(key=lambda tup: tup[1], reverse = True)
    print_words = playable_words[0:10]
    for word in print_words:
        print(word)