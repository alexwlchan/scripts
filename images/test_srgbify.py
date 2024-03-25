import filecmp
import pathlib

from PIL import Image

from srgbify import convert_image_to_srgb


def test_it_ignores_an_image_which_is_already_srgb():
    """
    If an image is already in sRGB, we don't need to do anything.

    This image was downloaded from https://webkit.org/blog-files/color-gamut/
    """
    im = Image.open("images/examples/Shoes-sRGB.jpg")

    assert convert_image_to_srgb(im) is None


def test_it_converts_a_display_p3_image_to_srgb(tmp_path):
    """
    If an image is in Display P3, it gets converted to sRGB.

    This image was downloaded from https://webkit.org/blog-files/color-gamut/
    """
    im = Image.open("images/examples/Iceland-P3.jpg")

    new_im = convert_image_to_srgb(im)

    new_im.save(tmp_path / "Iceland-sRGB-actual.jpg")

    assert filecmp.cmp(
        tmp_path / "Iceland-sRGB-actual.jpg",
        "images/examples/Iceland-sRGB-expected.jpg",
        shallow=False,
    )


def test_it_preserves_transparency_in_png_images():
    """
    If an image is a PNG with transparency, that gets preserved when converting
    to sRGB.

    This image is a screenshot from my own computer.
    """
    im = Image.open("images/examples/screenshot-with-transparency.png")

    new_im = convert_image_to_srgb(im)

    assert new_im.mode == "RGBA"

    # The top left-hand corner should be transparent
    assert new_im.getpixel((0, 0)) == (0, 0, 0, 0)


def test_it_converts_images_with_a_grey_profile():
    """
    If an image has a grey colour profile, that gets converted to sRGB.

    This image is from https://www.flickr.com/photos/lselibrary/3925727501/
    """
    im = Image.open("images/examples/3925727501_6aa7c94c10_w.jpg")

    new_im = convert_image_to_srgb(im)

    assert new_im.mode == "RGB"


def test_it_preserves_rotation_from_exif_orientation(tmp_path: pathlib.Path):
    """
    This is based on a photo exported from my Apple Photos Library
    which was rotated by 90 degrees upon transformation.

    This was caused by an image with an EXIF orientation tag that was
    being stripped on save.  I found a solution in the Pillow issue tracker.

    See https://github.com/alexwlchan/scripts/issues/21
    See https://github.com/python-pillow/Pillow/issues/4703
    """
    im = Image.open("images/examples/taylorswift.jpg")

    new_im = convert_image_to_srgb(im)

    assert new_im.size == (3024, 4032)
