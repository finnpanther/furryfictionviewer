from typing import List
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.properties import Clock
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
cafe_scene_dict = {
    "spring": {
        "morning": {
            "string": "It would be impossible not to find beauty in the pink blossoms you see, especially as they reflect in this early morning light.",
            "weather": {
                "yes": "A light morning drizzle coats the blossoms in just enough droplets of rain as to refract the light into all manners of color and splendor.",
                "no": "As you continue to look out you start to spot the spring pollenators, staying busy and getting the world ready for the new season of growth and bloom."}},
       "evening": {
            "string": "A smart looking couple is holding hands as they walk along a trail which passes by trees filled with young blossoms. One of the them is wearing a beautiful spring dress which neatly shapes their figure. The both of them are clearly enjoying a scenic walk in the spring weather. You are also enjoying it, as you look on in peace and quietude, sipping on your @drink.",
            "weather": {
                "yes": "One of them, the larger of the two, is holding an umbrella, to stave off what has become a fair amount of spring rain. It is hard to see if it is a man or woman, but they look every part a gentleman, gender norms be damned. You can't help but look on and wish for both roles in one - to hold the umbrella for a loved one, and also to be protected from the elements by your mate.",
                "no": "You notice each of the young couple has a drink of their own. One iced, one hot, and they seem so wrapped in conversation that, even if they did notice you looking on at them, they likely wouldn't have cared at all."}},
        "night": {
            "string": "The trees and bushes are beautiful this time of year. Perhaps moreso as the bright colors of the season reflect ever so gently in the night of a full moon. You take a sip of your @drink and sigh a contended sigh. Others in Furry Lounge might be up to all sorts of activities at this time of night. But you feel you could bask in this view until morning.",
            "weather": {
                "yes": "Part of the scene's beauty comes from the rain as it catches against rays of moonlight. In the distance you can see the branches of trees bob in the rain, and although you see no bugs or critters in the night, you can't help but imagine the rain will prove beneficial to all.",
                "no": "A gentle breeze sways the grass in beautiful time, as though coordinated to the backdrop of a midnight orchestra, heard by none but the trees, grass, and the moon herself."}}},
    "summer": {
        "morning": {
            "string": "It is early in the morning, yet thanks to summer sunlight hours the sun is already quite fully out. Yet the summer heat has not yet come in, as evidenced by morning walkers and joggers, unconcerned by the sun's occasionally hot rays.",
            "weather": {
                "yes": "There is, however, a breeze, which has just started to pick up. While not quite a heavy wind, you can definitely see gusts which agitate the fully green foliage and the fur and hair of the passerbys you see.",
                "no": "One jogger in particular sports short shorts, of the sort which warms your heart, and puts a comforting smile on your face. You take a drink of your @drink and try not to think about the passerby in to lewd of a fashion. Instead, you work to appreciate that shapely rear, framed perfectly by their swaying tail, for what it is: A perfect moment, and but a mere element to a more perfect day."}},
       "evening": {
            "string": "Even though it is now evening, the temperature has still not dropped down from its midday peak. You see a feline species basking topless in the summer sun, some sort of fit college student by the looks of it. At the same time, walking down the sidewalk, you spot some sort of rodent (a mink, perhaps?) nearly melting under the heat. You look on at the disparity between the two. You feel a little jealous of the basking cat, and perhaps wish you were out in the warm summer day as well. Although, more likely, you're quite content drinking your @drink from the safety of an air conditioned cafe.",
            "weather": {
                "yes": "However, there is some reprieve for them when a summer drizzle begins to fall. It comes seemingly from nowhere, and in a comical fashion, the two furries you can see seem to swap roles. You healthily drink your @drink and watch in a sort of delight, as the basking cat gets up and motions towards the sky, as though to say 'oh, come on, really!?' The mink, however, does an actual dance for joy. The rain revitalizes them. You can't help but smile in an odd way as you look on from your comfortable vantage point. Once again, you find yourself perhaps lucky not to be caught in the summer rain, although somehow you miss it at the same time.",
                "no": "You do notice, however, that the sky seems almost a startling blue. Without a cloud in sight, you see no doubt happy birds flying in whichever way. Somehow the scene gives you hope, although you'd be hard pressed to say exactly why."}},
        "night": {
            "string": "Thanks in part to school being out for the season, the summer night seems unusually crowded on the grounds at Furry Lounge. That, or perhaps there's some manner of event. But you see a fair number of furries of all types gathered around, lounging on the lawn, or taking a casual stroll with a partner or a friend. Through the pane of glass you can feel that the temperature is just right for a nighttime walk.",
            "weather": {
                "yes": "However, the scene is dirupted somewhat as a summer gale comes in. It is met with universal glee. The more conscientious of the furries you can see hold down their ruffling sundresses and skirts from blowing up in the wind. Others simply laugh, as the summer wind whips around their hair, fur, and tails. You get the impression that all of them, whether some of them are friends of many years, or if they are meeting each other now for the first time: It seems like everyone has become fast friends. You drink your @drink and watch on. You are jealous for them, and happy for them. Yet, being able to witness such a moment, you also feel happy for yourself, and rather contented by this rare scene at the window seat of the cafe in Furry Lounge.",
                "no": "Part of the joy is that, on the warm summer night, furries are dressed in all manner of scantily clad clothes. You see shirtless boys in gym shorts or bootyshorts, with girls wearing the same. You spot a few without tops, even, which to you comes across as bold. Up until you spot one couple in particular, brazenly streaking, yet in the most comfortable and casual of ways. Yet, nobody seems to mind. Part of you even wishes that you could join in."}}},
    "fall": {
        "morning": {
            "string": "The rays of early morning light stream through the colored leaves you can see on the grounds from your cozy seat by the window.",
            "weather": {
                "yes": "A light drizzle paints the leaves with a glimmer. Although you are comfortable secure behind the window of this cafe, you can still see hosts of critters and bugs, out for their morning activities, getting what they need to survive, either in spite of the rain or beacuse of it.",
                "no": "Even though you aren't even close to standing under a canopy of trees, you still seem to catch an amount of that dust in the air. It gives the sunlight a shimmer as the world slowly stirs to its autumn wake."}},
       "evening": {
            "string": "It is dusk now, the perfect time for students and businessmen to be walking home from school and work. You see some of them now, wearing smart jackets or scarves, some with messenger bags. But all of them have smiles on their faces.",
            "weather": {
                "yes": "The scene is marred only a little when a fall drizzle kicks in. Most of the furries continue on their walks without a care. Save for one furry in particular, a cute dog with floppy ears, wearing knee high socks and a short skirt. They have no bag, yet are carrying an arm full of books. You wish them luck as they start to scurry along, as the rain continues to pick up. Wherever it is they're headed, you hope they reach their destination soon, with their books at least reasonably dry.",
                "no": "You take note in particular of the trendier among them. These are the furries with layers of autumn clothing, an eye for fashion, and the happy demeanor which comes from an outfit well executed. If you didn't know better you'd think they were even in competion with each other, to see who could enjoy the autumn scene more. Yet, thanks to your vantage from this cafe window, and aided by your @drink, you can't help but feel that maybe you're the one who enjoys the scene the most."}},
        "night": {
            "string": "The night outside looks still and quiet. In a way it looks almost spooky, with how the multi-colored leaves ever so dimly reflect the moonlight.",
            "weather": {
                "yes": "Then it gets spookier when the wind picks up. At first you could see the branches of the trees start to wave in the wind. With a gasp you look on as the wind picks up in a big way. A powerful gust wipes away swaths of leaves directly from their branches. Leaves which had collected on the ground are also picked up in the wind. For the span of a moment you lay witness to a stunning dance of nature, as colors swirl and fly in the wind. Aided by the atmospheric moonlight, the night seems somehow blessed and cursed all at once. It seems like either Mother Nature is playing around among her own creation, or that a witch is casting a spell. You aren't sure which of the two you prefer.",
                "no": "Then, in a rare moment of silence in the cafe around you, you can hear the outside world. Yet, in the most peculiar of ways, you pointedly make out not a single sound. No crickets chirp, no animals rustle around. There isn't the hint of a breeze. Only color and moonlight, and deep textures, as though this window had instead become a brilliant painting. Then, as you shift around in your seat, you catch a small glimpse of your own reflection. Yet, rather than taking you out of the scene, it somehow adds to the beauty of the painting. A moment more perfectly captured than you thought was possible."}}},
"winter": {
        "morning": {
            "string": "The snow which fell overnight glistens as little crystals of snow catch against the morning rays of sun. It is still early in the day, so the blanket of snow across the grounds of Furry Lounge remains unbroken. The scene brings to you peace and serenity as you sip on your @drink.",
            "weather": {
                "yes": "Part of the serenity you feel comes from the snowfall. It is gentle, but the snowflakes are fat, fat, fat. If only the windows of the cafe were open so you could reach out your hand and catch one. But they are as beautiful to look at as they would be to hold, and the scene enchants you so much that you wouldn't disrupt it for the world.",
                "no": "As you watch on, you notice a bunny hopping along through the snow. A normal bunny, not an anthropomorphic one. Although the image makes you giggle, and you almost snort some of your @drink as you imagine a lagomorph taking a morning bound through the fresh layer of snow."}},
       "evening": {
            "string": "This is the time of evening when the young families are out and about with their cubs. Although this view of the grounds surrounding Furry Lounge has no hills for sledding, you still see some cubs running and playing in the previously unbroken field of snow. Through the frosted window you can hear their screams of laughter, although faintly enough as not to disturb your serenity as you sit on your @drink.",
            "weather": {
                "yes": "The sounds of mirth coming from the outside world is further dampened by steady snowfall. It also coats your vision of the outside world in a gentle haze. It helps to direct your attention away from the outside world, and into the cafe around you. It is hard to quantify, but the cafe itself seems cozy as well. Down to the other furries you see inside, some of whom are window watching as surely as you are. Then you catch sight of the baristas, all of whom seem to be in the spirit of the winter season. It's a cozy time of year. In this moment in particular, you can't help but feel like everyone has found a cozy place to call their own. You consider yourself lucky to be part of it.",
                "no": "Along the cute families you see one young couple, neatly bundled up against the cold, rolling up two balls of snow. You recognize what they're doing instantly, and it brings a smile to your face. Sure enough, the couple is smiling as well, as finally they bring their balls of snow together, and roll one atop the other. The snowman is becoming made. Except, the snow must be too powdery this evening, because the bottom snowball collapses under the weight. One of the furries busts up into laughter immediately, and you can't help but giggle along with them, even as their mate looks crestfallen. They perk up pretty quickly, however, when they tackle their partner into the snow. It's a beautiful scene, and you wouldn't change it for anything. Although, part of you does wish that they could have made their snowman in peace."}},
        "night": {
            "string": "The outside world is quiet and myserious, yet also majestic. Even through the closed window you swear you can beathe in the crisp air of a quiet winter night.",
            "weather": {
                "yes": "The scene is all the more quiet for the heavy snowfall just on the other side of this pane of glass. You can't even make out the trees across the field, which are ordinarily so incredibly clear. All you see if a fog of snowfall, maybe not quite a blizzard, but it comes damn close. You can't help but think that if this kept up all night, then there would hardly be a Furry Lounge remaining when the sun came back up.",
                "no": "It looks impossibly cold, and you count yourself lucky to be inside. You sip on your @drink and shiver on just imagining the temperature outside. Even the trees look cold, although of course they do, being so naked this late in the year. Except for a few fir trees you spot, which were smart enough to bring some winter clothes of their own."}}},
    "thinking about": {
        "life": "As you look on, you think about life and the nature of things. Before long the scene fades away, as you stare off into the middle distance, trying to make sense of it all. Sometimes when you feel this way, it comes up as an urgent rush stemming from the soul. As though the moment was too perfect not to seize in the biggest way imaginable. Right now, however, your thoughts about life come as a serene wave. As though you were standing on the shore of existence, and the question of life's meaning is the tide which tickles against your feet in the sand.\nWho are you? What is your place in things? And what are you doing here? Not to mention, what sort of plan do you have moving forward?\nThese are the questions which flow through your mind. Yet, as each question comes into focus, so too do they flow away. This moment is too nebulous, and too pure, to hold on to any single one. Instead you take a deep, contented breath in the experience of it all. You decide that maybe we make our own meaning in this world. And that maybe it's moments like these which have the most meaning of all.",
        "love": "In some versions of this moment, you see other furries outside, be they a family, a couple, or single. And when looking on at a couple, be it in this moment or a version of it, you can't help but feel a tremendous sense of... loss? Or, is it joy? Its a wistfulness in any case, and in the most melancholy of ways. You're happy for the couples you see, the ones who are so clearly in love. They are happy to have found each other. Looking on at them, they look actually jubilant to your eyes. It's a good look on them, you have to admit. And behind it there's a mask of sadness which you just can't explain away. You shake your head out of the thoughts, and hide what might be a growing tear behind a purposeful drink of your @drink. Why are you sad so suddenly, on imagining and dwelling on something which brings so much joy, both to others, and even to yourself? Then, with a deep breath and a heavy sigh, the feeling comes to pass. Love is good. And it hurts, too, sometimes in painful ways. But sometimes in the best of ways as well. You wish the best of luck for the couples you see in the scene beyond you, as surely as you wish for the best for yourself. You chide yourself, and stare wistfully into your @drink. What do they put in these things, anyway?",
        "nothing": "You take the deepest of contented breaths. Sometimes it's harda to be alone with your thoughts. Those are the moments you seek distraction, and Lord knows you'll find it. Sometimes you scrounge for your phone, or so desire to scroll to stave off a nameless dread. But now, none of that urgency comes to you. In fact, it seems that nothing does. What you feel is simple serenity, a stillness and peace of mind which so rarely comes to you. And now that it's here, you grab at it. Or, that's what someone experiencing turbulence within themselves would say. But in this moment you acknowledge that there is no turbulence, and peace is not something you grab. Peace simply is. As are you, and any of the furries you spot through the window, or any of the ones you might run into in Furry Lounge. It's a stillness of mind nearly unlike any you've felt before. And so, you feel it. And allow yourself to feel it. And time passes, and you continue to breathe and exist, and even bask, in the beingness of it all.",
        "furry lounge": "As you take in the scene through your window seat at this cafe, your mind turns to the cafe, as well as the establishment it is a part of. Furry Lounge is vast, and you can't help but feel that you've explored only a fraction of what it has to hold. Some bill it as a den of sodomy, but in a moment like this you can't help but laugh at how outrageous that sounds. When taking in a peacful moment like this, a beautiful scene, with a delicious cup of @drink to speed you along your way - there just couldn't be a more perfect place to be. And sure, you'd like to find someone here to spend some quality time with. But, you reflect on how important it is to also take times like these for yourself. Furry Lounge, after all, isn't going anywhere anytime soon. So, too, are you free to stay as long as you like, either in Furry Lounge, or even in this very seat. You could continue to bask in this scene for as long as you'd like, and looking on at the beauty just on the other side of the window, you begin to think that you just might."
    }}
door_key_found = False
interrupt_required = False
interrupt_dictionary = {}
interrupt_tuple = Interrupt_Tuple(None, None)

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
    pass
class Porn(Image):
    pass

class SceneScreen(FloatLayout):    
    global key
    display_text = StringProperty()
    

    ########


    def display_response_reminder(self, text):
        self.ids.main.add_widget(ResponseReminder(text=text))


    ########


        
    def clear_global_interrupt_variables(self):
        global interrupt_dictionary
        global interrupt_required

        interrupt_dictionary.clear()
        interrupt_required = False

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
        current_display = self.display_text
        templated_string = self.templating_sweep(string)

        if continued: #Only one of the following options execute
            self.display_text = current_display + ' ' + templated_string #Adds the continuation seamlessly
            return
        self.display_text = current_display + '\n    ' + templated_string #Adds space and the appropriate text
        self.ids.mainscroll.scroll_y = 0

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
        app.root.update_display(condict[key]["string"])
        app.root.generate_buttons()
        for item in app.root.children[:]:
            if item.__class__ == TitleWindow:
                app.root.remove_widget(item)


        
class FurryFictionViewerApp(App):
    pass

if __name__ == '__main__':
    FurryFictionViewerApp().run()