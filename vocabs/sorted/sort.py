words = []
fname = 'scrabble_120k'
with open(f'../{fname}.txt', 'r') as f:
    word = f.readline().strip()
    while word: 
        words.append(word)
        word = f.readline().strip()
    f.close()

words.sort()


with open(f'{fname}_sorted.txt', 'w+') as f:
    for word in words:
        f.write(word + '\n')
    f.close()