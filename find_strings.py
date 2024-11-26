import os
import pandas as pd
import re

def find_substrings_in_files(input_folder_path, substrings_to_find, output_folder_path):
    # Define the ordered list of books for the columns
    books = [
        "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", 
        "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", 
        "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", 
        "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
    ]

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterate over each subfolder in the input folder
    for subfolder_name in os.listdir(input_folder_path):
        subfolder_path = os.path.join(input_folder_path, subfolder_name)

        if os.path.isdir(subfolder_path):
            results = {}

            # Iterate over all files in each subfolder
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(subfolder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()

                        # Extract the name part before the last underscore and replace '_' with space
                        file_name_without_extension = os.path.splitext(filename)[0]
                        name_parts = file_name_without_extension.split('_')
                        partial_filename = " ".join(name_parts[:-1])  # Join all but the last part (the chapter number)

                        # Split the content into words (using a regular expression to handle punctuation)
                        words = re.findall(r'\b\w+\b', file_content)

                        # Store the full words that contain each substring
                        for substring in substrings_to_find:
                            for word in words:
                                if substring in word:
                                    if word not in results:
                                        results[word] = {}
                                    if partial_filename not in results[word]:
                                        results[word][partial_filename] = 0
                                    results[word][partial_filename] += 1

            # Create a pandas DataFrame for the current subfolder
            df = pd.DataFrame(results).T
            df.fillna(0, inplace=True)  # Fill any missing values with 0

            # Sort the rows (words) alphabetically
            df.sort_index(inplace=True)

            # Reorder the columns based on the predefined list of books
            df = df.reindex(columns=books, fill_value=0)

            # Define the output file name based on the subfolder name and output folder path
            output_file = os.path.join(output_folder_path, f"{subfolder_name}_results.csv")

            # Save the DataFrame as a CSV file
            df.to_csv(output_file)
            print(f"Results saved to {output_file}")