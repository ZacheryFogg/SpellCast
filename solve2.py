import sys 
import copy
import time
from multiprocessing import Process, Manager


max_depth = 6

# Get valid words
valid_words = []
with open("scrabble_words.txt", "r") as f:
    word = f.readline()
    i = 0
    while word: 
        i+=1
        valid_words.append(word.strip('\n'))
        word = f.readline()

class GridHandler:
    '''
    GridHandler provides helper functions for Grid objects 
    
    '''
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


    def map_str_to_2d_list(self, mat_str) -> list:
        '''
        Accepts a string that represents a list and returns a 2D list
        '''

        mat_str = mat_str[1:len(mat_str)-1]

        rows = mat_str[1:-1].split('],[')
    
        # Split each row into elements and strip whitespace
        list_2d_str = [[element.strip() for element in row.split(',')] for row in rows]

        # Add boolean representing validity of word 
        return [[element for element in sublist] for sublist in list_2d_str]

    def get_valid_adjacent(self, mask, row, col):
        '''
        Take in a row and column and return a list of tuples of valid indexs
        '''
        valid_adjacent = []
        
        for r in range(row - 1, row +2):
            if r >= 0 and r < len(grid):
                for c in range(col-1, col+2):
                    if c >=0 and c < len(grid[0]):
                        if mask[r][c] == True:
                            valid_adjacent.append((r,c))
        return valid_adjacent
    
    def get_point_score(self,str):
        points = 0
        for char in str:
            points += self.char_values[char]
        return points


mat_str = sys.argv[1]
# Create Grid
handler = GridHandler()
grid = handler.map_str_to_2d_list(mat_str)


 # TODO: Figure out how to incorporate knowledge of double letter, 2x, gems

def recursive_search(str, mask, depth, found_words, row, col):
    # If current word is a valid scrabble word, add to accumulated list, along with point score
    if str in valid_words and len(str) > 2:
        found_words.append((str, handler.get_point_score(str)))
    # If new_depth exceeds max_depth, do not recurse any further
    new_depth = depth + 1 
    if new_depth > max_depth:
        return
    
    # Get all valid adjacent char indices
    adjacent_char_indxs = handler.get_valid_adjacent(mask, row, col)

    # Recursively call search with all new char combinations
    for index in adjacent_char_indxs:
        row, col = index[0],index[1]

        # Create a new bool mask and make newly selected letter invalid
        mask[row][col]= False
        # Call recursive search with new string and new_mask
        char = grid[row][col]
        recursive_search(str + char, mask, new_depth, found_words, row, col)
        mask[row][col] = True
        
    return

def worker(char, mask, row, col, results):
    found_words = []
    recursive_search(char, mask, 1, found_words, row, col)
    results.append(found_words) 

if __name__ == '__main__':

    starting_bool_mask = [[True for pos in range(len(row))] for row in grid]

    processes = []

    with Manager() as manager:
        results = manager.list()
        # Create search processes, one for each starting character
        for row_idx, row in enumerate(grid):
            for col, char in enumerate(row):
                new_mask = copy.deepcopy(starting_bool_mask)
                # Make starting letter invalid
                new_mask[row_idx][col] = False
                process = Process(target=worker, args=(char, new_mask, row_idx, col, results))
                processes.append(process)

        start = time.time()

        # Start Processes
        for p in processes: 
            p.start()

        for p in processes:
            p.join()

        print(f'Elapsed time of: {time.time() - start}s for max depth: {max_depth}')
        playable_words = []
        # Compile results
        for result in results:
            playable_words += result

    playable_words.sort(key=lambda tup: tup[1], reverse = True)
    print_words = playable_words[0:10]
    for word in print_words:
        print(word)
