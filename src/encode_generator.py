import cv2
import face_recognition
import pickle
import os

# Importing student images
folder_path = 'images'
path_list = os.listdir(folder_path)
img_list = []
student_ids=[]

for path in path_list:
    img_list.append(cv2.imread(os.path.join(folder_path,path)))
    student_ids.append(os.path.splitext(path)[0])
    
print(student_ids)

def find_encodings(img_list):
    encodes_list=[]
    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodes_list.append(encode)

    return encodes_list

print('Encoding Started...')
encode_list_known = find_encodings(img_list)
encode_list_known_with_ids = [encode_list_known, student_ids]
print(encode_list_known_with_ids)
print('Encoding Completed!')

file = open('encode_file.pkl', 'wb')
pickle.dump(encode_list_known_with_ids, file)
file.close()
print('File Saved')
