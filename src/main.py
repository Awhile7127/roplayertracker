#!/bin/python

import argparse, sys, requests, json, time
from datetime import datetime

# Handle creating and parsing command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=""
    )

    parser.add_argument('-i', '--id', required=True)
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    return args


# MAKE A REQUEST TO THE ROBLOX WEB API ENDPOINT
def make_request(place_id):
    url = f"https://games.roblox.com/v1/games/{place_id}/servers/0"
    r = requests.get(url)
    if r.status_code != 200:
        print(r.status_code)
        return
    r = r.json()
    return r


# PARSE RETURNED JSON FOR PLAYER COUNT IN ALL SERVERS
def parse_json(jn):
    playing = 0

    if jn["data"] == []:
        playing = 0

    for obj in jn["data"]:
        playing += obj["playing"]

    return playing


# WRITE DATETIME AND PLAYER COUNT TO STRING
def format_as_csv(playing):
    now = datetime.now()
    dt_str = now.strftime("%Y/%m/%d %H:%M:%S")
    s = dt_str + "," + str(playing) + "\n"
    return s


# WRITE TO CSV FILE
def write_to_file(filename, s):
    obj = open(filename, "a")
    obj.write(s)


def main():
    args = parse_arguments()
    jn = make_request(args.id)
    playing = parse_json(jn)
    s = format_as_csv(playing)
    write_to_file(args.output, s)


main()
