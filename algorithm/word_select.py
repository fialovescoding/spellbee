from typing import Tuple

def load_word_lists(student_id) -> Tuple[dict, str]:
    #TODO: load from db
    new_word_list = []

    retest_list = []

    incorrect_list = []

    correct_list = []

    # This tells the next list from which the word should be selected the next time
    next_list_name = 'new'

    dict_of_lists = {'new': new_word_list,
            'retest': retest_list, 
            'incorrect': incorrect_list,
            'correct': correct_list}
    
    return dict_of_lists, next_list_name

def get_word_from_list(list_name, dict_of_lists):
    """Helper Function: Check if the list has any word, and if so, return the 1st word, else return None"""
    list_: list = dict_of_lists[list_name]
    if len(list_) > 0:
        word = list_.pop()
    else:
        word = None

    return word
    
def select_next_test_word(student_id):
    # Get the word lists from db
    dict_of_lists, next_list_name = load_word_lists(student_id)

    word = None

    # Check which list to check next (new or retest)
    if next_list_name == 'new':
        list_order = ['new', 'retest', 'incorrect', 'correct']
    else:
        # next_list_name should be 'retest' here
        list_order = ['retest', 'new', 'incorrect', 'correct']

    for list_name in list_order:
        # Check if list has any word
        word = get_word_from_list(list_name, dict_of_lists)
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
next_word = select_next_test_word(0)
if next_word is not None:
    print(next_word)


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