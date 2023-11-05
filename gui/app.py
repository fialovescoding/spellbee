print('From nicegui_client.app')
import context

from core.logic import *
# from data.models import *

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

logic_engine = SpellBee_LogicEngine()

def check_spelling(spelling: str, test_word: str):
    result = logic_engine.check_spelling(student_id, spelling, test_word)
    if result:
        ui.notify('Yah! You are right :)', type='positive')
    else:
        ui.notify('Oho! Wrong spelling', type='negative')
    show_spellbee()

def show_spellbee():
    test_word, list_name = logic_engine.select_next_test_word(student_id)
    if test_word is not None:
        main_area.clear()
        with main_area:
            ui.label(test_word).tailwind.font_weight('bold')
            ui.label(f'Taken from list: {list_name}').tailwind.font_style('italic').text_color('blue-400')
            spelling = ui.input('Type the spelling')

            # Check spelling and update word to correct or incorrect list
            ui.button('Check Spelling', on_click=lambda: check_spelling(spelling.value, test_word))
    else:
        ui.notify('Could not get any word!', type='negative')

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
    ui.icon('spellcheck').tailwind.font_size('lg')
    ui.label('Spell Bee').tailwind.font_weight('extrabold')

    ui.button('Start Test', on_click=lambda: show_spellbee())


# Run the app
ui.run(title=APP_TITLE, port=8080)