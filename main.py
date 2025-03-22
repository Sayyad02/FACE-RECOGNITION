# main.py
import cv2
import face_recognition_system
import argparse

def main():
    parser = argparse.ArgumentParser(description="Face Recognition System")
    parser.add_argument("--add_face", action="store_true", help="Add a new face from an image file")
    parser.add_argument("--image_path", type=str, help="Path to the image file for adding a face")
    parser.add_argument("--name", type=str, help="Name of the person for the new face")
    parser.add_argument("--update_face", action="store_true", help="Update an existing face with new image")
    parser.add_argument("--delete_face", action ="store_true", help="Delete a face")

    args = parser.parse_args()

    recognizer = face_recognition_system.FaceRecognitionSystem()

    if args.add_face:
        if args.image_path and args.name:
            recognizer.add_face_from_image(args.image_path, args.name)
        else:
            print("Error: Both --image_path and --name are required to add a face.")
        return #exit after adding the face.

    if args.update_face:
        if args.image_path and args.name:
            recognizer.update_face(args.name, args.image_path)
        else:
            print("Error: Both --image_path and --name are required to update a face.")
        return

    if args.delete_face:
        if args.name:
            recognizer.delete_face(args.name)
        else:
            print("Error: --name is required to delete a face.")
        return #exit after deleting the face


    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        face_locations, face_names = recognizer.recognize_faces(frame)
        recognizer.draw_boxes_and_labels(frame, face_locations, face_names)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()