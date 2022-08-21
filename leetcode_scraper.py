#!/usr/bin/env python3

import os.path
from csv import reader, writer
from datetime import datetime as dt
from json import dump, load
from sys import argv
from time import time

from requests import get

st = time()


def getRanking(contest):

    API_URL_FMT = (
        "https://leetcode.com/contest/api/ranking/{}/?pagination={}&region=global"
    )
    page = 1
    total_rank = []
    retry_cnt = 0

    while True:

        try:

            url = API_URL_FMT.format(contest, page)
            resp = get(url).json()
            page_rank = resp["total_rank"]

            if not page_rank:
                break

            total_rank.extend(resp["total_rank"])
            print("Retrieved ranking from page {}. {} retrieved.".format(
                page, len(total_rank)))
            page += 1
            retry_cnt = 0

        except:

            print(
                f"Failed to retrieved data of page {page}...retry...{retry_cnt}"
            )
            retry_cnt += 1

    # discard and transform fields
    for rank in total_rank:

        rank.pop("contest_id", None)
        rank.pop("user_slug", None)
        rank.pop("country_code", None)
        rank.pop("global_ranking", None)
        finish_timestamp = rank.pop("finish_time", None)

        if finish_timestamp:
            rank["finish_time"] = dt.fromtimestamp(
                int(finish_timestamp)).isoformat()

    persistent_file = "{}.json".format(contest)
    print("Save retrieved ranking to {}".format(persistent_file))

    with open(persistent_file, "w") as fp:
        dump(total_rank, fp)


def main():

    if len(argv) < 2:
        print("Argument error")
        return

    contest_val = argv[1]
    csv_file = argv[2]
    getRanking(contest_val)
    print(csv_file)

    # Read data from CSV file username column and store it into an array
    users = []
    if os.path.exists(csv_file):
        with open(csv_file, "r") as fp:
            users = [row[0] for row in reader(fp)]

    print("USERNAME OF THE USERS ARE", users)

    # Open a json file and write its contents to a CSV
    with open("{}.json".format(contest_val), "r") as fp:
        contests = load(fp)

    # Fix cp950 chinese write row issue
    with open("{}.csv".format(contest_val), "w", encoding="UTF-8") as fp:

        writ = writer(fp)
        arr = [
            "username",
            "username_color",
            "user_badge",
            "country_name",
            "rank",
            "score",
            "data_region",
            "finish_time",
        ]
        writ.writerow(arr)

        # If filter users not found, write all users to csv
        final = contests
        if users:
            final = [
                contest for contest in contests if contest["username"] in users
            ]

        # Sort final by rank
        final.sort(key=lambda c: c["rank"])

        for contest in final:
            try:
                writ.writerow([contest.get(i, "") for i in arr])
            except Exception as exc:
                print(exc)
        print("COMPLETED WRITING TO CSV")


if __name__ == "__main__":
    main()
    et = time()
    print("Execution time in seconds: {}".format(et - st))
