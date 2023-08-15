import context

from data.crud import SpellBee_CrudManager

engine = SpellBee_CrudManager(recreate_table=False)

word_list = ['mat', 'umbrella' , "cat" , "car" , "room" , "orphanage" , "day" , "goat"  "locomotion" , "garden"]

for word in word_list:
    engine.add_new_word('fia', word)