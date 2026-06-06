from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

ref = supabase.table("Students")

ref_storage = supabase.storage.from_("Student Images")

data = [
    {
        "id": "00001", 
        "name": "Nguyen Tuan Dan",
        "major": "AI Intern",
        "starting_year": 2024,
        "total_attendance": 20,
        "standing":  "G",
        'year': 3,
        "last_attendance_time": "2026-06-05 00:07:00"
    },
    {
        "id": "00002", 
        "name": "Messi",
        "major": "Computer Vision Eng",
        "starting_year": 2023,
        "total_attendance": 15,
        "standing":  "E",
        "year": 4,
        "last_attendance_time": "2026-06-04 14:30:15"
    },
    {
        "id": "00003", 
        "name": "Ronaldo",
        "major": "NLP Dev",
        "starting_year": 2025,
        "total_attendance": 8,
        "standing":  "A",
        "year": 2,
        "last_attendance_time": "2026-06-05 09:15:00"
    }
]

response = ref.upsert(data).execute()

image_files = ["00001.jpg", "00002.jpg", "00003.jpg"]
cropped_folder_path = os.path.join("images", "cropped")

for filename in image_files:
    local_file_path = os.path.join(cropped_folder_path, filename)
    cloud_storage_path = filename
    
    if os.path.exists(local_file_path):
        try:
            with open(local_file_path, 'rb') as f:
                ref_storage.upload(
                    path=cloud_storage_path,
                    file=f,
                    file_options={"content-type": "image/jpeg", "x-upsert": "true"} # Ghi đè nếu ảnh trùng tên
                )
            public_url = ref_storage.get_public_url(cloud_storage_path)

        except Exception as e:
            print(f"Lỗi khi upload file {filename}: {e}")
    else:
        print(f"Không tìm thấy file cục bộ tại: {local_file_path}")


    
