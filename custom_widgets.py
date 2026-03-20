
from functools import partial

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import NumericProperty, StringProperty, OptionProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from general_modules.Logger import create_logger
log = create_logger("custom_widgets")


class EditableLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_touch_down(self, touch):
        show_text_input_popup(self)

    def set_text_from_input(self, new_text, instance):
        self.text = new_text
        instance.dismiss()


class WidgetCreationPopup(Popup):
    def __init__(self, parent_widget, options_names, **kwargs):
        """ parent_widget: widget, options_names: list[str], **kwargs
        Creates a popup to choose child widget from the options in the options_names"""
        super().__init__(size=(200, 100 + len(options_names) * 32), size_hint=(None, None), pos = (300, 300), **kwargs)
        self.target_parent = parent_widget
        self.options_names = options_names
        self.title = "Widget Creator"
        box = BoxLayout(orientation = "vertical", size = (200, len(options_names) * 50))
        for option_name in options_names:
            option_btn = Button(text = f"{option_name}")
            func = partial(self.option_selected, option_name)
            option_btn.bind(on_release=func)
            option_btn.bind(on_release=self.dismiss)
            box.add_widget(option_btn)
        self.content = box

    def option_selected(self, option_name, instance):
        self.target_parent.option_chosen(option_name)
class DraggableResizableWidget(BoxLayout):
    dragging = BooleanProperty(False)
    resizing = BooleanProperty(False)

    def __init__(self, content_widget_name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos = (300, 300)
        self.background_color = [0.7, 0.7, 1, 1]
        self.content_widget_name = content_widget_name
        self.resize_border = 20
        self.touch_start_pos = None
        self.touch_offset_x = 0.0
        self.touch_offset_y = 0.0
        self.handle_size = 12
        self.header_bar = BoxLayout(size_hint = (1, 0.2))
        self.add_widget(self.header_bar)
        self.build_canvas()
        self.bind_events()
    def build_canvas(self):
        with self.canvas.before:
            self.border_color = Color(0.1, 0.3, 0.5, 1)
            self.border_line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.2)
            self.resize_handle = Rectangle(pos=(self.right-self.handle_size, self.top-self.handle_size), size=(self.handle_size, self.handle_size))

    def bind_events(self):
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)
        self.resize_handle.pos = (self.right - 10, self.top-10)

    def is_near_resize_corner(self, touch):
        return (
            self.right - touch.x < self.resize_border and
            self.top - touch.y < self.resize_border
        )

    def is_in_header_bar(self, touch):
        return(
            self.header_bar.x < touch.x < self.header_bar.right and
            self.header_bar.y < touch.y < self.header_bar.top
        )

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_start_pos = (touch.x, touch.y)
            if self.is_near_resize_corner(touch):
                self.resizing = True
                self.dragging = False
                print("resizing")
            elif self.is_in_header_bar(touch):
                self.dragging = True
                self.resizing = False
                print("in header bar")
            else:
                return super().on_touch_down(touch)

            self.touch_offset_x = self.x - touch.x
            self.touch_offset_y = self.y - touch.y
            return True

    def on_touch_move(self, touch):
        if not self.dragging and not self.resizing:
            return super().on_touch_move(touch)

        if self.resizing:
            new_width = max(50, touch.x - self.x)
            new_height = max(30, touch.y - self.y)
            self.size = (new_width, new_height)
        else:
            self.pos = (touch.x + self.touch_offset_x, touch.y + self.touch_offset_y)
        return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if not self.resizing and self.touch_start_pos:
                dx = abs(touch.x - self.touch_start_pos[0])
                dy = abs(touch.y - self.touch_start_pos[1])
        self.dragging = False
        self.resizing = False
        log.info(f"Widget position: {self.pos}, size: {self.size}")
        return super().on_touch_up(touch)


def show_text_input_popup(origin, **kwargs):
    box = BoxLayout(orientation='vertical')
    text_input = TextInput(text=origin.text, multiline = False)
    confirm_btn = Button(text="OK", size_hint_y=None, height=40)
    box.add_widget(text_input)
    box.add_widget(confirm_btn)
    popup = Popup(title="Edit Text", content=box, size_hint=(None, None), size=(300, 200))
    confirm_btn.bind(on_release=lambda x: origin.set_text_from_input(text_input.text, popup))
    popup.open()

def show_value_popup(self):
    box = BoxLayout(orientation='vertical')
    value_input = TextInput(text=str(self.counter), input_filter='int')
    confirm_btn = Button(text="Set Value", size_hint_y=None, height=40)
    box.add_widget(value_input)
    box.add_widget(confirm_btn)
    popup = Popup(title="Enter Value", content=box, size_hint=(None, None), size=(300, 200))
    confirm_btn.bind(on_release=lambda x: self.set_value_from_input(value_input.text, popup))
    popup.open()