scrabble_words = []
reasonable_words = []
with open('vocabs/temp.txt', 'r') as reasonable, open('vocabs/scrabble_120k.txt', 'r') as scrabble:
    word = reasonable.readline().strip()
    while(word):
        if(len(word) > 2):
            reasonable_words.append(word)
        word = reasonable.readline().strip()
    
    word = scrabble.readline().strip()
    while(word):
        scrabble_words.append(word)
        word = scrabble.readline().strip()

    reasonable.close()
    scrabble.close()





with open('common_10k.txt', 'w+') as f:
    i = 0
    for word in reasonable_words:
        if word in scrabble_words:
            f.write(word + '\n')
        i+=1
    
        if i % 2500 == 0: print(i)
    f.close()