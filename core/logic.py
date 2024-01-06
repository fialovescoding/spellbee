from core.crud import SpellBee_CrudManager
from core.models import *
from datetime import datetime

# def load_word_lists(student_id) -> Tuple[dict, str]:
#     #TODO: load from db
#     new_word_list = []

#     retest_list = []

#     incorrect_list = []

#     correct_list = []

#     # This tells the next list from which the word should be selected the next time
#     next_list_name = 'new'

#     dict_of_lists = {'new': new_word_list,
#             'retest': retest_list, 
#             'incorrect': incorrect_list,
#             'correct': correct_list}
    
#     return dict_of_lists, next_list_name

class SpellBee_LogicEngine():
    def __init__(self) -> None:
        self.crud_engine = SpellBee_CrudManager()


    def _get_word_type_from_list_name(self, list_name: str):
        match(list_name):
            case 'new':
                word_type = WordType.NEW
            case 'retest':
                word_type = WordType.RETEST
            case 'incorrect':
                word_type = WordType.INCORRECT
            case 'correct':
                word_type = WordType.CORRECT
            case _:
                raise ValueError('Invalid list name')

        return word_type


    def _get_word_from_list(self, student_id: str, list_name: str) -> str:
        """Helper Function: Check if the list has any word, and if so, return the 1st word, else return None"""
        # list_: list = dict_of_lists[list_name]
        # if len(list_) > 0:
        #     word = list_.pop()
        # else:
        #     word = None

        print(f'Getting word from {list_name} list...')

        # Get the word type
        word_type = self._get_word_type_from_list_name(list_name)

        # Get next word in list from database
        word = self.crud_engine.get_next_word(student_id, word_type)

        if word is not None:
            return word.data
        else:
            return None


    def _get_next_word_list_name(self, student_id: str):
        # Get next list to check from db
        return self.crud_engine.get_next_list(student_id)


    def _set_next_word_list_name(self, student_id: str, next_list: str):
        self.crud_engine.set_next_list(student_id, next_list)


    def move_word_to_list(self, student_id: str, word: str, next_list: str, last_seen: int = None):
        word_type = self._get_word_type_from_list_name(next_list)

        if last_seen is None:
            last_seen=int(datetime.now().timestamp())

        word_obj = Word(student_id=student_id, data=word,
                        type=word_type, last_seen=last_seen)

        self.crud_engine.update_word(student_id, word_obj, word_type)

    def check_spelling(self, student_id, spelling: str, test_word: str):
        if str.lower(spelling) == str.lower(test_word):
            # Correct
            self.move_word_to_list(student_id, test_word, 'correct')
            return True
        else:
            # Wrong
            self.move_word_to_list(student_id, test_word, 'incorrect')
            return False

    def select_next_test_word(self, student_id) -> Word:
        list_order = ['new', 'incorrect', 'correct']
        num_lists = len(list_order)

        # Get the list (from db) from which next word to be taken
        list_name = self._get_next_word_list_name(student_id)

        if list_name is None:
            # Can't find any stored list name, set to new
            list_name = 'new'
            # self._set_next_word_list_name(student_id, list_name)

        # Start with word = None, and try to find word in each of the lists (in list_order)
        word = None

        count = 0
        while word is None and count < num_lists:
            # Treat list_order as a circular list, and find the next list index
            next_list_index = (list_order.index(list_name) + 1) % num_lists
            next_list = list_order[next_list_index]

            # Get the next word from list
            word = self._get_word_from_list(student_id, list_name)

            # Increase count of how many times we have checked a list for next word
            count = count + 1

            if word is None:
                # Word not found in the selected list, check in other list
                list_name = next_list
            else:
                # Word is found, update the next list
                # TODO: are we going to chase the same word :)
                self._set_next_word_list_name(student_id, next_list)
                
                # Return the word to UI
                return word, list_name