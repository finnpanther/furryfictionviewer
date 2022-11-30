'''
Unfactored WIP code for additional game elements
Original Code written entirely by Finn Panther
'''


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import inspect

operational_tuple = ("verb", "noun")

introduction_text = StringProperty("You wake up a little groggy, a little unsure of who you are. Interestingly, that sensation fades rather quickly, because I didn't think it would be interesting for this test narrative to just have the player be, you know. Groggy. You still don't know who you are, though. Nor do you know where you are. You do have a suspicion that you can 'look around', though, or even press the HELP button for more information.")
place_dict = {}
gs = {} #game state dictionary, for storing the state of game objects

class Place():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.thing_dict = {}        
        self.verb_dict = {"go to": self.goto, "look at": self.look_at} #Some additional verbs handled at text validation
        place_dict.update({self.name: self})
        self.verb_list = ["go to", "look at", "look around", "look at everything"]

    def goto(self, noun):
        global main
        try:
            main = place_dict[noun]
            ud(f"You are at the {main.name}. {main.description}")
            ud(self.display_interactables())
        except:
            update_display("Something went wrong, it seems you cannot go to that.")

    def look_at(self, noun):
        __repr__ = "LOOK AT ME BABY!"
        try:
            update_display(self.thing_dict[noun].description)
        except:
            update_display("You can't look at that.")

    def look_around(self):
        try:
            ud(f"You are at the {main.name}. {main.description}")
            ud(main.display_interactables())
        except:
            ud("It seems like something went wrong.")

    def look_at_everything(self):
        ud(main.description)
        for item in main.thing_dict:
            ud(f"There is a {item}. {main.thing_dict[item].description}")

    def display_interactables(self):
        if main.thing_dict == {}:
            return "There are no interactables here."
        else:
            return f"You can interact with: {', '.join(main.thing_dict)}"

class Thing():
    def __init__(self, parent, name, description):
        self.parent = parent
        self.name = name
        self.description = description
        parent.thing_dict.update({self.name: self})
  
class Developer_Room(Place):

    def look_under(self, noun):
        if not noun == "bed":
            ud("I didn't understand that.")
            return
        ud("You hope to find secrets under the bed. As though a skeleton hidden in the closet, you have a hope that this developer room holds more secrets than it lets on. It is with tremendous joy that you get on all fours, and peer underneath the bed. You can't help but wonder at what wonders you might find!\n... unfortunately, you find nothing there. Not even a speck of dust. It's dimly lit, although in sort of an artificial way. As though even the lighting mechanics for this room haven't yet been entirely dialed in. Somehow, the experience makes you feel like this room is even more cheap than before. You do, however, deeply admire the dark grey pegs which hold up the bed.\nYou get the impression that it would be lovely to crawl under.")
    def crawl_under(self, noun):
        if not noun == "bed":
            ud("I didn't understand that.")
            return
        ud("Very well. You attempt to crawl under the bed. However, with just one foot of clearance off the ground, you just can't make your way underneath. Try as you might, you can barely squish your head into the space. It's an uncomfortable fit, one which fills you with joy as having pulled it off, as well as a slight terror when you imagine yourself unable to pull your head back out. Thankfully, this early in the development cycle, there isn't a way to actually get your head stuck. The developer desperately would like for you to have that option, truly, he would. But this game is one of baby steps, and that sort of advanced functionality is going to have to wait for another day.\nSo it is with a tremendous regret that you pull your head out from underneath the bed. Perhaps you can become stuck another day. But this is not that day.")

    def __init__(self, name, description):
        super().__init__(name, description)
        self.bed = Thing(self, "bed", "The bed looks like a developer bed. As in, it has the appearance of an unfinished game asset. It's a grey box, raised perhaps a foot above the floor with the assistance of four, darker grey pegs. You can only hope that later in the development cycle of the game that they finish this texture, because honestly it just seems sort of lazy. But, then again, this is the early access for the early access, so you aren't really sure what else you might have expected to find.")
        self.dresser = Thing(self, "dresser", "It's a dresser.")
        self.lamp = Thing(self, "lamp", "It is a lamp, which sits atop the dresser.")
        self.closet = Thing(self, "closet", "It is a closet, with two accordion style doors.")

developer_room = Developer_Room("developer room", "It looks like a developer room. The ceiling, floor, and walls are all a nondescript shade of grey, and large, black gridlines line each surface. You wager that they're spaced exactly one meter apart, as though the game developers wanted the visual aid for how large the room was. Although, speaking of developers, you do wonder why the maker of this game decided for his first ever scene to be a literal devloper room. Talk about uninspired.")


class Developer_Room_Closet(Place):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.shirt = Thing(self, "shirt", "There is a shirt, and it looks wonderful.")

gs = {"developer room": {}}

lgs = gs["developer room"]
developer_room_closet = Developer_Room_Closet("closet", "It has two large, accordion style doors. They are white, with slats to air out whatever secrets lay inside. The slats angle down, of course, so you cannot see what is inside. Right now is it closed. Until the developer expands on the feature, it will always be closed.")

main = developer_room

def confirm_valid_input(text):
    global operational_tuple
    verb_count = 0
    noun_count = 0
    noun = ""
    verb = ""
    for item in main.verb_list:
        if item in text:
            verb = item
            verb_count += 1
    for item in main.thing_dict:
        if item in text:
            noun = item
            noun_count += 1
    if verb == "look around":
        return "look around"
    
    if verb == "look at everything":
        return "look at everything"

    if verb_count == 1 and noun_count == 1:
        operational_tuple = (verb, noun)
        return True
    else:
        return False

#Kivy Stuff
def update_display(text):

    app = App.get_running_app()
                   #current screen         #dictionary of ids in current screen
    display_text = app.root.current_screen.ids.game_display.text
    display_text = display_text + "\n" + text
    app.root.current_screen.ids.game_display.text = display_text + "\n"
ud = update_display

class GameWindow(Screen):
    introduction_text = introduction_text

    def on_text_validate(self):
        player_text = self.ids.text_input.text
        self.ids.text_input.text = ""


        #UNFUCK THIS LATER
        if confirm_valid_input(player_text) == "look around":
            ud("You decide to look around.")



            #LETS GET FUCKY
            for item in inspect.getmembers(developer_room):
                print('\n\n\n\n INSPECTING ' + item[0])
                try:
                    print(str(inspect.getmembers(getattr(developer_room, item[0]))))
                except:
                    pass
            # method_list = [func for func in dir(developer_room) if callable(getattr(developer_room, func)) and not func.startswith("__")]

            # for item in method_list:
            #     ud("Trying to " + str(item) + " the bed")
            #     try:
            #         getattr(developer_room, item)("bed")
            #     except:
            #         ud("Unable to do that.")
            #         pass

            #DONE BEING FUCKY NOW!





            main.look_around()
            return
        
        if confirm_valid_input(player_text) == "look at everything":
            ud("You decide to look at everything.")
            main.look_at_everything()
            return

        if not confirm_valid_input(player_text):
            update_display("Something went wrong.")
            return
        
        global operational_tuple
        verb = operational_tuple[0]
        noun = operational_tuple[1]
        update_display(f"You decide to {verb} the {noun}.\n")
        main.verb_dict[verb](noun)

class SceneWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass
class GameViewerApp(App):
    pass
GameViewerApp().run()