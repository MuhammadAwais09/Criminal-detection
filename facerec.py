# facerec.py
import cv2
import numpy
import os

size = 2
haar_cascade = cv2.CascadeClassifier(r'C:\face detection and behaviour detection\face_cascade.xml')

# Part 1: Create fisherRecognizer
def train_model():
    model = cv2.face.LBPHFaceRecognizer_create()
    fn_dir = 'face_samples'

    print('Training...')

    (images, labels, names, id) = ([], [], {}, 0)

    allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.pgm', '.bmp']

    for (subdirs, dirs, files) in os.walk(fn_dir):
        for subdir in dirs:
            names[id] = subdir
            subject_path = os.path.join(fn_dir, subdir)
            for filename in os.listdir(subject_path):
                f_name, f_extension = os.path.splitext(filename)
                if f_extension.lower() not in allowed_extensions:
                    print("Skipping " + filename + ", wrong file type")
                    continue
                path = os.path.join(subject_path, filename)
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id += 1

    (images, labels) = [numpy.array(lst) for lst in [images, labels]]
    model.train(images, labels)

    return (model, names)



# Part 2: Use fisherRecognizer on camera stream
def detect_faces(gray_frame):
    global size, haar_cascade

    # Resize to speed up detection (optinal, change size above)
    mini_frame = cv2.resize(gray_frame, (int(gray_frame.shape[1] / size), int(gray_frame.shape[0] / size)))

    # Detect faces and loop through each one
    faces = haar_cascade.detectMultiScale(mini_frame)
    return faces


def recognize_face(model, frame, gray_frame, face_coords, names):
    (img_width, img_height) = (112, 92)
    recognized = []
    recog_names = []

    for i in range(len(face_coords)):
        face_i = face_coords[i]

        # Coordinates of face after scaling back by `size`
        (x, y, w, h) = [v * size for v in face_i]
        face = gray_frame[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (img_width, img_height))

        # Try to recognize the face
        (prediction, confidence) = model.predict(face_resize)

        # print(prediction, confidence)
        if (confidence<95 and names[prediction] not in recog_names):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            recog_names.append(names[prediction])
            recognized.append((names[prediction].capitalize(), confidence))
        elif (confidence >= 95):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return (frame, recognized)

# train_model()