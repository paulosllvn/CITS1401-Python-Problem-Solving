
"""
Author Paul O'Sullivan 21492318

Assumptions: For punctuations the project description was very unclear.

"..your program should count certain pieces of punctuation:
comma and semicolon. In addition, your program should also count singlequote and
hyphen, but only under certain circumstances...Any other punctuation or letters,
e.g '.' when not at the end of a sentence, should be regarded as white space,
so serve to end words."

This is not clear and my interpretation of this is that any punctuation other than comma
and semicolon not at the end of a sentence should be considered a white space.

So for example, the word "hello,world" or "hello;world" will not be split into two words
and will be regarded as one word "hello,world" / "hello;world"
"""



import os,math


# Reads in text files and strips punctuation as specified in the project description
# Conditions spread out between if statements for simpler reading
def readFiles(file):
    with open(file, "r") as f:
        lines = (line.replace("--", " ") for line in f)
        lines = (line.split() for line in lines)
        lines = (["\n"] if not list else list for list in lines)
        newlist = []
        for l in lines:
            newlist.extend(l)


    text2 = []
    for i, word in enumerate(newlist):
        word2 = ''
        for j, letter in enumerate(word):
            if letter.isalnum() or j == len(word) - 1:
                word2 += letter

            elif not letter.isalnum or letter == ',' or letter == ';':
                word2 += letter

            elif not letter.isalnum() and j != len(word) - 1 and word[j + 1] == '"' or word[j+1] == "'":
                word2 += letter

            elif letter == "'" and j != len(word) - 1 and word[j + 1].isalnum():
                word2 += letter

            elif letter == "-" and j != len(word) - 1 and word[j + 1].isalnum():
                word2 += letter
            else:
                text2.append(word2)
                word2 = ''
        text2.append(word2.lower())

    text3 = [x for x in text2 if len(x) > 0]
    return text3

#Calculates the number of paragraphs by counting the number of newline characters
#Counts one newline character if followed by further newline characters
def numpara(lines,sent):
    count = 0
    for i, line in enumerate(lines):
        if (lines[i] == '\n' and lines[i - 1] != '\n') or i == len(lines) - 1:
            count += 1

    # print(count)
    answer = round(sent/count,4)
    dict_sentpara = {'sentences_per_par':answer}


    return dict_sentpara

#Calculates the number of sentences by counting the sentence ending characters
def numwords(text):

    newtext = []
    for j, word in enumerate(text):
        count = 0

        for i, letter in enumerate(word):
            if not letter.isalnum():
                count += 1
        if count == len(word):
            continue
        else:
            newtext.append(word)

    endsent = '.!?'
    countlist = []

    count = 0
    for j, word in enumerate(newtext):
        count += 1
        for i, letter in enumerate(word):
            if letter in endsent:
                countlist.append(count)
                count = 0


    avg = sum(countlist) / len(countlist)


    dict_words = {'words_per_sentence':avg}

    return dict_words,len(countlist)

#Counts how often each word in the text is repeated. Returns as a dictionary.
def unifarms(text):
    newlist = []

    for i,word in enumerate(text):
        for j, letter in enumerate(word):
            if not letter.isalnum() and j < len(word) - 1 and word[j - 1].isalnum() and word[j + 1].isalnum() and j!=0:
                continue
            elif not letter.isalnum():
                word = word.replace(letter, '')
        newlist.append(word)
    text3 = [x for x in newlist if len(x) > 0]

    dict_unifarm = {}
    for i in text3:
        if i not in dict_unifarm:
            dict_unifarm[i] = 1
        else:
            dict_unifarm[i] += 1
    return dict_unifarm

#Counts the punctuation marks as outlined in "dict_punctuation"
def punctuation(lines):

    dict_punctuation = {',': 0, ';': 0, '-': 0, '\'': 0}
    for word in lines:
        for i, j in enumerate(word):
            if j in dict_punctuation:
                if j == ';' or j == ',':
                    dict_punctuation[j] += 1
                elif j == '\'' and i < len(word) - 1 and i > 0:
                    if word[i - 1].isalpha() and word[i + 1].isalpha():
                        dict_punctuation[j] += 1
                    else:
                        continue
                elif j == '-' and i < len(word) - 1 and i > 0:
                    if word[i - 1].isalpha() and word[i + 1].isalpha():
                        dict_punctuation[j] += 1
                    else:
                        continue
    return dict_punctuation

