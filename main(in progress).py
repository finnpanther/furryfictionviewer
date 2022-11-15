'''
Original Code written entirely by Finn Panther
'''

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from collections import namedtuple

#TODO Allow dynamic file selection as story content grows
import json
with open('rodney/introduction.json', 'r') as f:
    condict = json.load(f)
with open('rodney/adlib_dictionary.json', 'r') as f:
    adlibdict = json.load(f)

Interrupt_Tuple = namedtuple("InterruptTuple", "target postreturn") #@size, huge, "... his dick is so massive!"
key = '0'
interrupt_required = False
interrupt_tuple = Interrupt_Tuple(None, None)
reminder_widget_pos = 0
response_reminder_dict = {}


class Display(FloatLayout):
    pass
class TitleWindow(FloatLayout):
    pass

class InterruptButton(Button):

    def __init__(self, set_interrupt='default', target='default', blanket_return='default', **kwargs):
        super(Button, self).__init__(**kwargs)
        self.set_interrupt = set_interrupt
        self.target = target
        self.blanket_return = blanket_return

    def on_press(self):
        adlibdict[self.target]["set to"] = self.set_interrupt
        prepared_return = adlibdict[self.target]["interrupt"]["interrupt return"] + adlibdict[self.target]["interrupt"]["interrupt adlibs"][self.set_interrupt] + "\n " + self.blanket_return
        app = App.get_running_app()
        app.root.display_response_reminder(self.text)
        app.root.update_display(prepared_return)
        app.root.generate_buttons()

class FinalButton(Button):

    def on_press(self):
        global key
        global condict
        global adlibdict
        key = '0'
        condict.clear()
        adlibdict.clear()

        with open('rodney/introduction.json', 'r') as f:
            condict = json.load(f)
        with open('rodney/adlib_dictionary.json', 'r') as f:
            adlibdict = json.load(f)

        app= App.get_running_app()
        app.root.display_text = ''
        app.root.update_display(condict[key]["string"])
        app.root.generate_buttons()

class TextLabel(Label):
    pass

most_recent_game_response = TextLabel(text='') #Left blank for initial label update. It makes sense I promise

class FunkyButton(Button):

    def __init__(self, button_key='default', **kwargs):
        super(FunkyButton, self).__init__(**kwargs)
        self.button_key = button_key

    def on_press(self): #The global key now updates to each unique button press
        global key
        key = self.button_key
        app= App.get_running_app()
        app.root.display_response_reminder(self.text)
        app.root.update_display(condict[key]["string"])
        app.root.generate_buttons()

