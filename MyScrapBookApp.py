from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


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
    pass  # Page display layout and logic


class TemplateSelect(Screen):
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
    pass  # page creation menu layout and logic


class DataScrolling(Screen):
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
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(MainMenu(name='mainMenu'))
        sm.add_widget(ViewPages(name='pageView'))
        sm.add_widget(TemplateSelect(name='templateSelect'))
        sm.add_widget(PageCreation(name='pageCreation'))
        sm.add_widget(DataScrolling(name='dataScrolling'))
        return sm


if __name__ == "__main__":
    MyScrapbookApp().run()