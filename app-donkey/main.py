from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import kivy.clock
import paho.mqtt.client as mqtt
import webbrowser
import threading

def split_and_send(final_path):
    print(final_path)
    # Delete Path:
    final_path = final_path[6:]

    # Change to list
    final_path = final_path.split(sep=',')

    #Delete last empty elem in list
    final_path = final_path[:-1]

    #Delete empty spaces in every elem in list
    for i in range(len(final_path)):
        final_path[i] = final_path[i][1:]

    # setup client and broker
    # mqttBroker = "192.168.1.113"
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("User")
    client.connect(mqttBroker)

    # send START command - it's necessaery due to
    # design of functions in robot
    command = "START"
    client.publish("COMMANDS", command)
    print(str(command) + " command has been send")

    for command in final_path:
        command = command.split(sep=' ')[1]
        client.publish("COMMANDS", command)
        print("Just published " + str(command) + " to Topic COMMANDS")

    command = "STOP"
    client.publish("COMMANDS", command)
    print(str(command) + " command has been send")


class MainWindow(Screen):
    def travel_default_path(self, root):
        default_path = 'Path:  Move 420, Rotate L, Move 333, Move 333,' \
                             ' Rotate R, Rotate R, Move 100, Move 420, Rotate L, '

        split_and_send(default_path)


class LearnPath(Screen):
    def send_velocity(self):
        velocity = self.ids.my_slider.value

        # setup client and broker
        # mqttBroker = "192.168.1.113"
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("User")
        client.connect(mqttBroker)

        # send START command - it's necessaery due to
        # design of functions in robot
        command = "VEL=" + str(int(velocity))
        client.publish("COMMANDS", command)
        print(str(command) + " command has been send")

class AboutDonkey1(Screen):
    def github_button_on(self):
        self.ids.github_button_img.source = 'img/GitHub-Mark-Light-120px-plus_pressed.png'

    def github_button_off(self):
        self.ids.github_button_img.source = 'img/GitHub-Mark-Light-120px-plus.png'
        webbrowser.open('https://github.com/kmotyka00/Autonomous-Donkey')

class AboutDonkey2(Screen):
    pass

class ChoosePath(Screen):
    pass

class GridTop(GridLayout):
    pass

class Calculator(BoxLayout):
    def clear(self):
        self.ids.calc_input.text = '0'

    def remove(self):
        if len(self.ids.calc_input.text) == 1:
            self.ids.calc_input.text = '0'
        else:
            self.ids.calc_input.text = self.ids.calc_input.text[:-1]


    def rotation_button(self, angle):
        self.ids.calc_input.text = str(angle)

    def number_button_press(self, number):
        prior = self.ids.calc_input.text

        if prior == '0':
            self.ids.calc_input.text = str(number)
        else:
            self.ids.calc_input.text += str(number)

    def send_msg(self, root, operation):
        value = self.ids.calc_input.text
        self.ids.calc_input.text = '0'

        prior = root.ids.path.text
        if operation == 'move':
            root.ids.path.text = f'{prior} Move {value},'
        elif operation == 'rotate':
            root.ids.path.text = f'{prior} Rotate {value},'

    def reset_path(self, root):
        root.ids.path.text = 'Path: '

    def start_travelling(self, root):
        final_path = root.ids.path.text
        split_and_send(final_path)


class WindowManager(ScreenManager):
    pass


class Traversing(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.old_velocity = None
        self.current_dist = 0
        self.current_trace = 1
        self.travel_stage = "Start"
        background_check = threading.Thread(target=self.check_donkey_state, daemon=True)
        background_check.start()

    def check_donkey_state(self):
        def on_message(client, userdata, message):
            msg = message.payload.decode("utf-8")
            print("Received message")
            if message.topic == "TRAVEL_STAGE":
                self.current_trace = int(msg.split(": ")[1])
                self.ids.traversing_label_2.text = "Current stage " + msg
            if message.topic == "DISTANCE":
                self.current_dist = int(msg)
                self.ids.path_progress_bar.value = self.current_dist / self.current_trace
                self.ids.progress_bar_text.text = str(self.ids.path_progress_bar.value * 100) + "% of path traversed."

        # mqttBroker = "192.168.1.113"
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("UserInfo")
        client.on_message = on_message
        client.connect(mqttBroker)

        print("Loading data...")
        client.loop_start()
        client.subscribe([("TRAVEL_STAGE", 1), ("DISTANCE", 1)])


    def stop_donkey(self):
        self.ids.path_progress_bar.value = 0

        # setup client and broker
        # mqttBroker = "192.168.1.113"
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("User")
        client.connect(mqttBroker)

        # send START command - it's necessaery due to
        # design of functions in robot
        command = "INTERRUPT_STOP"
        client.publish("COMMANDS", command)
        print(str(command) + " command has been send")

    def change_velocity(self):
        if self.old_velocity != str(int(self.ids.speed_slider.value)) or self.old_velocity is None:
            self.old_velocity = str(int(self.ids.speed_slider.value))

            # setup client and broker
            # mqttBroker = "192.168.1.113"
            mqttBroker = "mqtt.eclipseprojects.io"
            client = mqtt.Client("User")
            client.connect(mqttBroker)

            # send START command - it's necessaery due to
            # design of functions in robot
            command = "VEL=" + str(int(self.ids.speed_slider.value))
            client.publish("COMMANDS", command)
            print(str(command) + " command has been send")


kv = Builder.load_file('new_window.kv')


class AwesomeApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    AwesomeApp().run()