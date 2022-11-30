from typing import List
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from collections import namedtuple
from kivy.uix.image import Image
from kivy.uix.label import Label
import inspect
from time import sleep

import json
with open('rodney/introduction.json', 'r') as f:
    condict = json.load(f)
with open('rodney/adlib_dictionary.json', 'r') as f:
    adlibdict = json.load(f)

Interrupt_Tuple = namedtuple("InterruptTuple", "target postreturn") #@size, huge, "... his dick is so massive!"
blank_condict = condict.copy()
blank_adlibdict = adlibdict.copy()
key = '0'
help_button_pressed = False
door_key_found = False
interrupt_required = False
interrupt_dictionary = {}
interrupt_tuple = Interrupt_Tuple(None, None)
reminder_widget_pos = 0
response_reminder_dict = {}

def boundless_void():
    pass
def closet():
    pass
def test_room():
    test_room_dict = {
        "look at": "You can't look at the room, you are already in it.",
        "description": "The room you are in is fine, if not a little unexpected. In particular, this is clearly a fantasy world. Anything could happen. With the magic of literature, you could be standing in any room imaginable. Oh, just imagine, the places you could be!\n... so why is this so clearly textured as a test room?\nI mean, for real. The walls, floor, and ceiling are all grey and covered in large gridlines, as though a developer would use them as roadmap to determine how large the room is. It isn't fair to say the walls are tiled, even, although they do look that way. To call them tiled brings to mind a manner of actual texture. As though the room was made of plates, bound together.\nBut no. This is just an uninspirng, grey room, with some lines marking a grid. In honesty, it almost feels a little lazy. Did the author seriously decide to write an unfinished test room, in order to test his... well, room?\nYou decide not to think too hard about it, and instead continue to look around, to see if there are any interactables.",
        "interactables": ["bed", "dresser", "closet", "door"],
        "bed": {
            "look at": "The bed, like everythign else in this room, is as yet untextured. You can tell it's a bed, though, because printed on it is the word, 'BED'. It is grey as well, although an off shade from the walls, floor, and ceiling, which all share the same tone. There is also a red strip across the bed, towards the top of it. Just above it are two, neatly labeled squares, each identified with large text reading 'PILLOW'. So, at least some attention to detail was paid.\nThe stripe across the bed actually gives a fair impression that it's supposed to be a blanket, or at least, that it would become one, later in the game's development cycle. In all, it gives you a strange suspicion that you aren't supposed to be here. It's an uncanny room to be in. This bed is uncanny.\nYou get more uncomfortable with it the more you think about it. So you try not to think about it too hard. Easier said than done.",
            "interactables": ["pillow", "blanket", "pillows"],
            "pillows": "Try looking at just one pillow.",
            #TODO WORK ON PILLOW
            "pillow": "WORKONTHIS",
            "blanket": {
                "look at": "The 'blanket' is checkered, like the rest of the room (annd each object inside it), although the checker pattern is more tight than the large, sweeping squares which make up the room.\nYou feel a sense of longing towards the bed. It seems like it would be quite inviting, to turn the blanket down, and to crawl inside and nestle up, warm and cozy. But unfortunately, this is just a test room. This is just a test blanket. You cannot crawl into it, you cannot get cozy.\nPerhaps someday you will be able to. But this is not that day.",
                "crawl into": "I literally just said that you can't do that. Come on, man. Don't be like that.",
                "be like that": "You ignore the game developer and crawl into the bed anyway. Amazingly, after a little bit of prying, you are actually able to life up the blanket, and crawl inside all the same!\nThat is, you would do that, if opening hte blanket didn't unleash a furious wormhole which sucks you up and tosses you into a boundless void.(1)",
                1: boundless_void()
            }
        },
        "dresser": {
            "look at": "The dresser is, honestly, amazing. It's checkered and non-textured like everything else in this room. But the markings on this dresser in particular are extravagant. The design artist behind it clearly took pride in his job. And looking at this dresser nnow, you can't help but take al ittle bride in him back.\nSomewhere out there, in this grand world, a junior developer among junior developers smiles. Your love of his dresser empowers him, and lets him know that he is on the right path. If he can make a dresser as great as this, then surely he can move mountains and tame seas, for the world must surely belong to him. Such is the power of the dresser. Such is the power of your belief.\n... there is nothing additionally interactable about this dresser. You wonder why the developer put it in."
        },
        "closet": {
            "look at": "There isn't anything terribly special about the closet by looking at it. It's just two large, accordion looking doors which have the text 'CLOSET' printed across the both of them. It does, however, look like a delightful thing to go to.",
            "go to": closet()
        },
        "door": {
            "look at": "The door, interestingly enough, is not labeled as a door. But it is the most clearly detailed object in the room. For it looks like a door. An honest to god door. It's brown, and it's got those weird, kind of wanna-be fancy grooves in it, as to mark it as an outside door. It's unmistakable, really. You get excited at the prospect of getting out of this weird, unfinished game space.\nThere is no window on this door to look out from, but there is a door handle.",
            "interactables": ["door handle"],
            "door handle": {
                "boolean": door_key_found,
                True: "The door seems like it is locked. Good think you have the key for it!",
                False: "The door is locked, unfortunately. You sure hope the key is somewhere inside this incomplete room. It'd be a major bummer if there wasn't any way out.",
            }
        }
    }

