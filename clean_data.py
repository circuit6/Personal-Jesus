import os

def concatenate_txt_files_from_subdirs(source_dir, output_filename):
    # Initialize an empty string to hold the contents of all files
    all_contents = ''
    
    # Walk through all directories and subdirectories in the source_dir
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt'):
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                # Open and read the file, then concatenate its contents
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_contents += f.read()
    
    # Save the concatenated contents into a new file in the "data" directory
    output_path = os.path.join('data', output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(all_contents)
    
    return output_path

# Example usage
source_dir = 'data'  # Replace with your source directory path
output_filename = 'concatenated_files.txt'
output_path = concatenate_txt_files_from_subdirs(source_dir, output_filename)
print(f'All .txt files from subdirectories have been concatenated into: {output_path}')