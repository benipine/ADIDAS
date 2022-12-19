#프로그램사용법
#python imgdtndb.py FILENAME
#현재 파일저장위치는 프로그램위치 / output/crop_imgpath 통해서 지정할 것

import cv2
import numpy as np
import sys
import sqlite3


if len(sys.argv)!=2:
    print("need an argument (image file)")
    sys.exit()

image_filename=sys.argv[1]
config_file='yolo/yolov3.cfg'
class_file='yolo/yolov3.txt'
weights_file='yolo/yolov3.weights'

config_file_d='yolo/yolo-drone.cfg'
weights_file_d='yolo/yolo-drone.weights'

detection_st=0

input_imgpath='fullimage/'
output_imgpath='fullimage/'
crop_imgpath='cropimage/'

conn = sqlite3.connect("adidas.db")
cur = conn.cursor()

cur.execute("SELECT count(*) FROM detection_data")
rows = cur.fetchall()
all_count = rows[0][0]

def db_insert(id_num, date, category, detail):
    cur.execute('INSERT INTO detection_data VALUES (?,?,?,?)',(id_num, date, category, detail)) 
    conn.commit()

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    
    add_space = int(Width/10) if Width>=Height else int(Height/10)
    a= x-add_space if x-add_space>0 else 0
    b= y-add_space if y-add_space>0 else 0
    c= x_plus_w+add_space if x_plus_w+add_space<Width else Width
    d= y_plus_h+add_space if y_plus_h+add_space<Height else Height
    cv2.imwrite(crop_imgpath+image_filename,img[b:d,a:c]) 

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    db_insert(10001+all_count,image_filename[0:14],str(classes[class_id]),'none')

    
image = cv2.imread(input_imgpath+image_filename)

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

classes = None

with open(class_file, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

classes_d = ['drone']

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

###

net = cv2.dnn.readNet(weights_file_d, config_file_d)

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4


for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])


indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    try:
        box = boxes[i]
    except:
        i = i[0]
        box = boxes[i]
    
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes_d)
    detection_st=1

cv2.imwrite(output_imgpath+image_filename, image)

if detection_st==1:
    conn.close()
    exit()

###

net = cv2.dnn.readNet(weights_file, config_file)

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4


for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])


indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    try:
        box = boxes[i]
    except:
        i = i[0]
        box = boxes[i]
    
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    if 4 in class_ids:
        if class_ids[i] == 4:
            draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes)
        else:
            continue
    else:
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes)
        break

    
cv2.imwrite(output_imgpath+image_filename, image)

conn.close()