#Counts the number of conjunctions as specified and returns them as a dictionary.
def conjunctions(text):
    newlist = []

    # If symbols are their own words do we strip those?
    for word in text:
        for j, letter in enumerate(word):
            if not letter.isalnum():
                word = word.replace(letter, '')
        newlist.append(word)

    dict_conjunctions = {'also': 0, 'although': 0, 'and': 0, 'as': 0, 'because': 0, 'before': 0, 'but': 0,
                         'for': 0, 'if': 0, 'nor': 0, 'of': 0, 'or': 0, 'since': 0, 'that': 0, 'though': 0,
                         'until': 0, 'when': 0, 'whenever': 0, 'whereas': 0, 'which': 0, 'while': 0, 'yet': 0}

    for i in newlist:
        if i in dict_conjunctions:
            dict_conjunctions[i] += 1

    return dict_conjunctions

#Dictionary combining conjunction and punctuaion dictionaries as well as
# number of words per sentence and number of sentences per paragraph.
def composite(conjunction, conjunction2, punctuation, punctuation2,sentpara,sentpara2,wordsent,wordsent2):

    dict_comp1 = dict()
    dict_comp2 = dict()
    dict_comp1.update(conjunction)
    dict_comp1.update(punctuation)
    dict_comp1.update(wordsent)
    dict_comp1.update(sentpara)
    dict_comp2.update(conjunction2)
    dict_comp2.update(punctuation2)
    dict_comp2.update(wordsent2)
    dict_comp2.update(sentpara2)

    return dict_comp1, dict_comp2

#Calculates the distance between profiles to determine the similarities of each text.
def distance(profile1,profile2):

    profilecopy = profile2.copy()
    dist = []
    for item in profile1:
        if item in profile2:
            value1 = profile1.get(item)
            value2 = profilecopy.get(item)
            dist.append((value1-value2)**2)
            profilecopy.pop(item)
        else:
            dist.append(profile1.get(item)**2)
    for item in profilecopy:
        dist.append(profilecopy.get(item)**2)


    return math.sqrt(sum(dist))


#Calls the relevant function while also performs error checks
def main(textfile1, textfile2, feature):

    feature = feature.lower().strip()
    # If file does not exist, print error and exit
    if not os.path.isfile(textfile1) or not os.path.isfile(textfile2):
        print("ERROR : One or both of these files does not exist")
        exit(1)

    # Checks to ensure that the inputted file is not empty.
    if os.stat(textfile1).st_size == 0 or os.stat(textfile2).st_size == 0:
        print("ERROR : One or both of these files is an empty file")
        exit(1)

    # If metric is not valid, print error and exit
    if feature not in {"punctuation", "unigrams", "conjunctions", "composite"}:
        print("ERROR: This feature is invalid")
        exit(1)

    text1 = readFiles(textfile1)
    text2 = readFiles(textfile2)

    if feature == "conjunctions":
        dict_conjunction1 = conjunctions(text1)
        dict_conjunction2 = conjunctions(text2)
        dist = "Distance: {:.4f}".format(distance(dict_conjunction1, dict_conjunction2))
        return (dist,dict_conjunction1,dict_conjunction2)

    elif feature == "punctuation":
        dict_punctuation1 = punctuation(text1)
        dict_punctuation2 = punctuation(text2)
        dist = "Distance: {:.4f}".format(distance(dict_punctuation1, dict_punctuation2))
        return (dist,dict_punctuation1,dict_punctuation2)


    elif feature == "unigrams":
        dict_unifarm1 = unifarms(text1)
        dict_unifarm2 = unifarms(text2)
        dist ="Distance: {:.4f}".format(distance(dict_unifarm1, dict_unifarm2))
        return (dist, dict_unifarm1, dict_unifarm2)


    elif feature == "composite":
        dict_conjunction1 = conjunctions(text1)
        dict_conjunction2 = conjunctions(text2)
        dict_punctuation1 = punctuation(text1)
        dict_punctuation2 = punctuation(text2)
        numword, numsent = numwords(text1)
        numparag = numpara(text1, numsent)
        numword2, numsent2 = numwords(text2)
        numparag2 = numpara(text2, numsent2)
        profile1,profile2 = composite(dict_conjunction1, dict_conjunction2, dict_punctuation1, dict_punctuation2, numparag, numparag2,
                  numword, numword2)
        dist = "Distance is: {:.4f}".format(distance(profile1,profile2))

        return (dist, profile1, profile2)
