# Face Recognition System

This project implements a face recognition system using Python, OpenCV, face_recognition, and SQLite. It allows you to register known faces, recognize them in real-time from a webcam feed, and manage the database of known faces.

## Project Structure

The project is organized as follows:

face_recognition_project/
├── src/                # Source code directory
│   ├── init.py     # Marks the directory as a Python package
│   ├── face_recognition_system.py  # Main class for face recognition
│   ├── utils.py          # Helper functions (image loading, etc.)
│   ├── database.py        # Database interaction (SQLite)
│   ├── main.py           # Entry point of the application
│   └── config.py          # Configuration settings
├── known_faces/      # Directory for storing images of known faces
├── test_images/      # Directory for testing images (optional)
├── data/             # Directory for the database file
│   └── faces.db       # SQLite database file (automatically created)
├── venv/             # Virtual environment (recommended)
├── requirements.txt  # List of required Python packages
└── README.md         # This file

## Setup and Installation

1.  **Clone the Repository (If Applicable):**

    ```bash
    git clone <repository_url>
    cd face_recognition_project
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**

    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    *   **Note on `dlib`:** The `face_recognition` library depends on `dlib`.  If you encounter issues installing `dlib`, refer to the `face_recognition` library's documentation for platform-specific instructions. You might need to use `conda` or install Visual Studio C++ Build Tools (on Windows).

5. **Create Directories:**
   * Create the following directories if they do not already exist: `known_faces`, `test_images`(optional) and `data`.

## Usage

### 1. Adding Known Faces

Before you can recognize faces, you need to add them to the database.  Use the following command:

```bash
python src/main.py --add_face --image_path <path_to_image> --name "<person's_name>"
--add_face: Tells the script to add a new face.
--image_path: The path to the image file of the person you want to add (e.g., known_faces/John Doe.jpg). Important: This image should contain only one face, and it should be a clear, well-lit image of the person.
--name: The name of the person in the image (e.g., "John Doe").
Example:

Bash

python src/main.py --add_face --image_path known_faces/Jane_Smith.jpg --name "Jane Smith"
Important: Place the images of known faces in the known_faces directory, and name each file after the person in the image (e.g., John_Doe.jpg).
2. Running Face Recognition (Webcam)
To start the face recognition system using your webcam:

Bash

python src/main.py
This will open a window displaying the webcam feed.
The system will attempt to recognize faces in real-time.
Recognized faces will be marked with a green bounding box and their name.
Unknown faces will be marked with a red bounding box and the label "Unknown".
Press q to quit.
3. Updating an Existing Face
If you have a better image of a person already in the database, you can update their face encoding:

Bash

python src/main.py --update_face --image_path <path_to_new_image> --name "<person's_name>"
--update_face: Indicates that you want to update an existing face.
--image_path: The path to the new image of the person.
--name: The name of the person whose face you are updating.
Example:

Bash

python src/main.py --update_face --image_path known_faces/Jane_Smith_New.jpg --name "Jane Smith"
4. Deleting a Face
To remove a face from the database:

Bash

python src/main.py --delete_face --name "<person's_name>"
--delete_face: Tells the program to delete a face entry.
--name: The name of the person to remove.
Example:

Bash

python src/main.py --delete_face --name "Jane Smith"
Code Overview
config.py
This file stores configuration settings:

DATABASE_PATH: The path to the SQLite database file (default: data/faces.db).
KNOWN_FACES_DIR: The path to directory containing known face (default: known_faces).
TOLERANCE: The threshold for face distance comparison (default: 0.6). Lower values are stricter.
MODEL: The face detection model to use: "hog" (faster, less accurate) or "cnn" (slower, more accurate).
utils.py
This file contains helper functions:

