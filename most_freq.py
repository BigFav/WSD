import array
import sys
from collections import defaultdict
#does most frequent baseline


word_dict = defaultdict(lambda: defaultdict(int))
with open("training_data.data", "r") as train:
    for line in train:
        line = line.partition(' | ')
        num = int(line[2].partition(' ')[0])
        word_dict[line[0]][num] += 1

with open("validation_data.data", "r") as val:
    for line in val:
        line = line.partition(' | ')
        num = int(line[2].partition(' ')[0])
        word_dict[line[0]][num] += 1
        
#find max for each word
for word,num_count in word_dict.iteritems():
    max_num = 0
    max_count = 0
    for num,count in num_count.iteritems():
        if count > max_count:
            max_num = num
            max_count = count
    #replace value in dictionary
    word_dict[word] = max_num


in_name = "%s_data.data" % (sys.argv[1])
out_name = "%s_most_freq_baseline.txt" % (sys.argv[1])
output = []
if sys.argv[1] == "test":
    with open(in_name, "r") as comp:
        for line in comp:
            line = line.partition(' |')
            output.append(word_dict.get(line[0], 1))

        
    output = '\n'.join(map(str, output))
    with open(out_name, "w") as out:
        out.write(output)

else:
    correct = 0
    with open(in_name, "r") as comp:
        for line in comp:
            line = line.partition(' | ')
            actual = int(line[2].partition(' ')[0])
            guess = word_dict[line[0]]
            output.append(guess)
            
            if guess is actual:
                correct += 1

    acc = "Accuracy is %0.2f percent\n" % (float(correct)/len(output) * 100)
    output = '\n'.join(map(str, output))
    with open(out_name, "w") as out:
        out.write(acc)
        out.write(output)
    print acc
