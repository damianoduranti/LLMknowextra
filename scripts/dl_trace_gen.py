import os
import shutil
import json
from concurrent.futures import ThreadPoolExecutor

def process_folder(base_dir, dir_name):
    original_dir = os.path.join(base_dir, dir_name)
    new_dir_name = dir_name + 'a'
    new_dir = os.path.join(base_dir, new_dir_name)

    os.makedirs(new_dir, exist_ok=True)
    
    for filename in os.listdir(original_dir):
        old_file_path = os.path.join(original_dir, filename)
        new_filename = filename.replace(dir_name, new_dir_name)
        new_file_path = os.path.join(new_dir, new_filename)
        
        if filename.endswith('instances.json'):
            with open(old_file_path, 'r') as file:
                data = json.load(file)
                data['P'], data['N'] = data['N'], data['P']
            
            with open(new_file_path, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            shutil.copy(old_file_path, new_file_path)

def process_folders(base_dir):
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda d: process_folder(base_dir, d), dirs)

# Example usage
base_dirs = ['data/DL_concept/strong_sep/', 'data/DL_concept/weak_sep/']

for base_dir in base_dirs:
    process_folders(base_dir)
