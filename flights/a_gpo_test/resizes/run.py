# 20180713

import os
import json
import csv
from datetime import date
from pprint import pprint
from collections import OrderedDict

FLIGHT_DATE = "071318"
FLIGHT_NAME = "a_gpo_{}".format(FLIGHT_DATE)
OFFER_FRAME_SIZES = ["160x600", "300x250", "300x600", "728x90", "320x50"]
END_FRAME_SIZES = ["160x600", "300x250", "300x600", "728x90"]
PRODUCT_FRAME_SIZES = {
    "img_160x600": ["160x600", ""],
    "img_300x250": ["300x250", ""],
    "img_300x600": ["300x600", ""],
    "img_728x90": ["728x90", ""],
    "img_2_728x90": ["728x90", "_logo"]
    }


def genrate_frame_obj(frame_name, isNeeded):
    """
        return personalized frame objects
    """
    if not isNeeded:
        frame_images = ["" for size in OFFER_FRAME_SIZES]
    else:
        # if frame_name == 'bopus' or frame_name == 'cc':
        #     format = ".jpg"
        # else:
        format = ".png"
        frame_images = [size + "_" + FLIGHT_NAME + "_" + frame_name + format for size in OFFER_FRAME_SIZES]

    return {
        "copy1": "",
        "img": frame_images
    }

def generate_end_frame_obj():
    """
        return object of end frames
    """
    return {
        "copy1": "",
        "img":{
            "fn_text1": ["" for size in END_FRAME_SIZES], #[size + "_" + FLIGHT_NAME + "_" + "fn_text1.png" for size in END_FRAME_SIZES],
            "fn_offer1": [size + "_" + FLIGHT_NAME + "_" + "fn_loy_offer.png" for size in END_FRAME_SIZES],
            "fn_offer2": [size + "_" + FLIGHT_NAME + "_" + "fn_non_offer.png" for size in END_FRAME_SIZES],
            "separator": [size + "_" + FLIGHT_NAME + "_" + "divider.png" for size in END_FRAME_SIZES]
        }
    }


def generate_assets(products, lifecycle):
    """
        Create asset array with all sizes of images for each product of lifecycle
    """
    assets = []
    for product in products:
        asset_obj = OrderedDict()
        asset_obj["id"] = product[0]
        asset_obj["division"] = lifecycle
        asset_obj["web_id"] = product[4]
        asset_obj["brand"] = product[3]
        asset_obj["category"] = product[2]
        for frame_key, size in PRODUCT_FRAME_SIZES.iteritems():
            if size[1].lower() == '_logo':
                asset_obj[frame_key] = size[0] + "_" + product[0] + size[1] + ".png"
            else:
                asset_obj[frame_key] = size[0] + "_" + product[0] + size[1] + ".jpg"
        asset_obj["style"] = None
        assets.append(asset_obj)
    return assets

def return_bool_rep(value):
    """
        Convert String representation to python boolean
    """
    return True if value.lower() == 'true' else False

def return_null_rep(value):
    """
        Convert String representation to python boolean
    """
    return None if value.lower() == 'null' else value

