#!/usr/bin/env python3
"""
Creates a square crop of an image.
"""

import pathlib
import sys

from PIL import Image


if __name__ == '__main__':
    try:
        path = pathlib.Path(sys.argv[1])
    except IndexError:
        sys.exit(f"Usage: {__file__} IMAGE_PATH")
    
    im = Image.open(path)
    
    out_path = path.with_suffix(".square" + path.suffix)
    assert out_path != path
    
    if im.width == im.height:
        print(path)
    elif im.width > im.height:
        left = (im.width - im.height) / 2
        upper = 0
        right = im.width - (im.width - im.height) / 2
        lower = im.height
        
        crop_im = im.crop((left, upper, right, lower))
        crop_im.save(out_path)
        print(out_path)
    elif im.height > im.width:
        left = 0
        upper = (im.height - im.width) / 2
        right = im.width
        lower = im.height - (im.height - im.width) / 2
        
        crop_im = im.crop((left, upper, right, lower))
        crop_im.save(out_path)
        print(out_path)
    
    
    # main()