print('From nicegui_client.app')
import context

from algorithm.word_select import *
from data.models import *

##########################
# NiceGui App Entry File #
##########################
from typing import Dict

from nicegui import ui, app

APP_TITLE = 'Spell Bee'
student_id = 'fia'

# App startup
def on_app_start():
    # TODO: separate into theme control
    ui.dark_mode().enable()
    ui.colors(primary='indigo', secondary='purple')

app.on_startup(on_app_start)

def show_spellbee():
    with main_area:
        for i in range(0,9):
            print(f'Getting word {i}...\n')
            test_word = select_next_test_word(student_id)
            if test_word is not None:
                ui.label(test_word.data)
                
                # TODO: update word
                move_word_to_list(student_id, test_word, 'retest')
            else:
                print('Cound not get any word!')

# App Layout and Containers #
header = ui.header().classes(replace='row items-center')

#############
# Main Area #
#############

# Menu bar within main area
menubar = ui.row()

# Fixed Top-bar
fixed_topbar = ui.row()

# Scrollable area for main content
main_area = ui.column() #scroll_area().classes('h-400') # TODO: How to set height to fill remaining space on visible page?

###########
# Sidebar #
###########

sidebar = ui.left_drawer() #.classes('bg-darkgray-100')

##########
# Header #
##########
with header:
    # Sidebar show/hide button
    ui.button(on_click=lambda: sidebar.toggle(), icon='menu').props('flat color=white')

    # App Logo
    ui.button(APP_TITLE, on_click=lambda: show_spellbee())


# Run the app
ui.run(title=APP_TITLE, port=8080)