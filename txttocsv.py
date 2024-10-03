import os
import csv

# Define the paths
input_folder = r"C:\Users\jinfa\OneDrive\Desktop\UDHR AI\txts"
output_folder = r"C:\Users\jinfa\OneDrive\Desktop\UDHR AI\csvs"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Initialize dictionaries to hold the text data for each CSV file
csv_data = {f'csv{i+1}.csv': [] for i in range(30)}

# Process each text file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        language = os.path.splitext(filename)[0]
        filepath = os.path.join(input_folder, filename)
        
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split the content by sections
        for i in range(1, 31):
            start_marker = f' {i} '
            end_marker = f' {i+1} ' if i < 30 else ''
            
            start_index = content.find(start_marker)
            end_index = content.find(end_marker, start_index + len(start_marker))
            
            if start_index != -1:
                start_index += len(start_marker)
                if end_index == -1 and i == 30:  # Special case for section 30
                    section_text = content[start_index:].strip()
                else:
                    section_text = content[start_index:end_index].strip()
                
                csv_filename = f'csv{i}.csv'
                csv_data[csv_filename].append({'Language': language, 'Text': section_text})

# Write the data to CSV files
for csv_filename, rows in csv_data.items():
    csv_filepath = os.path.join(output_folder, csv_filename)
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Language', 'Text'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
os.remove(r"C:\Users\jinfa\OneDrive\Desktop\UDHR AI\csvs\csv30.csv")
print("CSV files created successfully.")
