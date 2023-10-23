import context

from core.crud import SpellBee_CrudManager
from core.models import *

# To clear old list, set to True
recreate = True
student_id = 'fia'

engine = SpellBee_CrudManager(recreate_table=recreate)

if recreate:
    engine.set_next_list(student_id, 'new')

# Add your words here
word_list = ['mat', 'umbrella' , "cat" , "car" , "room" , "orphanage" , "day" ,
             "goat",  "locomotion" , "garden"]

add_words = True
if add_words:
    for word in word_list:
        engine.add_new_word(student_id, word)
