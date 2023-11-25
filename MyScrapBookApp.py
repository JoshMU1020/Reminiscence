import os
import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class DropZone(FloatLayout):
    def __init__(self, **kwargs):
        super(DropZone, self).__init__(**kwargs)
        self.drop_area = None
        self.add_text_input()

    def update_drop_zone(self, *args):
        self.drop_area = self.pos + self.size

    def _on_file_drop(self, window, file_path, x, y):
        print(f"File dropped: {file_path}")
        print(f"Drop position: {x}, {y}")
        # Check if the drop is within this widget's bounds
        self.handle_dropped_file(file_path)

    def handle_dropped_file(self, file_path):
        decoded_file_path = file_path.decode('utf-8')
        if decoded_file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.display_image(decoded_file_path)

    def display_image(self, file_path):
        print(f"Displaying image in DropZone at {self.pos} with size {self.size}")
        self.clear_widgets()
        image = Image(source=file_path, keep_ratio=True, allow_stretch=True,
                      size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(image)

    def clear_contents(self):
        self.clear_widgets()

    def add_text_input(self):
        self.clear_widgets()
        text_input = TextInput(
            hint_text='Enter your note here or Drag and Drop image',
            size_hint=(1, 1),
            halign='center',
            padding_y=(self.height * 0.4, 0),
            background_color=(243/255, 170/255, 107/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            multiline=True
        )
        text_input.bind(on_text=self.on_text)
        self.add_widget(text_input)

    def on_text(self, instance, value):
        instance.cursor = (0, 0)  # Reset cursor to start


class WelcomeScreen(Screen):
    '''
    This screen will contain:
    - Create Account button:
        - If chosen, a popup asking to enter a username and password into two text boxes is shown with confirm button.
    - Enter username text box.
    - Enter password text box.
    - credential confirmation button:
        - If username and password combination exist in credential file, move to MainMenu screen.
    '''
    pass  # Your welcome screen layout and logic


class MainMenu(Screen):
    '''
    This screen will contain 6 buttons:
    - View pages button:
        - Move to ViewPages screen.
    - Create new page button:
        - Move to TemplateSelect screen.
    - See all images button:
        - Move to DataScrolling screen.
    - See all videos button:
        - Move to DataScrolling screen.
    - See all notes button:
        - Move to DataScrolling screen.
    - Logout button:
        - return to welcome screen.
    '''
    pass  # Main menu layout and logic


class ViewPages(Screen):
    '''
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - A scrolling view of all created pages associated with the current user.
    '''
    def load_images(self):
        directory = 'saved_collages'
        if not os.path.exists(directory):
            return  # Directory does not exist

        container = self.ids.pages_container
        container.clear_widgets()  # Clear existing images if any
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(directory, filename)
                img = Image(source=file_path, size_hint_y=None, height=400)  # Set a fixed height for each image
                container.add_widget(img)


class TemplateSelect(Screen):  # MAY DROP IN FUTURE---------------------------------------------------------------------
    '''
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - Four page templates that the user can click on:
        - clicking on one of the templates both...
            - Moves user to PageCreation screen.
            - Places the selected template onto the PageCreation screen.
    '''
    pass  # template menu layout and logic


class PageCreation(Screen):
    '''
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - Displays the chosen page template:
        - Each template will have a number of boxes of varying size:
            - Each of these boxes can have memory data in the form of images, videos, or notes placed in them:
                - Users can drag and drop images/videos directly into these boxes.
                - Users can also click on the empty boxes to bring up a popup containing buttons, image, video, or note:
                    - image:
                        - popup displaying all images in the user's image folder where they can select one and place it.
                    - video:
                        - popup displaying all video in the user's video folder where they can select one and place it.
                    - note:
                        - popup of textbox that the user can write into. text is then displayed into the empty page box.
    - Confirmation button:
        - user confirms that the page is complete.
        - Page is then placed into a page directory associated with the current user to be viewed from ViewPages screen.
    '''
    def handle_drop(self, drop_zone, file_path):
        drop_zone.handle_dropped_file(file_path)

    pass  # page creation menu layout and logic

''' 
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.drop_area = FileDropWidget(size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
    self.add_widget(self.drop_area)
    '''


class DataScrolling(Screen):  # MAY DROP IN FUTURE----------------------------------------------------------------------
    '''
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - The MainMenu screen contains three buttons that lead to this screen:
        - If button pressed was "See all images":
            - This screen shows a scrolling bar of all images in the image directory associated with the current user.
        - If button pressed was "See all video":
            - This screen shows a scrolling bar of all videos in the video directory associated with the current user.
        - If button pressed was "See all images":
            - This screen shows a scrolling bar of all notes in the note directory associated with the current user.
    '''
    pass  # Data scrolling menu layout and logic


class MyScrapbookApp(App):
    # A list to store the saved pages
    saved_pages = []

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(MainMenu(name='mainMenu'))
        sm.add_widget(ViewPages(name='viewPages'))
        sm.add_widget(TemplateSelect(name='templateSelect'))
        sm.add_widget(PageCreation(name='pageCreation'))
        sm.add_widget(DataScrolling(name='dataScrolling'))
        # ... setup screens and drop zones ...
        Window.bind(on_drop_file=self.on_file_drop)
        return sm

    def open_create_account_popup(self):
        self.create_account_popup = Factory.CreateAccountPopup()
        self.create_account_popup.open()

    def create_account(self, username, password):
        # Logic to create a new account
        # Save the username and password to a file or database
        print("Creating account with...\nUsername:", username, "\nPassword:", password)
        self.create_account_popup.dismiss()

    def open_place_data_popup(self):
        self.place_data_popup = Factory.PlaceDataPopup()
        self.place_data_popup.open()

    def open_create_note_popup(self):
        self.create_note_popup = Factory.CreateNotePopup()
        self.create_note_popup.open()

    def save_note(self, note):
        # Save the note to a file or database
        print("Saving Note...")
        print(note)
        self.create_note_popup.dismiss()

    def switch_to_data_scrolling(self, data_type):  # MAY DROP IN FUTURE------------------------------------------------
        # Here, add logic to prepare the DataScrolling screen based on the data_type ('image' or 'video')
        self.root.current = 'dataScrolling'

    def on_file_drop(self, window, file_path, x, y):
        print(f"File dropped at global coordinates: {x}, {y}")
        y = Window.height - y
        for drop_zone in self.get_drop_zones(self.root):
            # Use the original global coordinates
            if drop_zone.collide_point(x, y):
                print(f"Drop zone hit at: {drop_zone.pos}")
                drop_zone._on_file_drop(window, file_path, x, y)
                return

    def get_drop_zones(self, widget):
        drop_zones = []
        if isinstance(widget, DropZone):
            drop_zones.append(widget)
            print(f"DropZone found at {widget.pos} with size {widget.size}")
        if hasattr(widget, 'children'):
            for child in widget.children:
                drop_zones.extend(self.get_drop_zones(child))
        return drop_zones

    def get_next_collage_number(self, directory):
        highest_num = 0
        for filename in os.listdir(directory):
            match = re.match(r"collage(\d+)\.png", filename)
            if match:
                num = int(match.group(1))
                highest_num = max(highest_num, num)
        return highest_num + 1

    def save_collage(self, layout):
        directory = 'saved_collages'
        if not os.path.exists(directory):
            os.makedirs(directory)

        next_number = self.get_next_collage_number(directory)
        file_path = os.path.join(directory, f'collage{next_number}.png')

        layout.export_to_png(file_path)
        self.clear_all_drop_zones()
        print(f"Collage saved as: {file_path}")

    def clear_all_drop_zones(self):
        for drop_zone in self.get_drop_zones(self.root):
            drop_zone.clear_contents()


if __name__ == "__main__":
    MyScrapbookApp().run()