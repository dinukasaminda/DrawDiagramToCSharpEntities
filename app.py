import xml.etree.ElementTree as ET
import os
from math import inf


# Define a class to hold the object details
class DiagramObject:
    def __init__(self, obj_id, value, x, y, width, height, fill_color):
        self.obj_id = obj_id
        self.value = value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color

    def __repr__(self):
        return f"DiagramObject(id={self.obj_id}, value={self.value}, x={self.x}, y={self.y}, width={self.width}, height={self.height}, fillColor={self.fill_color})"

def parseIntOrNone(value):
    try:
        return int(value)
    except:
        return None
# Function to parse the XML and extract the required details
def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    diagram_objects = []

    # Iterate over all mxCell elements
    for cell in root.findall(".//mxCell"):
        obj_id = cell.attrib.get("id")
        value = cell.attrib.get("value")
        style = cell.attrib.get("style")
        geometry = cell.find("mxGeometry")

        if geometry is not None:
            x = parseIntOrNone(geometry.attrib.get("x"))
            y = parseIntOrNone(geometry.attrib.get("y"))
            width = parseIntOrNone(geometry.attrib.get("width"))
            height = parseIntOrNone(geometry.attrib.get("height"))
        else:
            x, y, width, height = None, None, None, None

        # Extract fillColor from the style attribute if it exists
        fill_color = None
        if style:
            styles = style.split(";")
            for s in styles:
                if "fillColor" in s:
                    fill_color = s.split("=")[1]
                    break

        if obj_id and value:
            diagram_object = DiagramObject(obj_id, value, x, y, width, height, fill_color)
            diagram_objects.append(diagram_object)

    return diagram_objects

# Function to calculate the minimum distance between two diagram objects
def calculate_distance(obj1, obj2):

    if obj1.x is None or obj1.y is None or obj1.width is None or obj1.height is None:
        return inf
    
    if obj2.x is None or obj2.y is None or obj2.width is None or obj2.height is None:
        return inf

    # Horizontal distance
    if obj1.x + obj1.width < obj2.x:
        horizontal_distance = obj2.x - (obj1.x + obj1.width)
    elif obj2.x + obj2.width < obj1.x:
        horizontal_distance = obj1.x - (obj2.x + obj2.width)
    else:
        horizontal_distance = 0

    # Vertical distance
    if obj1.y + obj1.height < obj2.y:
        vertical_distance = obj2.y - (obj1.y + obj1.height)
    elif obj2.y + obj2.height < obj1.y:
        vertical_distance = obj1.y - (obj2.y + obj2.height)
    else:
        vertical_distance = 0

    # The minimum distance between objects is the larger of the two distances
    return max(horizontal_distance, vertical_distance)

# Function to cluster objects based on distance threshold
def cluster_objects(objects, max_distance):
    clusters = []
    visited = set()

    def bfs(start_index):
        queue = [start_index]
        cluster = []
        visited.add(start_index)

        while queue:
            current_index = queue.pop(0)
            current_obj = objects[current_index]
            cluster.append(current_obj)

            # Check all other objects
            for i in range(len(objects)):
                if i not in visited:
                    distance = calculate_distance(current_obj, objects[i])
                    if distance <= max_distance:
                        visited.add(i)
                        queue.append(i)
        
        return cluster

    for i in range(len(objects)):
        if i not in visited:
            cluster = bfs(i)
            clusters.append(cluster)

    return clusters

# Example XML data
xml_data = ""

# Read the XML data from the file
file_path = os.path.join(os.path.dirname(__file__), "ERD-v1.drawio.xml")

# read as utf-8
with open(file_path, "r", encoding="utf-8") as file:
    xml_data = file.read()

# Parse the XML and create the list of objects
diagram_objects = parse_xml(xml_data)

# # Print the list of diagram objects
# for obj in diagram_objects:
#     print(obj)

# Cluster the objects based on a maximum distance of 4 units
max_distance = 4
clusters = cluster_objects(diagram_objects, max_distance)


outputText = ""
# Print the clusters
for cluster_index, cluster in enumerate(clusters):
    if len(cluster) < 2:
        continue
    outputText+=f"Cluster {cluster_index + 1}:\n"
    mainObj = cluster[0]
    outputText+=f"TableName:  {mainObj.value}\n"
    for  obj in cluster[1:]:
        outputText+=f"Column:  {obj.value}\n"

# save file 
with open('output.txt', 'w') as f:
    f.write(outputText)