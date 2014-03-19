import sys
import subprocess
from collections import defaultdict
from random import randint

#Does random guess baseline


def get_accuracy(predicted, actual): 
    correct = sum([1 for (a,b) in zip(predicted,actual) if a is b]) 
    return correct/float(len(predicted))

    
in_name = "%s_data.data" % (sys.argv[1])
out_name = "%s_rand_baseline.txt" % (sys.argv[1])

#must get range of nums for each word, just max will do
words = []
word_dict = defaultdict(int)
if sys.argv[1] == "test":
    with open("training_data.data", "r") as comp:
        for line in comp:
            line = line.partition(' | ')
            word = line[0]
            num = int(line[2].partition(' ')[0])
            word_dict[word] = max(word_dict[word], num)

    with open("validation_data.data", "r") as comp:
        for line in comp:
            line = line.partition(' | ')
            word = line[0]
            num = int(line[2].partition(' ')[0])
            word_dict[word] = max(word_dict[word], num)

    with open(in_name, "r") as comp:
        for line in comp:
            line = line.partition(' | ')
            word = line[0]
            num = int(line[2].partition(' ')[0])
            word_dict[word] = max(word_dict[word], num)
            words.append(word)

    output = ["%d\n" % randint(1,word_dict[word]) for word in words]
    with open(out_name, "w") as comp:
        comp.writelines(output)
else:
    nums = []
    with open(in_name, "r") as comp:
        for line in comp:
            line = line.partition(' | ')
            word = line[0]
            num = int(line[2].partition(' ')[0])
            word_dict[word] = max(word_dict[word], num)
            words.append(word)
            nums.append(num)
    
    output = [randint(1,word_dict[word]) for word in words]
    acc = get_accuracy(output, nums) * 100
    output = '\n'.join(map(str,output))
    acc = "Accuracy is %0.2f percent\n" % (acc)
    with open(out_name, "w") as out:
        out.write(acc)
        out.write(output)
    print acc