def cafe_scene():
    pass

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
        

class Porn(Image):
    pass

class SceneScreen(FloatLayout):    
    global key
    display_text = StringProperty()
    

    ########


    def display_response_reminder(self, text):

        reminder = ResponseReminder(text=f"[b][i]\n{text}\n[/i][/b]")
        self.ids.main.add_widget(reminder)

        global reminder_widget_pos
        reminder_widget_pos = reminder.widget_pos






    ########


    def templating_sweep(self, text, templating_key=None):
        global key
        global interrupt_required
        global interrupt_tuple
        templating_target_stored = False
        templating_target = ""
        target = ""
        #function ey to handle the templating of buttons correctly
        if templating_key:
            function_key = templating_key
        else:
            function_key = key
        #exit instantly if no templating is required
        if not "adlibs" in condict[function_key]:
            return text

        #begin templating
        templating_list = text.split(" ")

        for index, item in enumerate(templating_list):
            if item.startswith("@"):
                #set the target
                target = item
                if not target[-1].isalpha():
                    target = item[:-1]
                #set and update occurence
                adlibdict[target]["occurence"] += 1 
                occurence = str(adlibdict[target]["occurence"]) #str here because my constructor requires that for some reason *shrug*
                #set target adlib
                #SLOT IN INTERRUPT TO THIS LOCATION!
                target_adlib = adlibdict[target]["set to"]

                if target_adlib == None:
                    interrupt_required = True
                    if not templating_target_stored:
                        templating_target = target
                        templating_target_stored = True
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
            #template_complete is now a lie, but renaming it was confusing me too much
            #making a named tuple here, because dictionaries betrayed me
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

        original_scroll = self.ids.mainscroll.viewport_size[1] # y value of total avaliable viewport 
        Clock.schedule_once(lambda dt: self.correct_scroll(original_scroll), 0.005)


    def correct_scroll(self, original_scroll):
        global reminder_widget_pos

        scroll_offset = response_reminder_dict[reminder_widget_pos].height
        corrected_scroll = original_scroll + scroll_offset
        current_scroll = self.ids.mainscroll.viewport_size[1]

        target_scroll = current_scroll - corrected_scroll
        self.ids.mainscroll.scroll_y = self.ids.mainscroll.convert_distance_to_scroll(0, target_scroll)[1]
    










    def generate_interrupt_buttons(self):
        # {"original incomplete template": incomplete_template,
        # "pre interrupt": pre_interrupt_string,
        # "post interrupt": "... " + post_interrupt_string})
        # Also features "interrupt target": adlibdict[target]}
        global interrupt_tuple
        global interrupt_required
        
        target = interrupt_tuple.target
        blanket_return = interrupt_tuple.postreturn
        first_interrupt = adlibdict[target]["interrupt"]["first interrupt"]

        for item in adlibdict[target]["interrupt"]["player choices"]:
            self.ids.player_responses.add_widget(InterruptButton(
                text=adlibdict[target]["interrupt"]["player choices"][item],
                set_interrupt = item,
                target = target,
                blanket_return = blanket_return
            ))

        interrupt_tuple = (None, None)
        interrupt_required = False
        self.update_display(first_interrupt)

    def generate_buttons(self):

        print(self.ids)




        global key
        global interrupt_required
        self.ids.player_responses.clear_widgets() #clear the existing buttons

        if interrupt_required:
            self.generate_interrupt_buttons()

        elif type(condict[key]["points"]) == list: #Generate new buttons, each option from the key "points"
            for item in condict[key]["points"]:
                self.ids.player_responses.add_widget(FunkyButton(
                    pos_hint={'x': 0, 'center_y': 0.5},
                    text=self.templating_sweep(condict[item]["string"], item), 
                    button_key=condict[item]["points"][0] #I believe this [0] allows for variables in the future
                    ))
        elif not condict[key]["points"].endswith("()"): #The following line of code handles responses pointing to responses
            key = condict[key]["points"]
            self.update_display(condict[key]["string"], True) #True = continued string (used for adlibs mainly)
            self.generate_buttons() #this simply repeats this exact function
        else:
            self.ids.player_responses.add_widget(FinalButton())
      
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
        for item in app.root.children[:]:
            if item.__class__ == TitleWindow:
                app.root.remove_widget(item)


        
class FurryFictionViewerApp(App):
    pass

if __name__ == '__main__':
    FurryFictionViewerApp().run()