"""
Usage:
    python3 exercise1.py <FILEPATH>
"""

import json
import sys
import yaml


def validate_json(path):
    try:
        with open(path) as ldfile:
            opfile = json.load(ldfile)
            return opfile
    except Exception as ErrVal:
        print(ErrVal)

def set_age_to_bucket_range(age, bucranges):
    for bucrange in bucranges:
        if age >= int(bucrange.split("_")[1].split("-")[0]) and age < int(bucrange.split("_")[1].split("-")[1]):
            return bucrange
        elif age > int(bucrange.split("_")[1].split("-")[0]) and age <= int(bucrange.split("_")[1].split("-")[1]):
            return bucrange

def create_bucket_ranges(bucketlist):
    buckets = bucketlist
    buckarray = {}
    itrbuckets = 0
    for buck in buckets:
        if itrbuckets == 0:
            itrbuckets += 1
            continue
        else:
            buckarray['bucket_' + str(buckets[itrbuckets - 1]) + '-' + str(buck)] = {}
            itrbuckets += 1
    return buckarray

def fill_the_buckets(jdata):
    sortedbuckets = (jdata["buckets"])
    sortedbuckets.sort()
    ppl_hash = sorted((jdata["ppl_ages"]).items(), key=lambda x: x[1])
    if ppl_hash[0][1] < sortedbuckets[0]:
        sortedbuckets.insert(0, ppl_hash[0][1])
    if ppl_hash[len(ppl_hash)-1][1] > sortedbuckets[len(sortedbuckets)-1]:
        sortedbuckets.insert(len(sortedbuckets), ppl_hash[len(ppl_hash)-1][1])
    bucketranges = create_bucket_ranges(sortedbuckets)
    yamlcol = {}
    for name, age in ppl_hash:
        appendbucket = set_age_to_bucket_range(age, bucketranges)
        yamlcol.setdefault(appendbucket, []).append(name)
    wrfile = open('exercise1.yaml', 'w')
    yaml.dump(yamlcol, wrfile, default_flow_style=False, allow_unicode=True)
    wrfile.close()

def main(path):
    fill_the_buckets(validate_json(path))

if __name__ == '__main__':
    main(sys.argv[1])
