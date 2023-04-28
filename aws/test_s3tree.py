from s3tree import build_s3_tree, S3Folder


def test_builds_a_tree_of_top_level_objects():
    keys = ["cat.jpg", "dog.png", "emu.gif"]

    tree = build_s3_tree(keys)
    assert tree == S3Folder(objects=["cat.jpg", "dog.png", "emu.gif"], path="")


def test_builds_a_tree_with_a_single_folder():
    keys = ["cat.jpg", "colours/blue.txt", "colours/green.txt", "colours/red.txt"]

    tree = build_s3_tree(keys)
    assert tree == S3Folder(
        objects=["cat.jpg"],
        folders={
            "colours": S3Folder(
                objects=["blue.txt", "green.txt", "red.txt"],
                path="colours",
            )
        },
        path="",
    )


def test_builds_a_tree_with_nested_folders():
    keys = [
        "cat.jpg",
        "colours/blue.txt",
        "colours/green.txt",
        "colours/red.txt",
        "shapes/triangle.png",
        "shapes/circle.txt",
        "shapes/quadrilaterals/square.txt",
        "shapes/quadrilaterals/rectangle.txt",
    ]

    tree = build_s3_tree(keys)
    assert tree == S3Folder(
        objects=["cat.jpg"],
        folders={
            "colours": S3Folder(
                objects=["blue.txt", "green.txt", "red.txt"],
                path="colours",
            ),
            "shapes": S3Folder(
                objects=["circle.txt", "triangle.png"],
                folders={
                    "quadrilaterals": S3Folder(
                        objects=["rectangle.txt", "square.txt"],
                        path="shapes/quadrilaterals",
                    )
                },
                path="shapes",
            ),
        },
        path="",
    )
