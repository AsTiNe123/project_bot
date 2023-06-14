from string import ascii_letters

async def make(last_word, mistake_words = []):
    sending_words = mistake_words
    with open('lisst_of_words.txt') as file:
        file = file.readlines()
        f = [i for i in file.split()]
    
    index = await f.index(last_word)+1
    while len(sending_words)!= 5 or index != len(f):
        sending_words += [f[index]]
        index+=1
        sending_words = sending_words.join("\n")
        sending_words.replace("-------", " - ")
    return sending_words

def check(answers, today_words):
    result = []
    with open('lisst_of_words.txt') as file:
        file = file.readlines()
        file = [i for i in file.split()]
        for i in range(5):
            word = today_words[i]
            answer = answer[i]
            index = file.index(word)
            liter = ascii_letters()
            if word[0] in liter:
                if set(file[index].split("-------")[0]) == set([answer]):
                    result +=[1]
                else:
                    result += [0]
            else:
                if set(file[index].split("-------")[1].split()) == set([answer]):
                    result +=[1]
                else:
                    result += [0]



    return result