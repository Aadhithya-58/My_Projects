import face_recognition

print(dir(face_recognition))  # Check available functions

# Load an image to test face encoding
image = face_recognition.load_image_file("C:/Users/admin/Pictures/number-1.jpeg")  # Replace with an actual image path
encodings = face_recognition.face_encodings(image)

if encodings:
    print("Face encoding found:", encodings[0])
else:
    print("No face found!")