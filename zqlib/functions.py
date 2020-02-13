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

# 2020-01-10: Assemble multiple images into one
def assemble_multiple_images(images, number_width=8, pad_index=True):
    import math
    images = np.asarray(images, dtype=np.uint8) # TxHxW for now
    img_h, img_w = images.shape[1:3]

    if len(images) % number_width != 0:
        number_mod = number_width - len(images) % number_width
        ph_images = np.zeros((number_mod, img_h, img_w))
        images = np.concatenate([images, ph_images], axis=0)
    number_images = len(images)
    number_group = int(number_images/number_width)

    if pad_index:
        for i in range(number_images):
            images[i] = cv2.putText(images[i],
                                "{:03d}".format(i),
                                (20, img_h-20),
                                cv2.FONT_HERSHEY_PLAIN,
                                2, 255, thickness=2)

    group_images = []
    for g in range(number_group):
        group_image = images[g*number_width:(g+1)*number_width]
        group_image = group_image.transpose((1, 0, 2))
        group_image = group_image.reshape((img_h, number_width*img_w))
        group_images.append(group_image)
    group_images = np.concatenate(group_images, axis=0)

    return group_images


