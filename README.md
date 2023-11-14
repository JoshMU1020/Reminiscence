# **Reminiscence**

## **Insperation:**
This project was inspired by our team's CMPSC 472 Operating Systems course. We were tasked as our final project, to create a software application that would provide happiness to the elderly. The contents of this repository are the result of our interpretation of this prompt.


## **Project Overview:**
Reminiscence is an application aimed at providing the elderly with a way to organize data related to their past memories. The software is designed to be a scrapbook-like application that would allow users to create notes and upload images, audio files, or videos to the software which can then be organized to the specifications of the user. The application can be used to store, organize, retrieve, and display memories in the form of photos, recordings, notes, etc. The software will showcase a friendly user interface for accessing these operations while utilizing our course-related concepts to ensure smooth management of the functions required to manipulate this memory data. Aside from the main scrapbook, Reminiscence can provide features like a photo album or an interactive timeline as ways to display the given data of a user. Concepts like threading and process synchronization can be used to ensure smooth transitions from data like photo scrolling. Other concepts related to file management can be used in managing stored data for quick retrieval. All together, Reminiscence will be able to provide the elderly with a way to construct a virtual scrapbook to create a personalized journey through their past memories.


## **Software Features:**

### Provide users with a way to:
- Upload memory data including Notes, Images, Audio Recordings, and Video Recordings.
- Allow users to browse their uploaded media.
- Provide the user with a User-Friendly GUI for them to choose where to place these data items on a GUI canvas.
  - Saves these canvas pages for later viewing.

## **Technology Stack:**
**As of the current date, our tech stack includes:**

**Coding Language:** Python

**GUI Tool:** Kivy
- Kivy’s TextInput Widget: Handles creating and editing text-based notes.
- Kivy’s SoundLoader Class: Handle basic support for playing audio files.
- Kivy’s VideoPlayer Widget: Supports basic video playing features.
- Kivy’s DropFile Widget: Supports drag and drop of files into GUI for a more GUI-friendly environment.

**Image Processing Tool:** Pillow (PIL Fork)
- Can be used alongside Kivy to resize, filter, and format images for display.

**Data Storage:** SQLite3
- Used to store user information related to usernames and passwords that will allow access to the user's related memory data.
- Can be used to store file path references to image, audio, and video files.


## **Implimentaion Process:**



## **Software Showcase:**



## **Project Results and Disscussion:**


