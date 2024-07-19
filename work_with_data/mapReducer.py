"""MapReduce is a calculation model for implementation of parralel operations over big data.
First step is mapper, that returns each element in 0 or mkore 'key-value' pairs.
Second step is to collect all pairs with same keys
Third step is to apply reducer to each collection of grouped values."""

from functools import partial
import math, random, re, datetime
from collections import Counter, defaultdict

def tokenize(message):
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return set(all_words)
def reduce_with(aggregation_fn, key, values):
    """reduces a key-values pair by applying aggregation_fn to the values"""
    yield (key, aggregation_fn(values))
def values_reducer(aggregation_fn):
    """turns a function (values -> output) into a reducer"""
    return partial(reduce_with, aggregation_fn)
def map_reduce(inputs, mapper, reducer):
    """runs MapReduce on the inputs using mapper and reducer"""
    collector = defaultdict(list)
    for input in inputs:
        for key, value in mapper(input):
            collector[key].append(value)
    return [output 
            for key, values in collector.items() 
            for output in reducer(key, values)]
sum_reducer = values_reducer(sum)
max_reducer = values_reducer(max)

status_updates = [
    {"id": 1,
     "username" : "joelgrus",
     "text" : "Is anyone interested in a data science book?",
     "created_at" : datetime.datetime(2013, 12, 21, 11, 47, 0),
     "liked_by" : ["data_guy", "data_gal", "bill"] 
     },
     {
        "id": 2,
        "username": "codewizard",
        "text": "Learning Python is fun!",
        "created_at": datetime.datetime(2024, 1, 19, 14, 35, 45),
        "liked_by": ["joelgrus", "dataguy"]
    },
    {
        "id": 3,
        "username": "joelgrus",
        "text": "Is anyone interested in a data science book?",
        "created_at": datetime.datetime(2024, 8, 5, 12, 47, 59),
        "liked_by": ["pythonguru", "dataguy", "codewizard"]
    },
    {
        "id": 4,
        "username": "pythonguru",
        "text": "Data science is amazing!",
        "created_at": datetime.datetime(2024, 3, 14, 9, 15, 8),
        "liked_by": ["joelgrus", "dataguy"]
    },
    {
        "id": 5,
        "username": "datagal",
        "text": "Who wants to join a study group?",
        "created_at": datetime.datetime(2024, 11, 23, 17, 5, 33),
        "liked_by": ["dataguy", "joelgrus", "pythonguru"]
    },
    {
        "id": 6,
        "username": "dataguy",
        "text": "Is anyone interested in a data science book?",
        "created_at": datetime.datetime(2024, 10, 27, 5, 42, 21),
        "liked_by": ["pythonguru"]
    },
    {
        "id": 7,
        "username": "joelgrus",
        "text": "Just completed a new project!",
        "created_at": datetime.datetime(2024, 9, 2, 21, 27, 12),
        "liked_by": ["dataguy", "datagal"]
    },
    {
        "id": 8,
        "username": "pythonguru",
        "text": "Learning Python is fun!",
        "created_at": datetime.datetime(2024, 2, 18, 6, 53, 40),
        "liked_by": ["dataguy", "joelgrus"]
    },
    {
        "id": 9,
        "username": "datagal",
        "text": "Who wants to join a data science group?",
        "created_at": datetime.datetime(2024, 4, 10, 19, 18, 4),
        "liked_by": ["codewizard", "dataguy"]
    },
    {
        "id": 10,
        "username": "codewizard",
        "text": "Data science is amazing!",
        "created_at": datetime.datetime(2024, 12, 15, 11, 20, 55),
        "liked_by": ["joelgrus", "datagal", "dataguy"]
    }
]

def data_science_day_mapper(status_update):
    """ yields (day_of_week, 1) if status_update contains 'data science' """
    if "data science" in status_update["text"].lower():
        day_of_week = status_update["created_at"].weekday()
        yield (day_of_week, 1)
data_science_days = map_reduce(status_updates, data_science_day_mapper, sum_reducer)
print(data_science_days)

def words_per_user_mapper(status_update):
    user = status_update["username"]
    for word in tokenize(status_update["text"]):
        yield(user, (word, 1))
def most_popular_word_reducer(user, words_and_count):
    """given a sequence of (word, count) paris, 
    return the word with the highest total count"""
    word_count = Counter()
    for word, count in words_and_count:
        word_count[word] += count
    word, count = word_count.most_common(1)[0]
    yield (user, (word, count))

user_words = map_reduce(status_updates, words_per_user_mapper, most_popular_word_reducer)
print(user_words)