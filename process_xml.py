import os
import re
import xml.etree.ElementTree as ET

def process_xml_files_in_folder(folder_path, xml_output_folder):
    """
    Iterates through all XML files in a specified folder and applies static processing logic to each file.

    Parameters:
    - folder_path (str): The path to the folder containing the XML files.
    - xml_output_folder (str): The folder where the processed XML files will be saved.
    """

    # Create the output folders if they don't exist
    os.makedirs(xml_output_folder, exist_ok=True)

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):  # Process only XML files
            name = os.path.splitext(filename)[0]  # Extract file name without extension
            file_path = os.path.join(folder_path, filename)  # Full path of the file

            # Reading the XML file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Removing all instances of <lb break="no"/> and <pc>·</pc>
            modified_content = content.replace('<lb break="no"/>', '')
            modified_content = modified_content.replace('<pc>·</pc>', '')
            modified_content = modified_content.replace('<pc>·</pc>', '')

            # Saving the modified content back to a new file
            modified_file_path = os.path.join(xml_output_folder, f'clean1_{name}.xml')
            with open(modified_file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

            # Parse the cleaned XML file
            tree = ET.parse(modified_file_path)
            root = tree.getroot()

            # Get the namespace (ns0) from the root tag
            ns = {'ns0': root.tag.split('}')[0].strip('{')}

            # Function to remove corrector readings
            def remove_corrector_readings(element):
                # Remove <teiHeader>
                tei_header = element.find(".//ns0:teiHeader", ns)
                if tei_header is not None:
                    element.remove(tei_header)

                # Remove <note> with type="local"
                for parent in element.findall(".//ns0:*", ns):
                    for child in list(parent):
                        if child.tag.endswith('note') and child.get('type') == 'local':
                            parent.remove(child)

                # Remove <rdg> with hand="corrector1" or "corrector2"
                for app in element.findall(".//ns0:app", ns):
                    for rdg in app.findall("ns0:rdg", ns):
                        if rdg.get('hand') in ['corrector1', 'corrector2']:
                            app.remove(rdg)

            # Call the function to remove corrector readings
            remove_corrector_readings(root)

            # Write the cleaned XML to a new file
            cleaned_file_path = os.path.join(xml_output_folder, f'clean2_{name}.xml')
            tree.write(cleaned_file_path, encoding='utf-8', xml_declaration=True)
