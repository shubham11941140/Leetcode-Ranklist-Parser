
#!/usr/bin/env python3

import time

st = time.time()

import argparse
import datetime
import json
import os
import requests
import sys
import csv

def getRanking(contest):
    API_URL_FMT = 'https://leetcode.com/contest/api/ranking/{}/?pagination={}&region=global'
    page = 1
    total_rank = []
    retry_cnt = 0
    while True:
        try:
            url = API_URL_FMT.format(contest, page)
            resp = requests.get(url).json()
            #print(requests.get(url).content)
            page_rank = resp['total_rank']
            if (0 == len(page_rank)):
                break
            total_rank.extend(resp['total_rank'])
            print('Retrieved ranking from page {}. {} retrieved.'.format(page, len(total_rank)))
            page += 1
            retry_cnt = 0
        except:
            print(f'Failed to retrieved data of page {page}...retry...{retry_cnt}')
            retry_cnt += 1

    # discard and transform fields
    for rank in total_rank:
        rank.pop('contest_id', None)
        rank.pop('user_slug', None)
        rank.pop('country_code', None)
        rank.pop('global_ranking', None)
        finish_timestamp = rank.pop('finish_time', None)
        if finish_timestamp:
            rank["finish_time"] = datetime.datetime.fromtimestamp(int(finish_timestamp)).isoformat()

    persistent_file = '{}.json'.format(contest)
    print('Save retrieved ranking to {}'.format(persistent_file))
    with open(persistent_file, 'w') as fp:
        json.dump(total_rank, fp)

def getContestInfo(contest):
    def unSlug(slug):
        return ' '.join([ w.capitalize() for w in slug.split('-') ])

    def isNew(contests, newContest):
        for c in contests:
            if newContest['title'] == c['title']:
                return False
        return True

    while True:
        try:
            CONTEST_INFO_API_URL_FMT = 'https://leetcode.com/contest/api/info/{}/'
            resp = requests.get(CONTEST_INFO_API_URL_FMT.format(contest)).json()
            startTimestamp = int(resp['contest']['start_time'])
            break
        except:
            print('Failed to retrieved contest info...retry...')

    newContest = {
        "title": unSlug(contest),
        "slug": contest,
        "startTime": startTimestamp
    }

    if os.path.exists('contests.json'):
        with open('contests.json', 'r') as fp:
            contests = json.load(fp)
    else:
        contests = []

    if isNew(contests, newContest):
        contests.append(newContest)
        contests.sort(key=lambda c : c['startTime'], reverse = True)

    with open('contests.json', 'w+') as fp:
        json.dump(contests, fp)


def main():
    #parser = argparse.ArgumentParser(description='Leetcode ranking crawler')
    #parser.add_argument('contest', help='contest slug (ex: weekly-contest-178)')
    # Add parser argument to take input from csv file as argument
    #parser.add_argument('-f', '--file', help='input file')
    #args = parser.parse_args()
    contest_val = sys.argv[1]
    csv_file = sys.argv[2]
    getRanking(contest_val)
    #csv_file = args.file
    print(csv_file)

    # Read data from CSV file username column and store it into an array
    with open(csv_file, 'r') as fp:
        reader = csv.reader(fp)
        users = [ row[0] for row in reader ]
    print("USERNAME OF THE USERS ARE", users)

    #getContestInfo(args.contest)
    # Open a json file and write its contents to a CSV
    with open('{}.json'.format(contest_val), 'r') as fp:
        contests = json.load(fp)
    with open('{}.csv'.format(contest_val), 'w') as fp:
        writer = csv.writer(fp)
        arr = ['username', 'username_color', 'user_badge', 'country_name', 'rank', 'score', 'data_region', 'finish_time']
        writer.writerow(arr)
        final = []
        for contest in contests:
            #print("CONTEST VALUE IS", contest['username'])
            if contest['username'] in users:
                final.append(contest)
                #writer.writerow([contest[i] for i in arr])
        #print("FINAL VALUE IS", final)
        # Sort final by rank
        final.sort(key=lambda c : c['rank'])
        for contest in final:
            writer.writerow([contest[i] for i in arr])
    print("COMPLETED WRITING TO CSV")



if __name__ == "__main__":
    main()
    et = time.time()
    print("Execution time: {}".format(et - st))
