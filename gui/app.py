import streamlit as st
from playsound import playsound
word_list = ['cat', 'umbrella' , "cat" , "car" , "room" , "orphanage" , "day" , "goat"  "locomotion" , "garden"]

# Part 1: Get data to show

# Part 2: Create GUI
# def show_user_info_screen():
#     st.write("Enter your personal details")
#     st.text_input('Name', '', key = 'w_name')
#     st.text_input('Phone Number', '', key = 'w_phone')
#     st.button('Submit', key = 'w_submit', on_click = save_user_info)

#TODO: remove this and add playsound...
wk_play_word = 'tmp_play_word'

wk_listen_word = 'btn_listen_word'
wk_spell_word = 'txt_spell_word'
wk_check_answer = 'btn_check_answer'
def show_test_screen():
    st.write('Listen to :red[the word] and :blue[type it and cheek if it is correct]')
    st.button('Listen to the word', key = wk_listen_word, on_click = handle_listen_word)
    st.text_input('Write the word spelling', key = wk_spell_word)
    st.button('Cheek the answer', key = wk_check_answer, on_click = handle_check_answer)


def show():
    show_test_screen()
    
    if wk_play_word in st.session_state:
        st.write(st.session_state[wk_play_word])

def handle_check_answer():
    print(st.session_state)

    # Get the value typed by user in answer text input
    ch_answer = st.session_state[wk_spell_word]

    # Check the answer
    if ch_answer == 'hello':
        st.write('Well done')
    else:
        st.write('Try Again')

# Part 3: Event handlers
# def save_user_info():
#     name = st.session_state['w_name']
#     phone = st.session_state['w_phone']
#     st.write('Your name is ' + name + ' and your number is ' + phone)


def handle_listen_word():
    print(st.session_state)
    
    st.session_state[wk_play_word] = 'Hello'
    # playsound(r"C:\Users\aanya\git\spellbee\basics\welcome.mp3")


# Main
show()