from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import paho.mqtt.client as mqtt

def split_and_send(final_path):
    print(final_path)
    # Delete Path:
    final_path = final_path[6:]
    print(type(final_path))

    # Change to list
    final_path = final_path.split(sep=',')
    print(final_path)
    final_path = final_path[:-1]
    print(final_path)

    for i in range(len(final_path)):
        final_path[i] = final_path[i][1:]
    print(final_path)

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
    pass

class AboutDonkey(Screen):
    pass

class ChoosePath(Screen):
    pass

class GridTop(GridLayout):
    pass

class Calculator(BoxLayout):
    def clear(self):
        self.ids.calc_input.text = '0'

    def remove(self):
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



kv = Builder.load_file('new_window.kv')

class AwesomeApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    AwesomeApp().run()