import os
import shutil

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from datetime import datetime


class DraggableWidget(Widget):
    def __init__(self, **kwargs):
        super(DraggableWidget, self).__init__(**kwargs)
        self.selected = None
        self.draggable = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.draggable:
            self.selected = self
            return True
        return super(DraggableWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.selected and self.draggable:
            self.selected.center = touch.pos
            return True
        return super(DraggableWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.selected and self.draggable:
            self.selected = None
            return True
        return super(DraggableWidget, self).on_touch_up(touch)


class DropZone(Widget):
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # Handle the drop logic here
            print("Dropped at", touch.pos)
        return super(DropZone, self).on_touch_up(touch)


class DragDropApp(App):
    def build(self):
        root_widget = Widget()

        self.note_input = TextInput(size_hint=(None, None), size=(400, 100), pos=(50, 50))
        root_widget.add_widget(self.note_input)

        # Create a Button to save the note
        save_button = Button(text='Save Note', size_hint=(None, None), size=(100, 50), pos=(50, 10))
        save_button.bind(on_press=self.save_note)
        root_widget.add_widget(save_button)


        # Bind the file drop event
        Window.bind(on_drop_file=self.on_file_drop)

        # Your existing draggable widgets and drop zone code
        for i in range(5):
            draggable = DraggableWidget(size=(100, 100), pos=(i * 110, 100))
            root_widget.add_widget(draggable)

        drop_zone = DropZone(size=(Window.width, 100), pos=(0, 0))
        root_widget.add_widget(drop_zone)

        return root_widget

    def save_note(self, instance):
        text = self.note_input.text
        if text.strip():
            # Ensure the notes directory exists
            notes_dir = 'path_to_your_base_directory/notes'
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)

            # Save the note to a file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(notes_dir, f'note_{timestamp}.txt')
            with open(file_path, 'w') as file:
                file.write(text)

            # Clear the text input for new notes
            self.note_input.text = ''

            # Read the text from the file
            with open(file_path, 'r') as file:
                text = file.read()
            # Create a Label (or TextInput) and add it to the GUI
            label = Label(text=text, size_hint=(None, None), size=(400, 100), pos=(50, 150))
            self.root.add_widget(label)

    def on_file_drop(self, window, file_path, x, y):
        # Corrected method signature
        print(f"Dropped file at {x}, {y}: {file_path.decode('utf-8')}")

        file_path = file_path.decode('utf-8')
        file_type = self.detect_file_type(file_path)
        target_dir = self.get_target_directory(file_type)
        new_file_path = shutil.copy(file_path, target_dir)

        # Handling the file based on its type
        corrected_y = Window.height - y
        if file_type == 'image':
            self.display_image(new_file_path, x, corrected_y)
        elif file_type == 'video':
            self.play_video(new_file_path, x, corrected_y)
        # Add similar handling for text and audio
        elif file_type == 'text':
            self.show_text(new_file_path, x, corrected_y)

    def detect_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        elif ext in ['.mp4', '.avi', '.mov']:
            return 'video'
        elif ext in ['.txt']:
            return 'text'
        elif ext in ['.WAV']:
            return 'audio'
        # Add checks for text and audio file extensions

    def get_target_directory(self, file_type):
        base_dir = 'path_to_your_base_directory'
        target_dir = os.path.join(base_dir, file_type + 's')  # e.g., images, videos
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        return target_dir

    def display_image(self, file_path, x, y):
        # Code to display the image
        print("Attempting to display image...")
        img = Image(source=file_path, size_hint=(None, None), size=(100, 100), pos=(x, y))
        # Add the image to your application's root widget
        self.root.add_widget(img)
        print("Displayed image at ", x, ",", y)

    def play_video(self, file_path, x, y):
        # Code to play the video
        print("Attempting to display video...")
        video = VideoPlayer(source=file_path)
        video.pos = (x, y)
        video.size = (300, 300)
        video.state = 'play'
        video.options = {'eos': 'loop'}
        self.root.add_widget(video)


if __name__ == '__main__':
    DragDropApp().run()