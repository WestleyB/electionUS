import numpy as np
import pandas as pd
import pymongo
import json
from time import time

"""
client = pymongo.MongoClient("ec2-54-88-183-61.compute-1.amazonaws.com:27017",
                             27017, ssl=True, ssl_keyfile='aws_mongodb_key.pem')
"""
# client = pymongo.MongoClient("ec2-54-88-183-61.compute-1.amazonaws.com:27017")
start = time()
client = pymongo.MongoClient("localhost")

db = client.elections

collections = db.votes

cur_file = pd.read_csv("../data 2/2016-11-08-20-01_Alabama.txt",
                       header=None, sep=";", names=["time", "state", "name"])

print("import csv done")

cur_json = json.loads(cur_file.to_json(orient="records"))

collections.insert_many(cur_json)

print("import into mongodb done")

count = collections.count()
print("number of votes for Clinton: ", count)
end = time()
print(end - start)

print("all done")
