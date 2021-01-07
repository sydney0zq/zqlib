#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 qiang.zhou <qiang.zhou@Macbook>
#
# Distributed under terms of the MIT license.

"""

"""
import cv2
import numpy as np
import os


__all__ = ['imgs2vid', 'readvdnames', 'gray2rgb', 'assemble_multiple_images',
           'overlay_mask', 'list_to_file', 'mkdirs']

# 2020-01-09: imgs have been read as a TxHxW array
def imgs2vid(imgs, output_fn="test.avi", fps=5, w_index=True):
    import cv2
    import numpy as np
    imgs = np.asarray(imgs)
    if imgs.ndim == 3:
        _, height, width = imgs.shape
    elif imgs.ndim == 4:
        _, height, width, channels = imgs.shape
        assert channels == 3, "The number of channel (dim==3) must be 3..."
    else:
        assert False, "Invalid ndarray with the shape of {}...".format(imgs.shape)

    video_handler = cv2.VideoWriter(output_fn, cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height), isColor=False)
    for i, img in enumerate(imgs):
        img = np.uint8(img)
        img = cv2.putText(img, "{:03d}".format(i), (20, height-20),
                     cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        video_handler.write(img)
    cv2.destroyAllWindows()
    video_handler.release()

# 2020-01-02: Dump images of TxHxW to debug directory
dumpimgs = lambda x, p: [cv2.imwrite("debug/{}_{:05d}.png".format(p, i), xi) for i, xi in enumerate(x)]

# 2020-01-02: Read txt files into a list
readvdnames = lambda x: open(x).read().rstrip().split('\n')

def gray2rgb(img):
    if len(img.shape) == 2:
        rgb = np.stack((img,)*3, axis=-1)
    elif len(img.shape) == 3 and img.shape[2] == 1:
        rgb = np.repeat(img, 3, 2)
    else:
        assert False, "img {} not supported...".format(img.shape)
    return rgb

# 2020-06-19: Add support for gray image
# 2020-06-04: Update tag
def assemble_multiple_images(images, number_width=8, tags=None):
    for i, image in enumerate(images):
        if len(image.shape) == 2 or image.shape[2] == 1:
            images[i] = gray2rgb(image)

    images = np.asarray(images, dtype=np.uint8) # TxHxWxC for now
    img_h, img_w = images.shape[1:3]
    
    if len(images) % number_width != 0:
        number_mod = number_width - len(images) % number_width
        ph_images = np.zeros((number_mod, img_h, img_w))
        images = np.concatenate([images, ph_images], axis=0)
    number_images = len(images)
    number_group = int(number_images/number_width)

    if tags is not None:
        for i, tag in enumerate(tags):
            images[i] = cv2.putText(images[i], tag, (20, img_h-20), 
                                    cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=2, color=(0, 0, 255), thickness=2)

    group_images = []

    for g in range(number_group):
        group_image = images[g*number_width:(g+1)*number_width]
        group_image = group_image.transpose((1, 0, 2, 3))
        group_image = group_image.reshape((img_h, number_width*img_w, -1))
        group_images.append(group_image)
    group_images = np.concatenate(group_images, axis=0)

    return group_images


# Version: 2019-09-02, add elegant countours display
def overlay_mask(image, mask, countour_value=128, alpha=0.5):
    from scipy.ndimage.morphology import binary_erosion, binary_dilation

    image, dtype = image.copy(), image.dtype
    label_colours = [[0, 0, 0], [255, 0, 0], [0, 255, 0], [255, 255, 0], [0, 0, 255], 
                     [255, 0, 255], [0, 255, 255], [128, 128, 128], [64, 0, 0], 
                     [191, 0, 0], [64, 128, 0], [191, 128, 0], [64, 0, 128], 
                     [191, 0, 128], [64, 128, 128], [191, 128, 128], [0, 64, 0], 
                     [128, 64, 0], [0, 191, 0], [128, 191, 0], [0, 64, 128], [128, 64, 128]]

    indices = np.unique(mask)
    for cls_index in indices:
        if cls_index != 0:
            mask_index = mask == cls_index
            cls_color = label_colours[cls_index]
            image[mask_index, :] = image[mask_index, :]*alpha + np.array(cls_color)*(1-alpha)
            countours = binary_dilation(mask_index) ^ mask_index
            image[countours, :] = countour_value
    return image.astype(dtype)

# 2020-08-13: mkdirs
mkdirs = lambda x: os.makedirs(x, exist_ok=True)

# 2020-06-07: Write a list object to file (without the last newline)
def list_to_file(id_list, fn):
    with open(fn, "w") as f:
        f.write("\n".join(id_list))






