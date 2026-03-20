from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty, OptionProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from general_modules.Logger import create_logger
from custom_widgets import DraggableResizableWidget, show_text_input_popup, EditableLabel, WidgetCreationPopup
from saving import SaveSystem
log = create_logger("interface")



# mode = OptionProperty("counter", options=["counter", "textbox", "value_entry"])
# counter = NumericProperty(0)
# text = StringProperty("0")


class AspectLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.title = EditableLabel(text = "TITLE", size_hint= (1, 0.33))
        self.add_widget(self.title)

    # def on_touch_down(self, touch):
    #     if self.title.collide_point(touch.x, touch.y):
    #         show_text_input_popup(self.title)
    #     else:
    #         return super().on_touch_down(touch)
class CounterWidget(AspectLayout):
    counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.specific_layout = BoxLayout(orientation = "horizontal")
        self.add_widget(self.specific_layout)
        self.increase_btn = Button(text="+")
        self.increase_btn.bind(on_press = self.increase_counter)
        self.decrease_btn = Button(text="-")
        self.decrease_btn.bind(on_press = self.decrease_counter)
        self.display = Label(text = "0", size_hint = (1, 0.6), pos_hint = {"x": 0, "y": 0})
        self.specific_layout.add_widget(self.display)
        self.specific_layout.add_widget(self.increase_btn)
        self.specific_layout.add_widget(self.decrease_btn)
        self.bind(counter= self.update_label)

    def get_data(self):
        """returns data as dict"""
        data_dict = {"name": self.title.text, "counter" : self.counter}
        return data_dict

    def set_data(self, data):
        self.title.text = data["name"]
        self.counter = data["counter"]

    def update_label(self, instance, value):
        self.display.text = f"{self.counter}"

    def increase_counter(self, instance):
        self.counter += 1
        print(self.counter)

    def decrease_counter(self, instance):
        self.counter -= 1
        print(self.counter)
class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_system = SaveSystem("data")
        self.frames = []
        self.layout_data = []
        self.tracker_widgets = []
        self.trackers_data = {}
        self.options_dict = {"Counter": CounterWidget, "Text": TextInput, "empty": DraggableResizableWidget}
        self.menu_bar = FloatLayout(pos= (0, Window.height - 60), size = Window.size)
        self.add_widget(self.menu_bar)
        self.dynamic_area = FloatLayout(pos= (0, 0), size = (Window.width, Window.height - 60))
        self.add_widget(self.dynamic_area)
        self.menu_button_size = (120, 50)
        self.buttons = 0
        self.create_menu()
        self.create_widget("counter")

    def create_menu(self):
        self.create_menu_button("Add Widget", self.show_mode_selection_popup)
        # self.create_menu_button("save Layout", self.save_layout)
        # self.create_menu_button("load Layout", self.load_layout)
        # self.create_menu_button("save data", self.save_data)
        # self.create_menu_button("load data", self.load_data)
        self.create_menu_button("save", self.save)
        self.create_menu_button("load", self.load)

    def create_menu_button(self, button_text, func):
        self.menu_bar.add_widget(Button(
            text = button_text,
            size_hint=(None, None),
            size = (120, 50),
            pos= (10 + self.buttons * 150, Window.height - 60),
            on_release = func
        ))
        self.buttons += 1
    def show_mode_selection_popup(self, instance):

        popup = WidgetCreationPopup(self, self.options_dict.keys())
        popup.open()

    def option_chosen(self, name):
        self.create_widget(name)

    def create_widget(self, widget_name):
        widget = self.options_dict[widget_name]()
        frame = DraggableResizableWidget(widget_name)
        frame.add_widget(widget)
        self.frames.append(frame)
        self.dynamic_area.add_widget(frame)
        self.tracker_widgets.append(widget)
        return frame

    def get_data(self, trigger = None):
        data = {}
        for widget in self.tracker_widgets:
            widget_data_dict = widget.get_data()
            key = widget_data_dict["name"]
            name = key
            duplicate = 1
            while name in data.keys():
                duplicate += 1
                name = key + f"({duplicate})"
            data[name] = widget_data_dict
            print(f"widget_data_dict for {name}: {data[name]}")
        print(f" get_data data: {data}")
        return data

    def save_data(self, instance = None):
        self.trackers_data = self.get_data()

    def load_data(self, instance = None):
        data = self.trackers_data
        print(f"load_data: {data=}")
        index = 0
        for key, value in data.items():
            self.tracker_widgets[index].set_data(value)
            index += 1

    def get_layout(self):
        layout_data = []
        for frame in self.frames:
            frame_data = {}
            frame_data["widget_type"] = frame.content_widget_name
            frame_data["size"] = (frame.size[0], frame.size[1])
            frame_data["pos"] = (frame.pos[0], frame.pos[1])
            layout_data.append(frame_data)
        print((f"get_layout layout_data: {layout_data}"))
        return layout_data

    def save_layout(self, instance = None):
        self.layout_data = self.get_layout()


    def load_layout(self, instance = None):
        layout_data = self.layout_data
        self.dynamic_area.clear_widgets()
        self.frames = []
        self.tracker_widgets = []
        for frame_data in layout_data:
            frame = self.create_widget(frame_data["widget_type"])
            frame.size = frame_data["size"]
            frame.pos = frame_data["pos"]

    def save(self, instance = None):
        self.save_layout()
        self.save_data()

    def load(self, instance = None):
        self.load_layout()
        self.load_data()



class WidgetBuilderApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    WidgetBuilderApp().run()
