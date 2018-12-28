import cv2
import numpy as np
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


def mergeJson():
    img_dir_path = './wrong_labels/'
    paths = glob.glob(os.path.join(img_dir_path, '*'))
    # all_json ={}
    for path in paths:
        print(path)
        json_paths = glob.glob(os.path.join(path, 'via_region_data_*.json'))
        json_extend = {}
        for json_path in json_paths:
            annotations = json.load(open(json_path))
            for key, annotation in annotations.items():
                regions = annotation['regions']
                filename = annotation['filename']
                image_file_path = os.path.join(path, filename)
                if (len(regions) == 0):
                    try:
                        if os.path.exists(image_file_path):
                            os.remove(image_file_path)
                            # del annotations[key]
                            print('删除文件：' + str(image_file_path))
                    except  Exception as e:
                        print('文件删除失败：' + str(img_dir_path))
                else:
                    for region in regions:
                        region_attributes = region['region_attributes']
                        region_attributes['name'] = 'wrong'
                    new_image_name = path.split('/')[2] + '_' + filename
                    annotation['filename'] = new_image_name

                    new_image_path = os.path.join(path, new_image_name)
                    if os.path.exists(image_file_path):
                        file_size = int(os.path.getsize(image_file_path))
                        os.rename(image_file_path, new_image_path)
                    if os.path.exists(new_image_path):
                        file_size = int(os.path.getsize(new_image_path))
                    annotation['size'] = file_size
                    json_extend[new_image_name + str(file_size)] = annotation
        # all_json.update(json_extend)
        # json_extend.update(annotations)26 27 12 32 30 + 28
        print(len(json_extend))
        save_json(os.path.join(path, 'via_region_data.json'),
                  json_extend)


def resize():
    img_dir_path = './dataset'
    img_type = 'val'
    img_new = img_type + '_new'
    json_path = os.path.join(img_dir_path, img_type, 'via_region_data.json')
    json_extend = {}
    annotations = json.load(open(json_path))
    for key, annotation in annotations.items():
        regions = annotation['regions']
        filename = annotation['filename']
        image_file_path = os.path.join(img_dir_path, img_type, filename)
        try:
            if os.path.exists(image_file_path):
                image = cv2.imread(image_file_path, flags=cv2.IMREAD_COLOR)
                image = cv2.resize(image, None, fx=0.33, fy=0.33, interpolation=cv2.INTER_LINEAR)
                resize_image_path = os.path.join(img_dir_path, img_new, filename)
                cv2.imwrite(resize_image_path, image)
                file_size = int(os.path.getsize(resize_image_path))
            for region in regions:
                all_points_x = region['shape_attributes']['all_points_x']
                all_points_y = region['shape_attributes']['all_points_y']
                region['shape_attributes']['all_points_x'] = (
                (np.asarray(all_points_x) * 0.33).astype(int)).tolist()
                region['shape_attributes']['all_points_y'] = (
                (np.asarray(all_points_y) * 0.33).astype(int)).tolist()

            annotation['size'] = file_size
            json_extend[filename + str(file_size)] = annotation

        except  Exception as e:
            print('error：' + str(e))

    print(len(json_extend))
    save_json(
        os.path.join(img_dir_path, img_new, 'via_region_data.json'),
        json_extend)


if __name__ == '__main__':
    resize()
