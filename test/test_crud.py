import context

from data.crud import SpellBee_CrudManager
from data.models import *
import random

recreate = True

engine = SpellBee_CrudManager(recreate_table=recreate)

word_list = ['mat', 'umbrella' , "cat" , "car" , "room" , "orphanage" , "day" , "goat",  "locomotion" , "garden"]

student_id = 'fia'

add_words = recreate
if add_words:
    for word in word_list:
        engine.add_new_word(student_id, word)

word_types = list(WordType)
non_new_word_types = list(set(word_types).difference(set([WordType.NEW])))

for i in range(0,9):
    # word_type = WordType.NEW
    random.seed(10)
    word_type = random.choice(word_types)
    result = engine.get_next_word(student_id, word_type)
    if result is not None:
        n = len(result)
        assert(n <= 1)
        if n == 1:
            next_word = result[0]
            print(next_word, word_type)
            new_type = random.choice(non_new_word_types)
            engine.update_word(student_id, next_word, new_type)