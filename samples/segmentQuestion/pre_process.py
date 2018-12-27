import cv2
import numpy as np
import sys
import os
import glob
import json


def delete_file(image_path, annotations):
    file_name = ''.join(os.path.splitext(os.path.basename(image_path)))
    file_size = int(os.path.getsize(image_path))
    key = file_name + str(file_size)
    isExist = key in annotations.keys()
    if not isExist:
        os.remove(image_path)


def save_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def to_gray_image(path, img_dir_path):
    file_name = ''.join(os.path.splitext(os.path.basename(image_path)))

    # 读取图片
    image = cv2.imread(path, flags=cv2.IMREAD_COLOR)

    _, threshold = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)
    threshold = cv2.resize(threshold, None, fx=0.33, fy=0.33, interpolation=cv2.INTER_LINEAR)

    cv2.imwrite(os.path.join(img_dir_path, file_name), threshold,
                )
    # 质量压缩参数 [int(cv2.IMWRITE_JPEG_QUALITY), 5]


def getPositions(x, y, change, max):
    if x == change:
        change1 = x
        change2 = y
    if y == change:
        change1 = y
        change2 = x
    positions1 = []
    positions2 = []
    counts = np.random.randint(10, 20)
    unit = (max - change) / counts
    for i in range(counts):
        position1 = change1 + (i + 1) * unit + np.random.randint(-10, 10)
        if (position1 < max):
            positions1.append(int(position1))
            positions2.append(int(change2 + np.random.randint(1, 8)))
        else:
            break
    if x == change:
        return positions1, positions2
    if y == change:
        return positions2, positions1


img_dir_path = './dataset/val'
img_list = glob.glob(os.path.join(img_dir_path, 'original/*.jp*'))
print('处理图片数量:{}'.format(len(img_list)))

annotations = json.load(open(os.path.join(img_dir_path, "via_region_data.json")))
# annotations = list(annotations.values())  # don't need the dict keys
print(len(annotations))
# for image_path in img_list:
#     delete_file(image_path, annotations)

for image_path in img_list:
    to_gray_image(image_path, img_dir_path)

for annotation in annotations.values():
    regions = annotation['regions']
    for region in regions:
        shape_attributes = region['shape_attributes']
        region_attributes = region['region_attributes']
        region_attributes['name'] = 'MultipleChoices'
        shape_attributes['name'] = 'polygon'
        resize_scale = 0.32
        x = int(shape_attributes['x'] * resize_scale) - 1
        y = int(shape_attributes['y'] * resize_scale) - 1
        height = int(shape_attributes['height'] * resize_scale) - 1
        width = int(shape_attributes['width'] * resize_scale) - 1
        shape_attributes['all_points_x'] = []
        shape_attributes['all_points_y'] = []

        # xValues = [x, x + width, x + width, x]
        # yValues = [y, y, y + height, y + height]

        shape_attributes['all_points_x'].append(x)
        shape_attributes['all_points_y'].append(y)
        xPositions, yPositions = getPositions(x, y, x, x + width)
        shape_attributes['all_points_x'].extend(xPositions)
        shape_attributes['all_points_y'].extend(yPositions)

        shape_attributes['all_points_x'].append(x + width)
        shape_attributes['all_points_y'].append(y + np.random.randint(-10, 10))
        xPositions, yPositions = getPositions(x + width, y, y, y + height)
        shape_attributes['all_points_x'].extend(xPositions)
        shape_attributes['all_points_y'].extend(yPositions)

        shape_attributes['all_points_x'].append(x + width + np.random.randint(-10, 10))
        shape_attributes['all_points_y'].append(y + height + np.random.randint(-10, 10))
        xPositions, yPositions = getPositions(x, y + height, x, x + width)
        shape_attributes['all_points_x'].extend(reversed(xPositions))
        shape_attributes['all_points_y'].extend(reversed(yPositions))

        shape_attributes['all_points_x'].append(x + np.random.randint(-10, 10))
        shape_attributes['all_points_y'].append(y + height + np.random.randint(-10, 10))

        xPositions, yPositions = getPositions(x, y, y, y + height)
        shape_attributes['all_points_x'].extend(reversed(xPositions))
        shape_attributes['all_points_y'].extend(reversed(yPositions))

        # xPositions = []
        # yPositions = []
        # for i in range(counts):
        #     xPosition = x + np.random.randint(10, 50)
        #     if (xPosition < x + width):
        #         xPositions.append(xPosition)
        #         xPositions.extend()
        #         yPositions.append(y + np.random.randint(1, 8))

        # getMaskPositions(x, y)
        # getMaskPositions(x, y)
        # getMaskPositions(x, y)
        # getMaskPositions(x, y)

        # shape_attributes['all_points_x'] = [x, x + width, x + width, x]
        # shape_attributes['all_points_y'] = [y, y, y + height, y + height]

save_json(os.path.join(img_dir_path, 'via_region_data_0.json'), annotations)

# The VIA tool saves images in the JSON even if they don't have any
# annotations. Skip unannotated images.
# annotations = [a for a in annotations if a['regions']]

# Add images
# for a in annotations:
