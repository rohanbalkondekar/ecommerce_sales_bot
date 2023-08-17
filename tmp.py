import os

folder_path = 'images'  # Replace this with the path to your 'images' folder
new_folder_path = 'renamed_images'  # Replace this with the desired path for the renamed images

if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

for idx, old_filename in enumerate(image_files, start=1):
    extension = os.path.splitext(old_filename)[1]
    new_filename = f"{idx}{extension}"
    old_filepath = os.path.join(folder_path, old_filename)
    new_filepath = os.path.join(new_folder_path, new_filename)
    
    os.rename(old_filepath, new_filepath)

print("Images renamed successfully.")
