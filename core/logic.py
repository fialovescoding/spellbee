from core.crud import SpellBee_CrudManager
from core.models import *

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


    def _get_word_from_list(self, student_id: str, list_name: str) -> Word:
        """Helper Function: Check if the list has any word, and if so, return the 1st word, else return None"""
        # list_: list = dict_of_lists[list_name]
        # if len(list_) > 0:
        #     word = list_.pop()
        # else:
        #     word = None

        word_type = self._get_word_type_from_list_name(list_name)

        # Get next word in list from database
        word = self.crud_engine.get_next_word(student_id, word_type)

        return word


    def _get_next_word_list_name(self, student_id: str):
        # Get next list to check from db
        return self.crud_engine.get_next_list(student_id)


    def _set_next_word_list_name(self, student_id: str, next_list: str):
        self.crud_engine.set_next_list(student_id, next_list)


    def move_word_to_list(self, student_id: str, word: Word, next_list: str):
        word_type = self._get_word_type_from_list_name(next_list)

        self.crud_engine.update_word(student_id, word, word_type)


    def select_next_test_word(self, student_id) -> Word:
        list_name: NextWordList = self._get_next_word_list_name(student_id)

        if list_name is None:
            list_name = 'new'
            self._set_next_word_list_name(student_id, list_name)
        else:
            list_name = list_name.next_list

        word = self._get_word_from_list(student_id, list_name)

        if list_name == 'new':
            next_list = 'retest'
        elif list_name == 'retest':
            next_list = 'new'

        # Update next word list
        self._set_next_word_list_name(student_id, next_list)

        return word

        # Check which list to check next (new or retest)
        if next_list_name == 'new':
            list_order = ['new', 'retest', 'incorrect', 'correct']
        else:
            # next_list_name should be 'retest' here
            list_order = ['retest', 'new', 'incorrect', 'correct']

        for list_name in list_order:
            # Check if list has any word
            word = get_word_from_list(student_id, list_name) #, dict_of_lists)
            if word is not None:
                # We found the word, update variables and return the word

                if list_name == 'new':
                    next_list_name = 'retest'
                elif list_name == 'retest':
                    next_list_name = 'new'

                # TODO: save the updated lists to db

                return word
            # else, check next list - the loop will do it for us

    # Check the code
    # next_word = select_next_test_word(0)
    # if next_word is not None:
    #     print(next_word)


        # Example to access lists_dict to get a list by its name
        # new_list: list = lists_dict['new']
        # if len(new_list) > 0:
        #     # Get the 1st element of list (FIFO)
        #     word = new_list.pop()  
        # elif len(lists_dict['retest']) > 0:
        #     word = lists_dict['retest'][0]
        # elif len(lists_dict['incorrect']) > 0:
        #     word = lists_dict['incorrect'][0]
        # elif len(lists_dict['correct']) > 0:
        #     word = lists_dict['correct'][0]

        # return word