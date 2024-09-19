import xml.etree.ElementTree as ET
import html

def parse_mxfile(xml_content):
    # Parse the XML content
    root = ET.fromstring(xml_content)
    
    # Dictionary to hold mxCell values by id
    mx_cells = {}
    
    # Iterate over all mxCell elements
    for mxcell in root.iter('mxCell'):
        cell_id = mxcell.get('id')
        cell_value = mxcell.get('value', '')
        
        # Store the mxCell content by ID
        mx_cells[cell_id] = cell_value
        
        # Look for "Enum" in the cell value
        if 'Enum' in cell_value:
            print(f"Found Enum field in mxCell ID: {cell_id} with value: {cell_value}")
            
            # Find related mxCell that contains the enum values
            for related_cell in root.iter('mxCell'):
                if related_cell.get('value', '').startswith('Values:'):
                    # Extract and decode HTML content from the value attribute
                    encoded_value = related_cell.get('value', '')
                    decoded_value = html.unescape(encoded_value)
                    
                    # Extract enum values by removing 'Values:' prefix and splitting by <div> tags
                    enum_values_raw = decoded_value.replace('Values:', '').replace('<div>', '').replace('</div>', '')
                    enum_values = [val.strip() for val in enum_values_raw.split(',') if val.strip()]
                    
                    # Print or process the extracted enum values
                    print(f"Extracted Enum Values: {enum_values}")
                    return enum_values

# Example XML content (replace with your actual XML content)
xml_content = '''
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.14">
  <diagram name="Page-1" id="EQdpkOtj_za4Lja_ZH32">
    <mxGraphModel>
      <root>
        <mxCell id="62Rd1LYud2o8fdQoDaq8-9" value="Enum Type" />
        <mxCell id="62Rd1LYud2o8fdQoDaq8-26" value="Values:&lt;div&gt;BasicSalary,&lt;/div&gt;&lt;div&gt;SalaryRange1,&lt;/div&gt;&lt;div&gt;SalaryRange2,Other&lt;/div&gt;" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

# Call the function to parse the XML and extract enum values
enum_values = parse_mxfile(xml_content)

# Further processing or usage of enum_values can be done here
