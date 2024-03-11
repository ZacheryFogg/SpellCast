scrabble_words = []
reasonable_words = []
with open('reasonable_words.txt', 'r') as reasonable, open('scrabble_words.txt', 'r') as scrabble:
    word = reasonable.readline()
    while(word):
        if(len(word) > 2):
            reasonable_words.append(word.strip())
        word = reasonable.readline()
    
    word = scrabble.readline()
    while(word):
        scrabble_words.append(word.strip())
        word = scrabble.readline()

    reasonable.close()
    scrabble.close()





with open('normal_valid_words.txt', 'w+') as f:
    i = 0
    for word in reasonable_words:
        if word in scrabble_words:
            f.write(word + '\n')
        i+=1
    
        if i % 5000 == 0: print(i)
    f.close()