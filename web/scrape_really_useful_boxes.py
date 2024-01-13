#!/usr/bin/env python3
"""
Scrape the Really Useful Boxes catalogue, in particular their product page
at https://www.reallyusefulproducts.co.uk/uk/html/onlineshop/fullrange_rub.php

This sucks down information about the dimension of the boxes, which
I use to do searches of boxes that need to fit into specific spaces,
e.g. boxes that are between 20 and 30cm wide.  It creates a SQLite
database that I throw into datasette.

See https://social.alexwlchan.net/@alex/111750446474991705
"""

from collections.abc import Iterator
import time
from typing import TypedDict
from urllib.parse import urljoin

import bs4
import httpx
from sqlite_utils import Database
import tqdm


client = httpx.Client()


def get_soup(url: str) -> bs4.BeautifulSoup:
    """
    Fetch the contents of a URL, parse it as HTML, and return the parsed soup.
    """
    resp = client.get(url)
    resp.raise_for_status()

    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    return soup


def get_product_page_urls() -> Iterator[str]:
    """
    Generate URLs to individual product pages.
    """
    base_url = (
        "https://www.reallyusefulproducts.co.uk/uk/html/onlineshop/fullrange_rub.php"
    )

    soup = get_soup(base_url)

    # The page is arranged something like:
    #
    #     <ul class="productgallery">
    #     <li>
    #       <form action="https://www.romancart.com/cart.asp" method="post">
    #         <a href="./rub/b00_07litre.php">
    #           <img src="…">
    #           0.07 litre<br>Really Useful Box
    #         </a>
    #         …
    #     </li>
    #
    product_gallery = soup.find("ul", attrs={"class": "productgallery"})

    for li_elem in product_gallery.find_all("li"):
        link = li_elem.find("a")

        if link is None:
            continue

        name = link.text

        if "Really Useful Box" not in name:
            continue

        if any(
            w in name.lower()
            for w in {"tray", "set", "pack", "bauble insert", "bonus pack"}
        ):
            continue

        yield urljoin(base_url, link.attrs["href"])


class BoxInfo(TypedDict):
    image_url: str
    url: str
    name: str
    length: int
    width: int
    depth: int


def get_box_info(url: str) -> BoxInfo:
    soup = get_soup(url)

    name = soup.find("h2").text

    # The dimensions are in a single paragraph like:
    #
    #     <p><em class="type1">Dimensions</em><br>
    #     External: 120 x 85 x 45<br>
    #     Internal: 90 x 65 x 32<br>
    #     (length x width x depth in mm)</p>
    #
    dimensions = next(p for p in soup.find_all("p") if "Dimensions" in p.text)

    lines = dimensions.text.splitlines()
    assert len(lines) == 4
    assert lines[0].startswith("Dimensions")
    assert lines[-1] == "(length x width x depth in mm)"
    assert lines[1].startswith("External: ")
    length, width, depth = lines[1].replace("External: ", "").split(" x ")
    length = int(length.split()[0].replace(",", ""))
    width = int(width.split()[0].replace(",", ""))
    depth = int(depth.split()[0].replace(",", ""))

    image_url = urljoin(url, soup.find("img", attrs={"class": "rhsimage"}).attrs["src"])

    # The order of this dict will become the order of columns in
    # the SQLite database, which in turn will be used by datasette --
    # make it the convenient order for viewing.
    return {
        "image_url": image_url,
        "name": name,
        "length": length,
        "width": width,
        "depth": depth,
        "url": url,
    }


if __name__ == "__main__":
    db = Database("really_useful_boxes.db")

    product_urls = list(get_product_page_urls())

    for url in tqdm.tqdm(product_urls):
        db["boxes"].insert(get_box_info(url))

        # This is to avoid getting rate-limited or upsetting the website
        time.sleep(1)
