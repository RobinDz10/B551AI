# SeekTruth.py : Classify text objects into two categories
#
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math
import random


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#


def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    bag_of_words_class_truthful = {}  # the real bag_of_words
    bag_of_words_class_deceptive = {}  # the fake bag_of_words
    total_truthful = 0
    total_deceptive = 0
    for index in range(0, len(train_data["objects"])):
        review = train_data["objects"][index]
        label = train_data["labels"][index]
        words = review.strip().split(' ')
        # remove punctuation characters/marks
        for word in words:
            # I will remove most punctuation characters, but i will keep these: % - _
            # for example, I treat these strings as NORMAL words and I will not filter them out: 70%, as-i-wish, a_character
            word_filtered = "".join(c for c in word if c not in (
                '#', ';', ']', '[', '$', ')', '(', '/', "'", '+', '!', '.', ':', ',', '"', '?', '*', '&', '\x96',
                '\x97', '\x85'))
            if label == 'truthful':
                total_truthful += 1
                if word_filtered not in bag_of_words_class_truthful.keys():
                    bag_of_words_class_truthful[word_filtered] = 1
                else:
                    bag_of_words_class_truthful[word_filtered] += 1
            else:
                total_deceptive += 1
                if word_filtered not in bag_of_words_class_deceptive.keys():
                    bag_of_words_class_deceptive[word_filtered] = 1
                else:
                    bag_of_words_class_deceptive[word_filtered] += 1
    # end of training

    # prior
    smoothing = 0.5  # whatever it is, it's better than no-smoothing
    # turns bag_of_words dictionary from 'count of words' to the 'proportion of words'
    for key, value in bag_of_words_class_truthful.items():
        bag_of_words_class_truthful[key] = math.log(
            (value + smoothing) / (total_truthful + train_data["labels"].count("truthful") * smoothing),
            math.e)
    for key, value in bag_of_words_class_deceptive.items():
        bag_of_words_class_deceptive[key] = math.log(
            (value + smoothing) / (total_deceptive + train_data["labels"].count("deceptive") * smoothing),
            math.e)

    prior_truthful = math.log(train_data["labels"].count("truthful") / (len(train_data["labels"])), math.e)
    prior_deceptive = math.log(train_data["labels"].count("deceptive") / (len(train_data["labels"])), math.e)
    res = []
    for index in range(0, len(test_data["objects"])):
        test_review = test_data["objects"][index]
        words = test_review.strip().split(' ')
        post_truthful = prior_truthful
        post_deceptive = prior_deceptive
        # remove punctuation characters/marks
        for word in words:
            # I will remove most punctuation characters, but i will keep these: % - _
            # I treat these strings as NORMAL words and I will not filter them out: 70%, as-i-wish, a_character
            word_filtered = "".join(c for c in word if c not in (
                '#', ';', ']', '[', '$', ')', '(', '/', "'", '+', '!', '.', ':', ',', '"', '?', '*', '&', '\x96',
                '\x97', '\x85'))
            # a word should exist at least one bag_of_words dictionary, otherwise it should be skipped
            if word_filtered in bag_of_words_class_truthful.keys() or word_filtered in bag_of_words_class_deceptive.keys():
                if word_filtered in bag_of_words_class_truthful.keys():
                    post_truthful = post_truthful + bag_of_words_class_truthful[word_filtered]
                else:
                    post_truthful = post_truthful + math.log(
                        smoothing / (total_truthful + train_data["labels"].count("truthful") * smoothing), math.e)

                if word_filtered in bag_of_words_class_deceptive.keys():
                    post_deceptive = post_deceptive + bag_of_words_class_deceptive[word_filtered]
                else:
                    post_deceptive = post_deceptive + math.log(
                        smoothing / (total_deceptive + train_data["labels"].count("deceptive") * smoothing), math.e)

        if post_truthful > post_deceptive:
            res.append('truthful')
        elif post_truthful < post_deceptive:
            res.append('deceptive')
        else:
            if random.randint(1, 2) == 1:
                res.append('truthful')
            else:
                res.append('deceptive')

    return res


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
