from analytics import *
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt



folders_at = 'datafiles'
subfolders = [f.path for f in os.scandir(folders_at) if f.is_dir()]

def storevalues(maindirectory, databasename):

    p=security_and_login_information( maindirectory + '/security_and_login_information')
    print(json.dumps(p, indent=4, sort_keys=True))
    

for ele in subfolders:

    storevalues(ele, os.path.basename(ele));
