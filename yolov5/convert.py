import os
import xml.etree.ElementTree as ET

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_file, txt_file, classes):
    in_file = open(xml_file)
    out_file = open(txt_file, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(f"{cls_id} " + " ".join([str(a) for a in bb]) + '\n')

classes = ["cat", "dog","monkey"]  # Update with your class names
xml_folder = 'dataset/animal_test_train/test'
txt_folder = 'dataset/animal_test_train/test'

if not os.path.exists(txt_folder):
    os.makedirs(txt_folder)

for xml_file in os.listdir(xml_folder):
    if xml_file.endswith('.xml'):
        txt_file = os.path.join(txt_folder, os.path.splitext(xml_file)[0] + '.txt')
        convert_annotation(os.path.join(xml_folder, xml_file), txt_file, classes)
