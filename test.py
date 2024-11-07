import pyodbc
import xml.etree.ElementTree as ET

# Set up your database connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=WINSERV2022;DATABASE=OneIM;UID=sa;PWD=Password123!')

# Execute the query to retrieve the filename and XML content
cursor = conn.cursor()
cursor.execute("SELECT FileName, customcode FROM DialogAEDS WHERE UID_DialogProduct = 'QBM-622BB2900FC2A11B3BFB908847869C46'")

# Fetch all rows
rows = cursor.fetchall()

# Loop through each row to save XML data with the specified filename
for row in rows:
    # Get the filename and XML data from the row
    filename = row.FileName  # This will be used as the file name
    xml_data = row.customcode  # Assuming this column contains the XML content

    # Parse the XML content to ensure it’s well-formed
    try:
        root = ET.fromstring(xml_data)  # Check if it's well-formed XML
    except ET.ParseError as e:
        print(f"Error parsing XML for file {filename}: {e}")
        continue
    
    # Write XML data to a file with the filename from the database
    with open(f'{filename}.xml', 'w', encoding='utf-8') as file:
        # Write XML content in a formatted way
        file.write(ET.tostring(root, encoding='unicode'))
    
    print(f'Saved file {filename}.xml')

# Close the cursor and connection
cursor.close()
conn.close()