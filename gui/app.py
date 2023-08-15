import context

import streamlit as st
# from playsound import playsound
from data.crud import SpellBee_CrudManager

# Word list
word_list = ['mat', 'umbrella' , "cat" , "car" , "room" , "orphanage" , "day" , "goat"  "locomotion" , "garden"]

#TODO: remove this and add playsound...

# svar = session variable
svar_play_word = 'tmp_play_word'

# wk = widget key
wk_listen_word = 'btn_listen_word'
wk_spell_word = 'txt_spell_word'
wk_check_answer = 'btn_check_answer'

def set_word_under_test(test_word: str):
    st.session_state[svar_play_word] = test_word.lower()

def get_word_under_test() -> str:
    if svar_play_word in st.session_state:
        return st.session_state[svar_play_word]
    else:
        return None

def play_word():
    # TODO: remove once we can play the sound
    # playsound(r"C:\Users\aanya\git\spellbee\basics\welcome.mp3")

    word_to_play = get_word_under_test()

    if word_to_play is not None:
        st.write(word_to_play)


def select_word_to_test():
    # Randomly select the next word to be tested
    return 'Hello'


def handle_check_answer():
    # print(st.session_state)

    # Get the value typed by user in answer text input
    ch_answer: str = st.session_state[wk_spell_word]

    # Check the answer
    if ch_answer.lower() == get_word_under_test():
        st.write('Well done')
    else:
        st.write('Try Again')


def handle_listen_word():
    # print(st.session_state)
    
    # Select the word to play
    test_word = select_word_to_test()

    # Set the word under test
    set_word_under_test(test_word)

    # Play the word
    play_word()


def show():
    st.write('Listen to :red[the word] and :blue[type it and cheek if it is correct]')
    st.button('Listen to the word', key = wk_listen_word, on_click = handle_listen_word)
    st.text_input('Write the word spelling', key = wk_spell_word)
    st.button('Cheek the answer', key = wk_check_answer, on_click = handle_check_answer)


# Main

engine = SpellBee_CrudManager(recreate_table=False)

show()