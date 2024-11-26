import os
import xml.etree.ElementTree as ET

def process_readings_txt(folder_path, text_output_folder):
    """
    Iterates through all XML files in a specified folder that start with "clean2_", 
    extracts firsthand readings, and saves the results in a new text file for each XML file.
    
    Parameters:
    - folder_path (str): The path to the folder containing the XML files.
    - text_output_folder (str): The folder where the extracted text files will be saved.
    """

    # Create the output folders if they don't exist
    os.makedirs(text_output_folder, exist_ok=True)

    # Iterate through all files in the folder that start with 'clean2_'
    for filename in os.listdir(folder_path):
        if filename.startswith("clean2_") and filename.endswith(".xml"):  # Process only XML files starting with 'clean2_'
            name = os.path.splitext(filename)[0].replace('clean2_', '')  # Extract file name without the 'clean2_' prefix
            file_path = os.path.join(folder_path, filename)  # Full path of the file

            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Function to handle <lb/> and <lb break="no"/>, and extract only firsthand readings while skipping correctors
            def extract_firsthand_readings(element):
                text_parts = []
                for elem in element.iter():
                    # Handle <lb break="no"/> tags (no space added)
                    if 'lb' in elem.tag and elem.get('break') == 'no':
                        continue

                    # Handle regular <lb/> tags (just ignore but maintain word spacing)
                    if 'lb' in elem.tag:
                        continue

                    # Add the text content of the <w> element (if it's inside firsthand and not skipped)
                    if elem.text and 'w' in elem.tag:
                        text_parts.append(elem.text.strip())
                        text_parts.append(' ')  # Add a space after each </w> tag

                # Join the text parts and normalize spaces, removing extra spaces
                return ' '.join(''.join(text_parts).split())

            # Extract all the text, selecting only firsthand readings
            xml_string = extract_firsthand_readings(root)

            # Save the extracted text to a text file with the same base name
            text_output_file_path = os.path.join(text_output_folder, f'{name}.txt')
            with open(text_output_file_path, 'w', encoding='utf-8') as file:
                file.write(xml_string)

