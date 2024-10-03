import os

# Specify the folder path
folder_path = r"C:\Users\jinfa\OneDrive\Desktop\UDHR AI\txts"

# List all files in the folder
files = os.listdir(folder_path)

# Loop through each file in the folder
for file_name in files:
    # Construct full file path
    file_path = os.path.join(folder_path, file_name)
    
    # Check if it's a .txt file
    if file_path.endswith('.txt'):
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove newlines, commas, semicolons, colons, and periods
        content = content.replace('\n', ' ').replace(',', '').replace('.', '').replace(';', '').replace(':', '').replace('°', '').replace('。', '').replace('、', '').replace('，', '').replace('ª', '')
        
        # Replace hyphens with spaces
        content = content.replace('-', ' ').replace("‐", ' ')

        # Find the position of the first instance of the string ' 1 '
        start_pos = content.find(' 1 ')
        
        # If ' 1 ' is found, remove everything before it
        if start_pos != -1:
            content = content[start_pos:]
                
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

print("Processing complete.")