def build_nodes(loy_cold_prod, loy_hot_prod, nonloy_cold_prod, nonloy_hot_prod):
    """
        Create single audience/endnode and append to end feed
    """
    final_feed = {
        "data": []
    }
    loyalist_offer = [size+"_"+FLIGHT_NAME+"_loy_offer.png" for size in OFFER_FRAME_SIZES]
    nonloyalist_offer = [size+"_"+FLIGHT_NAME+"_non_offer.png" for size in OFFER_FRAME_SIZES]

    with open('end_node_map.csv', 'rU') as node_map_file:
        reader = csv.reader(node_map_file)
        reader.next()
        for row in reader:
            lifecycle = True if row[9].lower() == 'loyalist' else False
            isCold = return_bool_rep(row[15])
            node_obj = OrderedDict()
            node_obj["audience_id"] = row[0]
            node_obj["audience"] = row[0]
            node_obj["_id"] = "default"
            node_obj["reporting"] = row[10]
            node_obj["maxAssets"] = False if row[11].lower() == 'false' else int(row[11])
            node_obj["orderedRotation"] = return_bool_rep(row[12])
            node_obj["controls"] = OrderedDict({
                "staging": False,
                "loyalist": lifecycle,
                "frame_bopus": return_bool_rep(row[1]),
                "frame_y2y": return_bool_rep(row[2]),
                "frame_cc": return_bool_rep(row[3]),
                "frame_end": return_bool_rep(row[6]),
                "frame_cash": return_bool_rep(row[4]),
                "frame_cash_hf": return_bool_rep(row[14]),
                "frame_addtl": return_bool_rep(row[16]),
                "gallery_arrows": return_bool_rep(row[7])
            })
            node_obj["global"] = OrderedDict({
                "template": "A",
                 "images": {
                    "background1":  [size+"_"+FLIGHT_NAME+"_background1.jpg" for size in OFFER_FRAME_SIZES], #["" for size in OFFER_FRAME_SIZES],
                    "logo1": "logo.png",
                    "image1": {
                        "loyalist": loyalist_offer,
                        "nonloyalist": nonloyalist_offer
                    },
                        "gallery": {
                        "arrow_top": "",
                        "arrow_bottom": "",
                        "arrow_left": "",
                        "arrow_right": ""
                    }
                },
                "styles": {
                    "background1": "background-color: #167d9a;",
                    "cta1": "background-color: #000; color: #fff;"
                },
                "copy": {
                    "cta1": "SHOP NOW"
                },
                "clicktags": {
                    "clicktag1": "https://kohls.com/"
                }
            })
            node_obj["frames"] = {
                "frame_bopus" : genrate_frame_obj("bopus", True),
                "frame_y2y" : genrate_frame_obj("y2y", True),
                "frame_cc": genrate_frame_obj("cc", False),
                "frame_cash": genrate_frame_obj("cash", True),
                "frame_cash_hf": genrate_frame_obj("cash_hf", False),
                "frame_addtl": genrate_frame_obj("intro", False),
                "frame_end": generate_end_frame_obj()
            }
            if lifecycle:
                if isCold:
                    node_obj["assets"] = generate_assets(loy_cold_prod, 'loyalist_cold')
                else:
                    node_obj["assets"] = generate_assets(loy_hot_prod, 'loyalist_hot')
            else:
                if isCold:
                    node_obj["assets"] = generate_assets(nonloy_cold_prod, 'nonloyalist_cold')
                else:
                    node_obj["assets"] = generate_assets(nonloy_hot_prod, 'nonloyalist_hot')
            final_feed["data"].append(node_obj)

        with open('feed_{}.json'.format(FLIGHT_DATE), 'w') as outfile:
            json.dump(final_feed, outfile)
        return


def create_lol_non_json():
    """
        Create separate list of products
    """
    loyalist_cold_products = []
    loyalist_hot_products = []
    nonloyalist_cold_products = []
    nonloyalist_hot_products = []
    with open('product_map.csv', 'rU') as product_map_file:
        reader = csv.reader(product_map_file)
        reader.next()
        for row in reader:
            if row[1].lower() == 'loyalist':
                if row[5].lower() in ['cold', 'both']:
                    loyalist_cold_products.append(row)
                if row[5].lower() in ['hot', 'both']:
                    loyalist_hot_products.append(row)
            else:
                if row[5].lower() in ['cold', 'both']:
                    nonloyalist_cold_products.append(row)
                if row[5].lower() in ['hot', 'both']:
                    nonloyalist_hot_products.append(row)

    build_nodes(loyalist_cold_products, loyalist_hot_products, nonloyalist_cold_products, nonloyalist_hot_products)



if __name__ == "__main__":
    create_lol_non_json()