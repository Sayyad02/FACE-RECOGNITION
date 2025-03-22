# face_recognition_system.py
import face_recognition
import cv2
import os
import numpy as np
import config
import utils
import database

class FaceRecognitionSystem:
    def __init__(self):
        """Initializes the FaceRecognitionSystem."""
        self.tolerance = config.TOLERANCE
        self.model = config.MODEL
        self.known_face_encodings = []
        self.known_face_names = []
        database.create_database()  # Ensure the database exists
        self.load_known_faces()


    def load_known_faces(self):
        """Loads known face data from the database."""
        self.known_face_names, self.known_face_encodings = database.get_all_faces_from_db()
        print(f"Loaded {len(self.known_face_names)} faces from the database.")


    def add_face_from_image(self, image_path, name):
        """Adds a new face to the database from an image file."""
        try:
            image = utils.load_image(image_path)
            rgb_image = utils.convert_bgr_to_rgb(image)  # Convert to RGB
            face_encoding = face_recognition.face_encodings(rgb_image)[0] #convert to rgb before getting encodings
            database.add_face_to_db(name, face_encoding)
            self.load_known_faces()  # Reload after adding
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error adding face: {e}")


    def recognize_faces(self, frame):
        """Recognizes faces in a given frame."""
        small_frame = utils.resize_frame(frame, 0.25)
        rgb_small_frame = utils.convert_bgr_to_rgb(small_frame)

        face_locations = face_recognition.face_locations(rgb_small_frame, model=self.model)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=self.tolerance)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            if len(face_distances) > 0: #prevent errors when the known_faces_encoding is empty
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Scale back up face locations
        scaled_face_locations = []
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            scaled_face_locations.append((top, right, bottom, left))

        return scaled_face_locations, face_names


    def draw_boxes_and_labels(self, frame, face_locations, face_names):
        """Draws bounding boxes and name labels on the frame."""
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)  # Green for known, red for unknown
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def delete_face(self,name):
        """
        Deletes a face by its name from the database.
        """
        database.delete_face_from_db(name)
        # Reload to reflect the database change
        self.load_known_faces()

    def update_face(self, name, new_image_path):
        """
        Updates the face encoding for an existing user.

        Args:
            name (str): The name of the user to update.
            new_image_path (str): The path to the new image.
        """
        try:
            image = utils.load_image(new_image_path)
            rgb_image = utils.convert_bgr_to_rgb(image)
            new_encoding = face_recognition.face_encodings(rgb_image)[0]
            database.update_face_in_db(name, new_encoding)
            self.load_known_faces()  # Reload to reflect database changes.
            print(f"Face encoding for '{name}' updated successfully.")
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error updating face: {e}")