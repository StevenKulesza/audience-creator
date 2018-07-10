# 20180713

import os
import json
import csv
from datetime import date
from pprint import pprint
from collections import OrderedDict

FLIGHT_DATE = "071318"
FLIGHT_NAME = "a_gpo_{}".format(FLIGHT_DATE)
IMAGE_PATH = "https://dev-kohls-feed.moxhost.com/images/{}/".format(FLIGHT_NAME)
PRODUCT_FRAME_SIZES = {
    "img_160x600": ["160x600", ""],
    "img_300x250": ["300x250", ""],
    "img_300x600": ["300x600", ""],
    "img_728x90": ["728x90", ""],
    "img_2_728x90": ["728x90", "_logo"]
    }


def generate_assets(all_assets):
    """
        Create asset array with all sizes of images for each product of lifecycle
    """

    assets = {}
    for lifecycle, products in all_assets.iteritems():
        assets[lifecycle] = []
        for product in products:
            asset_obj = OrderedDict()
            asset_obj["id"] = product[0]
            asset_obj["division"] = product[1]
            asset_obj["web_id"] = product[4]
            asset_obj["brand"] = product[3]
            asset_obj["category"] = product[2]
            for frame_key, size in PRODUCT_FRAME_SIZES.iteritems():
                if size[1].lower() == '_logo':
                    asset_obj[frame_key] = IMAGE_PATH + size[0] + "_" + product[0] + size[1] + ".png"
                else:
                    asset_obj[frame_key] = IMAGE_PATH + size[0] + "_" + product[0] + size[1] + ".jpg"
            asset_obj["style"] = None
            assets[lifecycle].append(asset_obj)
    import json
    with open('assets.json', 'w') as outfile:
        json.dump(assets, outfile)



def create_lol_non_json():
    """
        Create separate list of products
    """
    all_assets= {
        'loyalist_cold_products' : [],
        'loyalist_hot_products' : [],
        'nonloyalist_cold_products' : [],
        'nonloyalist_hot_products' : []
    }

    with open('product_map.csv', 'rU') as product_map_file:
        reader = csv.reader(product_map_file)
        reader.next()
        for row in reader:
            if row[1].lower() == 'loyalist':
                if row[5].lower() in ['cold', 'both']:
                    all_assets['loyalist_cold_products'].append(row)
                if row[5].lower() in ['hot', 'both']:
                    all_assets['loyalist_hot_products'].append(row)
            else:
                if row[5].lower() in ['cold', 'both']:
                    all_assets['nonloyalist_cold_products'].append(row)
                if row[5].lower() in ['hot', 'both']:
                    all_assets['nonloyalist_hot_products'].append(row)

    generate_assets(all_assets)



if __name__ == "__main__":
    create_lol_non_json()
