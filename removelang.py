import csv
import os
import argparse

def remove_language_from_csv(csv_folder_path, language_to_remove):
    # Iterate over each CSV file in the folder
    for csv_file_name in os.listdir(csv_folder_path):
        # Check if the file is a CSV
        if csv_file_name.endswith('.csv'):
            csv_file_path = os.path.join(csv_folder_path, csv_file_name)
            
            # Read the CSV file
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = [row for row in reader]
                fieldnames = reader.fieldnames
            
            # Remove the specified language
            rows = [row for row in rows if row['Language'] != language_to_remove]
            
            # Write the modified rows back to the CSV file
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"Removed language '{language_to_remove}' from {csv_file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a language from CSV files.")
    parser.add_argument("language", help="The language to remove from the CSV files")
    parser.add_argument("csv_folder", help="The path to the folder containing CSV files")
    args = parser.parse_args()
    
    remove_language_from_csv(args.csv_folder, args.language)
