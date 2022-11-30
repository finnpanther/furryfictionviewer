'''
Original Code written entirely by Finn Panther
'''

from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from collections import namedtuple

#TODO Allow dynamic file selection as story content grows
import json
with open('the_first_story.json', 'r') as f:
    condict = json.load(f)
with open('adlib_dictionary.json', 'r') as f:
    adlibdict = json.load(f)

Interrupt_Tuple = namedtuple("InterruptTuple", "target postreturn") # @size, huge, "... his dick is so massive!"
key = '0'
interrupt_required = False
interrupt_tuple = Interrupt_Tuple(None, None)
reminder_widget_pos = 0
response_reminder_dict = {}
reset_text = "[size=38]The game will now reset.\nEnjoy playing the next round![/size]"

#TODO Convert labels into static title image
class TitlePage1(Label):
    pass
class TitlePage2(Label):
    pass
class TitlePage3(Label):
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

        with open('the_first_story.json', 'r') as f:
            condict = json.load(f)
        with open('adlib_dictionary.json', 'r') as f:
            adlibdict = json.load(f)

        #TODO: 
        # Make fresh restart (clear game screen)
        # Correct scroll pos dynamically

        app= App.get_running_app()
        app.root.display_text = ''
        app.root.update_display(reset_text)
        app.root.ids.main.add_widget(TitlePage1())
        app.root.ids.main.add_widget(TitlePage2())
        app.root.update_display(condict[key]["string"])
        app.root.generate_buttons()
        app.root.ids.mainscroll.scroll_y = .05

class TextLabel(Label):
    pass

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

    # Game buttons are disabled at default.
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
        # Handles occurences to replace adlibs in sequence
        # Isolates required interrupt on first encounter with adlib
        # Coded this way to account for branching narratives
        global key
        global interrupt_required
        global interrupt_tuple
        templating_target_stored = False
        templating_target = ""
        target = ""

        if templating_key:
            function_key = templating_key
        else:
            function_key = key
        if not "adlibs" in condict[function_key]:
            return text

        templating_list = text.split(" ")
        for index, item in enumerate(templating_list):
            if item.startswith("@"):
                target = item 
                if not target[-1].isalpha():
                    target = item[:-1]
                adlibdict[target]["occurence"] += 1 
                occurence = str(adlibdict[target]["occurence"])
                target_adlib = adlibdict[target]["set to"]
                if target_adlib == None:
                    interrupt_required = True
                    if not templating_target_stored:
                        templating_target = target
                        templating_target_stored = True
                else:
                    templating_list[index] = condict[function_key]["adlibs"][target_adlib][occurence]

        for item in adlibdict:
            adlibdict[item]["occurence"] = 0
        template_complete = ""
        templating_target_stored = False
        for item in templating_list:
            template_complete = template_complete + item + " "

        if not interrupt_required:
            return template_complete
        else:
            pre_interrupt_string = template_complete.split("@")[0] + '...'
            return_index = template_complete.find(templating_target)
            post_interrupt_string = template_complete[return_index:]
            interrupt_tuple = Interrupt_Tuple(templating_target, post_interrupt_string)
            return pre_interrupt_string

    def update_display(self, string, continued=False):
        templated_string = self.templating_sweep(string)
        
        if string == reset_text:
            new_widget = TextLabel(text=templated_string, halign='center')
        else:
            new_widget = TextLabel(text=templated_string)
        self.ids.main.add_widget(new_widget)   
        self.ids.mainscroll.scroll_y = 0
        if continued:
            pass

            # I MUST STILL CORRECT FOR CONTINUED STRINGS AFTER INTERUPT TO RUN CORRECTLY
            # IF I FORGET TO DO THIS THING, AND YOU SEE THIS COMMENT, FORGIVE ME FOR I HAVE SINNED

        original_scroll = self.ids.mainscroll.viewport_size[1] # y value of total avaliable viewport 
        Clock.schedule_once(lambda dt: self.correct_scroll(original_scroll), 0.01)

    def correct_scroll(self, original_scroll):
        # This function scheduled to encourage Kivy to first fully update GUI
        # Scrolls the view to the bottom of the player reminder
 
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
        self.ids.player_responses.clear_widgets()

        if interrupt_required:
            self.generate_interrupt_buttons()

        elif type(condict[key]["points"]) == list:
            for item in condict[key]["points"]:
                self.ids.player_responses.add_widget(FunkyButton(
                    pos_hint={'x': 0, 'center_y': 0.5},
                    text=self.templating_sweep(condict[item]["string"], item), 
                    button_key=condict[item]["points"][0], #This [0] allows for variables in the future
                    disabled=True
                    ))

        # The following block updates display, then repeats this exact function 
        # A feature required based on how my scene constructor was made
        elif not condict[key]["points"].endswith("()"): 
            key = condict[key]["points"]
            self.update_display(condict[key]["string"], True) 
            self.generate_buttons() 

        else:
            self.ids.player_responses.add_widget(FinalButton(disabled=True))

    def start_scene(self):
        global key
        self.display_text = ""
        self.update_display(condict[key]["string"])
        self.generate_buttons()

class FirstButton(Button):
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