load_image(image_path): Loads an image from the given path, raising errors if the file is not found or cannot be opened.
display_image(image, title="Image"): Displays an image in a window.
convert_bgr_to_rgb(image): Converts an image from BGR (OpenCV's default) to RGB (used by face_recognition).
resize_frame(frame, scale_factor): Resizes a frame by a given scale factor.
database.py
This file handles interactions with the SQLite database:

adapt_array(arr) and convert_array(text): Functions to convert NumPy arrays (face encodings) to and from binary strings for database storage.
create_database(): Creates the database and the faces table if they don't exist.
add_face_to_db(name, encoding): Adds a new face (name and encoding) to the database.
get_all_faces_from_db(): Retrieves all face encodings and names from the database.
delete_face_from_db(name): Deletes a face from the database by name.
update_face_in_db(name, new_encoding): Updates the encoding for an existing face.
face_recognition_system.py
This file contains the main FaceRecognitionSystem class:

__init__(): Initializes the system, loads configuration, creates the database (if it doesn't exist), and loads known faces from the database.
load_known_faces(): Loads face data (names and encodings) from the database.
add_face_from_image(image_path, name): Adds a new face to the database from an image file. Handles image loading, face encoding, and database insertion.
recognize_faces(frame): Performs face recognition on a given frame. Resizes the frame, converts to RGB, finds face locations and encodings, compares encodings to known faces, and returns scaled face locations and names.
draw_boxes_and_labels(frame, face_locations, face_names): Draws bounding boxes and name labels on the frame. Uses green for known faces and red for unknown faces.
delete_face(name): Deletes a face record from the database, based on the provided name.
update_face(name, new_image_path): Updates the face encoding for an existing face in the database, using the new image provided.
main.py
This is the entry point of the application:

main():
Parses command-line arguments using argparse.
Handles --add_face, --update_face and --delete_face operations by calling the appropriate methods of the FaceRecognitionSystem class.
If no add/update/delete arguments are provided, it starts the webcam-based face recognition loop:
Initializes the webcam.
Reads frames from the webcam.
Calls recognize_faces to detect and recognize faces.
Calls draw_boxes_and_labels to draw results on the frame.
Displays the frame.
Exits when the 'q' key is pressed.
Troubleshooting
ModuleNotFoundError: Ensure your virtual environment is activated and all required packages are installed (pip install -r requirements.txt).
Webcam Issues: Verify your webcam is working and you're using the correct camera index (usually 0) in cv2.VideoCapture(0).
Face Not Recognized: Adjust the TOLERANCE in config.py, add more/better images to known_faces/, or switch to the "cnn" model.
dlib installation: Check the face_recognition library page for OS specific instructions.

I am unable to create or manipulate images. I am a text-based model and do not have the capability to generate or edit visual content. I can, however, describe in detail what you would see when running the project and the various scenarios.

Here's a textual description of what the program's output would look like in different situations, along with descriptions of the command-line interactions:

1. Adding a Face (Command Line):

Command:

Bash

python src/main.py --add_face --image_path known_faces/John_Doe.jpg --name "John Doe"
Terminal Output:

Face 'John Doe' added to the database.
Loaded 1 faces from the database.
(The "Loaded X faces" number will increment as you add more faces.)  There is no visual output other than this text.  The program adds the face data to the data/faces.db database file.

2. Running Face Recognition (Webcam):

Command:

Bash

python src/main.py
Visual Output (Webcam Window):

A window titled "Video" appears, showing the live feed from your webcam.

Scenario A: Recognized Face:

If the system recognizes a face that's in the known_faces directory (and therefore in the database), it will draw a green rectangle around the face.
Below the rectangle, the person's name (as you entered it when adding the face) will be displayed in white text. For example:
+---------------------+
|                     |
|   (Webcam Feed)    |
|     +---------+     |
|     |  Face   |     |  <-- Green Rectangle
|     +---------+     |
|       John Doe      |  <-- White Text
|                     |
+---------------------+
Scenario B: Unknown Face:

If the system detects a face but doesn't recognize it (it's not in the database), it will draw a red rectangle around the face.
Below the rectangle, it will display the text "Unknown" in white.
+---------------------+
|                     |
|   (Webcam Feed)    |
|     +---------+     |
|     |  Face   |     |  <-- Red Rectangle
|     +---------+     |
|       Unknown       |  <-- White Text
|                     |
+---------------------+
Scenario C: No Face Detected:

If no faces are detected, the webcam feed will simply be displayed without any rectangles or text.
Scenario D: Multiple Faces:

The system can handle multiple faces simultaneously. Each detected face will have a rectangle (green for known, red for unknown) and the corresponding label. The rectangles and labels will track the faces as they move within the frame.

This README provides a comprehensive overview of the project, its functionality, and how to use it.  It should be easy for anyone to understand and get started with the face recognition system.