import zipfile
import sys,os
from pymongo import MongoClient
from analytics import *
import time
folder = 'zipfiles'
extension = ".zip"
connection=MongoClient()
folders_at = 'zipfiles'
subfolders = [f.path for f in os.scandir(folders_at) if f.is_dir()]

for item in os.listdir(folder):
	if item.endswith(extension):
		zip_ref = zipfile.ZipFile(folder+'/'+item)
		zip_ref.extractall("zipfiles/") # extract file to dir
		zip_ref.close() # close file
 


def storevalues(maindirectory, databasename):
    db = connection[databasename]

    connection.drop_database(databasename)
    apps_and_websites1 = db['apps_and_websites']
    apps_and_websites1.insert(apps_and_websites(maindirectory + '/apps_and_websites'))

    profile_information1 = db['profile_information']
    profile_information1.insert(profile_information(maindirectory + '/profile_information'))


    calls_and_messages1 = db['calls_and_messages']
    calls_and_messages1.insert(calls_and_messages(maindirectory + '/calls_and_messages'))

    likes_and_reactions1 = db['likes_and_reactions']
    likes_and_reactions1.insert(likes_and_reactions(maindirectory + '/likes_and_reactions'))

    friends1 = db['friends']
    friends1.insert(friends(maindirectory + '/friends'))

    search_history1 = db['search_history']
    search_history1.insert(search_history(maindirectory + '/search_history'))

    messages1 = db['messages']
    messages1.insert(messages(maindirectory + '/messages'))

    videos1 = db['videos']
    videos1.insert(videos(maindirectory + '/videos'))

    saved_items1 = db['saved_items']
    saved_items1.insert(saved_items(maindirectory + '/saved_items'))

    ads1 = db['ads']
    ads1.insert(ads(maindirectory + '/ads'))

    about1 = db['Contact_Information']
    about1.insert(about_you(maindirectory + '/about_you'))


    profile1 = db['Profile_information']
    profile1.insert(profile_information(maindirectory + '/profile_information'))



    pay1 = db['Payment_information']
    pay1.insert(payment_history(maindirectory + '/payment_history'))

    event1 = db['Event_info']
    event1.insert(events(maindirectory + '/events'))

    follow1 = db['Following_details']
    follow1.insert(following_and_followers(maindirectory + '/following_and_followers'))

    group1 = db['groups']
    group1.insert(groups(maindirectory + '/groups'))

    otheractivity = db['other_activity']
    otheractivity.insert(other_activity(maindirectory + '/other_activity'))

    sec1 = db['security_and_login_info']
    sec1.insert(security_and_login_information(maindirectory + '/security_and_login_information'))

    pages1=db['pages']
    pages1.insert(pages(maindirectory + '/pages'))
    comments1 = db['comments']
    comments1.insert(comments(maindirectory + '/comments'))

cols = connection.database_names()
for ele in subfolders:
    
   if os.path.basename(ele) not in cols:
     storevalues(ele, os.path.basename(ele));
     print("hey")


# print(cols)