class ResponseReminder(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global reminder_widget_pos
        self.widget_pos = len(response_reminder_dict)
        response_reminder_dict.update({len(response_reminder_dict): self})

class PlayerResponses(GridLayout):
    player_responses = ObjectProperty(None)

class MyScrollView(ScrollView):

    # Game buttons are disabled at default. Buttons reactivate on scroll zero. 
    # Check for scroll zero on each scroll event.
    def is_zero(self):
        if self.scroll_y < self.convert_distance_to_scroll(0, 10)[1]:
            app = App.get_running_app()
            for item in app.root.ids.player_responses.children:
                item.disabled = False

class SceneScreen(FloatLayout):    
    global key
    display_text = StringProperty()
    
    def display_response_reminder(self, text):
        reminder = ResponseReminder(text=f"[b][i]\n{text}\n[/i][/b]")
        self.ids.main.add_widget(reminder)
        global reminder_widget_pos
        reminder_widget_pos = reminder.widget_pos

    def templating_sweep(self, text, templating_key=None):
        global key
        global interrupt_required
        global interrupt_tuple
        templating_target_stored = False
        templating_target = ""
        target = ""
        # function key to handle the templating of buttons correctly
        if templating_key:
            function_key = templating_key
        else:
            function_key = key
        # exit instantly if no templating is required
        if not "adlibs" in condict[function_key]:
            return text

        #begin templating
        templating_list = text.split(" ")
        for index, item in enumerate(templating_list):
            if item.startswith("@"):
                target = item  # set the target
                if not target[-1].isalpha():
                    target = item[:-1]
                adlibdict[target]["occurence"] += 1  # set and update occurence of adlib in templating key
                occurence = str(adlibdict[target]["occurence"]) # str here because my constructor requires that for some reason *shrug*
                target_adlib = adlibdict[target]["set to"] # set target adlib
                if target_adlib == None:
                    interrupt_required = True
                    if not templating_target_stored:
                        templating_target = target # This code flags the earliest required interrupt as the first to run
                        templating_target_stored = True  # Keeps the scene in order, yet allows templating to fully sweep target text
                else:
                    templating_list[index] = condict[function_key]["adlibs"][target_adlib][occurence]

        #reset occurences for next templating sweep
        for item in adlibdict:
            adlibdict[item]["occurence"] = 0
        template_complete = ""
        templating_target_stored = False #triggered early, but it just needed to be in the code so it's fine
        for item in templating_list:
            template_complete = template_complete + item + " "

        #returns either complete sentence, or partial sentence with global interrupt flag = True
        if not interrupt_required:
            return template_complete
        else:
            # template_complete is now a lie, but renaming it was confusing me too much
            # making a named tuple here, because dictionaries betrayed me
            pre_interrupt_string = template_complete.split("@")[0] + '...'
            return_index = template_complete.find(templating_target)
            post_interrupt_string = template_complete[return_index:]
            interrupt_tuple = Interrupt_Tuple(templating_target, post_interrupt_string)
            return pre_interrupt_string

    def update_display(self, string, continued=False):
        templated_string = self.templating_sweep(string)
        self.ids.main.add_widget(TextLabel(text=templated_string))   
        self.ids.mainscroll.scroll_y = 0
        if continued: #Only one of the following options execute
            pass

            # I MUST STILL CORRECT FOR CONTINUED STRINGS AFTER INTERUPT TO RUN CORRECTLY
            # IF I FORGET TO DO THIS THING, AND YOU SEE THIS COMMENT, FORGIVE ME FOR I HAVE SINNED

        original_scroll = self.ids.mainscroll.viewport_size[1] # y value of total avaliable viewport 
        Clock.schedule_once(lambda dt: self.correct_scroll(original_scroll), 0.005)

    def correct_scroll(self, original_scroll):
        # This function scheduled to encourage Kivy to fully update GUI, before then calculating where to scroll
        # Scrolls the view to the bottom of the player reminder, for the reader's viewing pleasure
        global reminder_widget_pos
        scroll_offset = response_reminder_dict[reminder_widget_pos].height
        corrected_scroll = original_scroll + scroll_offset
        current_scroll = self.ids.mainscroll.viewport_size[1]
        target_scroll = current_scroll - corrected_scroll
        self.ids.mainscroll.scroll_y = self.ids.mainscroll.convert_distance_to_scroll(0, target_scroll)[1]

    def generate_interrupt_buttons(self):
        global interrupt_tuple
        global interrupt_required
        
        target = interrupt_tuple.target
        blanket_return = interrupt_tuple.postreturn
        first_interrupt = adlibdict[target]["interrupt"]["first interrupt"]

        for item in adlibdict[target]["interrupt"]["player choices"]:
            self.ids.player_responses.add_widget(InterruptButton(
                pos_hint={'x': 0, 'center_y': 0.5},
                text=adlibdict[target]["interrupt"]["player choices"][item],
                set_interrupt = item,
                target = target,
                blanket_return = blanket_return,
                disabled=True
            ))
        interrupt_tuple = (None, None)
        interrupt_required = False
        self.update_display(first_interrupt)

    def generate_buttons(self):
        global key
        global interrupt_required
        self.ids.player_responses.clear_widgets() #clear the existing buttons

        # Below is the hard coded scenarios of types of buttons to make; Different ways the scene can progress
        # In the future this can be expanded to include any number of scene transformations
        if interrupt_required:
            self.generate_interrupt_buttons()
        elif type(condict[key]["points"]) == list: #Generate new buttons, each option from the key "points"
            
            for item in condict[key]["points"]:
                self.ids.player_responses.add_widget(FunkyButton(
                    pos_hint={'x': 0, 'center_y': 0.5},
                    text=self.templating_sweep(condict[item]["string"], item), 
                    button_key=condict[item]["points"][0], #I believe this [0] allows for variables in the future
                    disabled=True
                    ))
        elif not condict[key]["points"].endswith("()"): #The following line of code handles responses pointing to responses
            key = condict[key]["points"]
            self.update_display(condict[key]["string"], True) #True = continued string (used for adlibs mainly)
            self.generate_buttons() #this simply repeats this exact function; A feature required based on how my scene constructor was made
        else:
            self.ids.player_responses.add_widget(FinalButton(disabled=True))
      
    def start_scene(self):
        global key
        self.display_text = ""
        self.update_display(condict[key]["string"])
        self.generate_buttons()

class FirstButton(Button):

    # This button is largely a hold-over of where my UI began, and where it is now
    # I will refactor it out later on, but for now it's fine, though it does serve exactly one use
    global key

    def on_press(self):
        app = App.get_running_app()
        app.root.display_text = ""
        app.root.display_response_reminder(self.text)
        app.root.update_display(condict[key]["string"])
        app.root.generate_buttons()
        app.root.ids.mainscroll.scroll_y = 1

        for item in app.root.children[:]:
            if item.__class__ == TitleWindow:
                app.root.remove_widget(item)
        
class FurryFictionViewerApp(App):
    pass

if __name__ == '__main__':
    FurryFictionViewerApp().run()