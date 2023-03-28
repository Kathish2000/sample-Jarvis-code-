from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.snackbar import Snackbar
from gtts import gTTS
import os
import wikipedia
import subprocess
import pywhatkit
import plyer

wikipedia.set_lang('en')

class MainScreen(FloatLayout):
    theme_cls = ThemeManager()

    input_text = ObjectProperty()
    output_text = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.request_permission()

    def request_permission(self):
        if not plyer.check_permission('android.permission.RECORD_AUDIO'):
            plyer.request_permission('android.permission.RECORD_AUDIO')

    def listen(self):
        subprocess.Popen(['am', 'start', '-a', 'android.intent.action.VOICE_COMMAND'])
        Clock.schedule_once(self.get_input, 1)

    def get_input(self, dt):
        try:
            self.input_text.text = self.ids['output_label'].text
        except KeyError:
            pass
        Clock.schedule_once(self.respond, 2)

    def respond(self, dt):
        input_text = self.input_text.text.lower()
        self.output_text.text = f"User: {input_text}"
        if 'wikipedia' in input_text:
            topic = input_text.replace('wikipedia', '')
            try:
                summary = wikipedia.summary(topic, sentences=2)
                self.output_text.text += f"\nJarvis: {summary}"
                language = 'en'
                myobj = gTTS(text=summary, lang=language, slow=False)
                myobj.save("welcome.mp3")
                os.system("mpg321 welcome.mp3")
            except wikipedia.exceptions.DisambiguationError as e:
                self.output_text.text += f"\nJarvis: {e}"
                language = 'en'
                myobj = gTTS(text=e, lang=language, slow=False)
                myobj.save("welcome.mp3")
                os.system("mpg321 welcome.mp3")
        elif 'play' in input_text:
            topic = input_text.replace('play', '')
            pywhatkit.playonyt(topic)
            self.output_text.text += f"\nJarvis: Playing {topic} on YouTube."
            language = 'en'
            myobj = gTTS(text=f"Playing {topic} on YouTube.", lang=language, slow=False)
            myobj.save("welcome.mp3")
            os.system("mpg321 welcome.mp3")
        else:
            self.output_text.text += f"\nJarvis: Sorry, I did not understand that."
            language = 'en'
            myobj = gTTS(text="Sorry, I did not understand that.", lang=language, slow=False)
            myobj.save("welcome.mp3")
            os.system("mpg321 welcome.mp3")

        self.input_text.text = ''

class JarvisApp(App):
    theme_cls = ThemeManager()

    def build(self):
        Builder.load_file('jarvis.kv')
        return MainScreen()

if __name__ == '__main__':
    JarvisApp().run()
