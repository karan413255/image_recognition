import os
import face_recognition
import shutil
from utils import zip_folder
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
scan_folder = "/app/images"

def find_and_zip_matches(input_img_path, scan_folder_input, user_name):
    logging.info(f"Starting face matching for user: {user_name}")
    logging.info(f"Loading reference image from: {input_img_path}")
    known_encodings = []
    input_img_np = face_recognition.load_image_file(input_img_path)
    face_locations = face_recognition.face_locations(input_img_np)
    known_encodings = face_recognition.face_encodings(input_img_np, face_locations)
    logging.info(f"Found {len(known_encodings)} face(s) in the reference image.")

    matched_files = set()
    output_dir = f"matched_results/{user_name}"
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Output directory created at: {output_dir}")

    total_files_scanned = 0
    total_images_matched = 0

    logging.info(f"Scanning folder: {scan_folder}. It exists: {os.path.isdir(scan_folder)}")
    logging.info(f"Listing everything in the folder {scan_folder}: \n{os.listdir(scan_folder)}")
    for root, _, files in os.walk(scan_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                file_path = os.path.join(root, file)
                total_files_scanned += 1
                try:
                    target_img = face_recognition.load_image_file(file_path)
                    encodings = face_recognition.face_encodings(target_img)
                    if not encodings:
                        logging.warning(f"No faces found in image: {file_path}")
                    for encoding in encodings:
                        results = face_recognition.compare_faces(known_encodings, encoding)
                        if any(results):
                            if file_path not in matched_files:
                                shutil.copy(file_path, output_dir)
                                matched_files.add(file_path)
                                total_images_matched += 1
                                logging.info(f"Match found and copied: {file_path}")
                            break
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")

    logging.info(f"Scanned {total_files_scanned} image(s) in total.")
    logging.info(f"Total matched images: {total_images_matched}")

    zip_path = f"{output_dir}.zip"
    logging.info(f"Zipping matched images to: {zip_path}")
    zip_folder(output_dir, zip_path)
    logging.info("Zipping completed.")

    return zip_path, len(known_encodings)
