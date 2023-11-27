import os
import re
import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


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
            bold=True,
            font_size='20sp',
            padding_y=(self.height * 0.4, 0),
            background_color=(133/255, 168/255, 186/255, 1),
            hint_text_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            multiline=True
        )
        text_input.bind(on_text=self.on_text)
        self.add_widget(text_input)

    def on_text(self, instance, value):
        instance.cursor = (0, 0)  # Reset cursor to start


class WelcomeScreen(Screen):
    """
    This screen will contain:
    - Create Account button:
        - If chosen, a popup asking to enter a username and password into two text boxes is shown with confirm button.
    - Enter username text box.
    - Enter password text box.
    - credential confirmation button:
        - If username and password combination exist in credential file, move to MainMenu screen.
    """
    def login_and_clear(self):
        self.verify_login()
        # Clear the text inputs
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''

    def verify_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        app = App.get_running_app()
        if app.verify_credentials(username, password):
            app.current_user = username  # Set the current user
            self.manager.current = 'mainMenu'
        else:
            print("\nFailed login attempt!")
            pass


class MainMenu(Screen):
    """
    This screen will contain 6 buttons:
    - View pages button:
        - Move to ViewPages screen.
    - Create new page button:
        - Move to PageCreation screen.
    - Logout button:
        - return to welcome screen.
    """
    def logout(self):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = 'welcome'


class ViewPages(Screen):
    """
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - A scrolling view of all created pages associated with the current user.
    """
    def load_images(self):
        app = App.get_running_app()
        if app.current_user:
            directory = os.path.join('saved_collages', app.current_user)
            if not os.path.exists(directory):
                return  # User's directory does not exist

            container = self.ids.pages_container
            container.clear_widgets()  # Clear existing images if any
            for filename in sorted(os.listdir(directory)):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(directory, filename)
                    img = Image(source=file_path, size_hint_y=None, height=400)  # Set a fixed height for each image
                    container.add_widget(img)
        else:
            print("No user is currently logged in.")


class PageCreation(Screen):
    """
    This screen will contain:
    - Return button:
        - Return to MainMenu screen.
    - Displays the page creating template:
        - Template will have 4 boxes:
            - Each of these boxes can have memory data in the form of images or notes placed in them:
                - Users can drag and drop images directly into these boxes.
                - Users can also click on the empty boxes to type in a text-based note directly into the box.
    - Confirmation button:
        - user confirms that the page is complete.
        - Page is then placed into a page directory associated with the current user to be viewed from ViewPages screen.
    """
    def handle_drop(self, drop_zone, file_path):
        drop_zone.handle_dropped_file(file_path)

    def clear_drop_zones(self):
        app = App.get_running_app()
        for drop_zone in app.get_drop_zones(self):
            drop_zone.clear_contents()
            drop_zone.add_text_input()

    def save_current_collage(self):
        filename = self.generate_collage_filename()
        App.get_running_app().save_collage(self.ids.collage_layout, filename)

    def generate_collage_filename(self):
        # Generate a unique filename based on the current time
        return f"collage_{int(time.time())}.png"


class MyScrapbookApp(App):
    current_user = None

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(MainMenu(name='mainMenu'))
        sm.add_widget(ViewPages(name='viewPages'))
        sm.add_widget(PageCreation(name='pageCreation'))
        Window.bind(on_drop_file=self.on_file_drop)
        return sm

    def open_create_account_popup(self):
        self.create_account_popup = Factory.CreateAccountPopup()
        self.create_account_popup.open()

    def create_account(self, username, password):
        username_input = self.create_account_popup.ids.new_username
        username_input.hint_text = 'Enter username'
        if not username or not password:
            print("Account Creation Failed")
            self.create_account_popup.ids.new_username.text = ''
            self.create_account_popup.ids.new_password.text = ''
            return
        if self.username_exists(username):
            print("Username already exists")
            if hasattr(self, 'create_account_popup'):
                self.create_account_popup.ids.new_username.text = ''
                self.create_account_popup.ids.new_password.text = ''
                username_input = self.create_account_popup.ids.new_username
                username_input.hint_text = 'Username is taken'
            # Optionally show a message to the user in the UI
            return
        with open("credentials.txt", "a") as file:
            file.write(f"{username}:{password}\n")
        print("Account created with Username:", username)
        user_dir = os.path.join("saved_collages", username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        if hasattr(self, 'create_account_popup'):
            self.create_account_popup.ids.new_username.text = ''
            self.create_account_popup.ids.new_password.text = ''
            self.create_account_popup.dismiss()

    def username_exists(self, username):
        try:
            with open("credentials.txt", "r") as file:
                for line in file:
                    stored_username, _ = line.strip().split(':')
                    if username == stored_username:
                        return True
        except FileNotFoundError:
            pass
        return False

    def on_file_drop(self, window, file_path, x, y):
        print(f"File dropped at global coordinates: {x}, {y}")
        y = Window.height - y
        for drop_zone in self.get_drop_zones(self.root):
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
        if self.current_user:
            timestamp = int(time.time())  # Get current timestamp
            filename = f"collage_{timestamp}.png"  # Create a unique filename

            user_dir = os.path.join("saved_collages", self.current_user)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            file_path = os.path.join(user_dir, filename)
            layout.export_to_png(file_path)
            print(f"Collage saved to {file_path}")
        else:
            print("No user is currently logged in.")

    def clear_all_drop_zones(self):
        for drop_zone in self.get_drop_zones(self.root):
            drop_zone.clear_contents()
            drop_zone.add_text_input()  # Re-add TextInput

    def verify_credentials(self, username, password):
        try:
            with open("credentials.txt", "r") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(':')
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            pass
        return False


if __name__ == "__main__":
    MyScrapbookApp().run()
