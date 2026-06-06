import cv2
import os
import numpy as np
import pickle
import face_recognition
from datetime import datetime
import cvzone
from supabase import create_client, Client

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
ref = supabase.table("Students")
ref_storage = supabase.storage.from_("Student Images")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

img_background = cv2.imread('resources/background.png')

folder_mode_path = 'resources/modes'
mode_path_list = os.listdir(folder_mode_path)
img_mode_list = []

for path in mode_path_list:
    img_mode_list.append(cv2.imread(os.path.join(folder_mode_path, path)))

print("Loading encoder file")
file = open('encode_file.pkl', 'rb')
encode_list_known_with_ids = pickle.load(file)
file.close()

encode_list_known, student_ids = encode_list_known_with_ids
print("Encoder file loaded")

mode_type = 0
counter = 0
frame_count = 0
student_info = None
img_student = None
student_id = ""

while True:
    success, img = cap.read()
    if not success:
        break

    frame_count += 1

    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    img_background[162:162+480, 55:55+640] = img
    img_background[44:44+633, 808:808+414] = img_mode_list[mode_type]

    if frame_count % 4 == 0 and counter == 0:
        face_cur_frame = face_recognition.face_locations(img_small)
        encode_cur_frame = face_recognition.face_encodings(img_small, face_cur_frame)
        
        if face_cur_frame:
            for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
                matches = face_recognition.compare_faces(encode_list_known, encode_face)
                face_dis = face_recognition.face_distance(encode_list_known, encode_face)

                match_index = np.argmin(face_dis)

                if matches[match_index]:
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    img_background = cvzone.cornerRect(img_background, bbox=bbox, rt=0)
                    student_id = student_ids[match_index]

                    cvzone.putTextRect(img_background, 'Loading...', (275, 400))
                    cv2.imshow("Face Attendance", img_background)
                    cv2.waitKey(1)
                    counter = 1
                    mode_type = 1

    if counter != 0:
        if counter == 1:
            try:
                student_info = ref.select("id", "name", "major", "starting_year", "total_attendance", "standing", "year", "last_attendance_time").eq("id", student_id).execute().data[0]
                print(student_info)

                blob = ref_storage.download(f"{student_id}.jpg")
                array = np.frombuffer(blob, np.uint8)
                img_student = cv2.imdecode(array, cv2.IMREAD_COLOR)
                if img_student is not None:
                    img_student = cv2.resize(img_student, (216, 216))

                raw_time = student_info['last_attendance_time']
                clean_time = raw_time.split('+')[0]
                date_time = datetime.strptime(clean_time, "%Y-%m-%dT%H:%M:%S.%f")
                second_elapsed = (datetime.now() - date_time).total_seconds()
            
                if second_elapsed > 30:
                    ref.update({
                        "total_attendance": student_info['total_attendance'] + 1, 
                        "last_attendance_time": str(datetime.now())
                    }).eq("id", student_id).execute()
                    student_info['total_attendance'] += 1
                else:
                    mode_type = 3
                    counter = 0
                    img_background[44:44+633, 808:808+414] = img_mode_list[mode_type]

            except Exception as e:
                print(f"❌ Lỗi: {e}")
                counter = 0
                mode_type = 0

        if mode_type != 3:
            if 10 < counter < 20:
                mode_type = 2

            img_background[44:44+633, 808:808+414] = img_mode_list[mode_type]

            if counter <= 10 and student_info is not None:
                cv2.putText(img_background, str(student_info['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(img_background, str(student_info['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 2)
                cv2.putText(img_background, str(student_id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(img_background, str(student_info['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(img_background, str(student_info['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(img_background, str(student_info['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2    
                cv2.putText(img_background, str(student_info['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                
                if img_student is not None:
                    img_background[175:175+216, 909:909+216] = img_student

        counter += 1

        if counter >= 20:
            counter = 0
            mode_type = 0
            student_info = None
            img_student = None
            img_background[44:44+633, 808:808+414] = img_mode_list[mode_type]

    cv2.imshow("Face Attendance", img_background)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()