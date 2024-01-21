# Open the file in read mode
import hou
import platform

file_path = hou.getenv('NAS')+"/Houdini/env/houdini20.0/file.history"  # Replace with the actual path to your file

# Open and read the txt file
with open(file_path, "r") as f:
    txt = f.read()

# Split the txt by the section names
sections = txt.split("}\n")

# For each section, get the last line
for section in sections:
    # Split the section by the newline character
    lines = section.split("\n")
    # Get the last line
    if len(lines)>2:
        last_line = lines[-2]
        #print(lines)
        if lines[0]=="HIP":
            if platform.system()=='Linux':
                last_line = last_line.replace("Z:", "$NAS")
            if platform.system()=='Windows':
                last_line = last_line.replace("/mnt/NAS", "$NAS")
            hou.hipFile.load(last_line)
