import os.path
##os.system('pip install pygeoip')
##os.system('pip install opencv-python')
import json
import pygeoip
import inspect
#face_cascade = cv.CascadeClassifier('C:\Users\Nayan\Desktop\haarcascade_frontalface_alt.xml')
from collections import Counter
import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)

from datetime import datetime



def getnamefromnumber(number,directory):

    maindirectory = os.path.dirname(directory)
    data=json.load(open(maindirectory+'/about_you/your_address_books.json'))
    name1=None
    try:
        for i in range(0, len(data["address_book"]["address_book"])):
                    if data["address_book"]["address_book"][i]["details"][0]["contact_point"]==number:
                        name1 = data["address_book"]["address_book"][i]["name"]
    except:
        pass
    return name1
                # #print(region_code_for_country_code(pn.country_code))

def getfriendlist(directory):
    maindirectory = os.path.dirname(directory)
    friends = json.load(open(maindirectory + '/friends' + '/friends.json'))
    #print(len(friends['friends']))
    friendlist = []
    try:
        for i in range(0, len(friends['friends'])):
            friendlist.append(friends['friends'][i]['name'])
    except:
        pass;
    return friendlist;

def find_words(text, search):
    """Find exact words"""
    dText   = text.split()
    dSearch = search.split()

    found_word = 0

    for text_word in dText:
        for search_word in dSearch:
            if search_word == text_word:
                found_word += 1

    if found_word == len(dSearch):
        return True
    else:
        return False
#1
def security_and_login_information(directory):

    jsonfiles = common(directory)
    #print(jsonfiles)
    citysforactivity=[]
    countrycodesforactivity=[]
    status_changes=""
    for ele in jsonfiles:
        data=json.load(open(ele))
        #print(data)
        if 'account_activity' in data.keys():
                    #print('len of account activity is'+str(len(data['account_activity'])))
                    for activity in data['account_activity']:
                        ip = activity['ip_address']
                        try:
                            data = rawdata.record_by_name(ip)
                            citysforactivity.append( data['city'])
                            countrycodesforactivity.append(data['country_name'])
                            ##print countrycodesforactivity
                        except:
                            # #print 'invalid ip  :'+ ip
                            pass;
                    citysforactivity=dict(Counter(citysforactivity))
                    #print ('citys with activity in: '+str(citysforactivity))
                    countrycodesforactivity = dict(Counter(countrycodesforactivity))
                    #print ('countries with activity in: '+str(countrycodesforactivity))
        # if 'account_status_changes' in data.keys():
        #     pass

        adminchangescity=[]
        adminchangescountry=[]
        if 'admin_records' in data.keys():
                #print('in admin records')
                changes=[]
                len_of_adminrecords=str(len(data['admin_records']))

                #print ('len of account status changes are'+ len_of_adminrecords)
                for ele in data['admin_records']:
                    ip=ele['session']['ip_address']

                    try:
                        data = rawdata.record_by_name(ip)
                        city=data['city']
                        country=data['country_name']
                        adminchangescity.append(data['city'])
                        adminchangescountry.append(data['country_name'])
                        # #print countrycodesforactivity
                    except:
                        city='not known'
                        country='not known'
                        #print ('invalid ip  :' + ip)
                        pass;
                    adminchange={'city':city,'country':country,'ip':ip,'type':ele['event'],'time':ele['session']['created_timestamp']}
                    changes.append(adminchange)
                #print (dict(Counter(adminchangescountry)))
                #print (dict(Counter(adminchangescity)))
                types=[]
                for ele in changes:
                    types.append(ele['type'])
                adminchanges={}
                for ele in types:
                    list1=[]
                    for element in changes:
                        ##print element
                        if element['type']==ele:
                           list1.append({'city':element['city'],'country': element['country'], 'ip': element['ip'],'timestamp':element['time']})
                    adminchanges[ele]=list1
                #print(json.dumps(adminchanges,indent=4))
            #authorized logins
        if 'account_status_changes' in data.keys():
            #print('number of account status changes'+str(len(data['account_status_changes'])))
            types=[]
            try:
                for ele in data['account_status_changes']:
                    types.append(ele['status'])
                types= list(set(types))
                status_changes=[]
            except:
                pass;
            try:
                for type in types:
                    list1=[]
            except:
                pass;

            try:
                for ele in data['account_status_changes']:
                    if ele['status']==type:
                        list1.append(ele['timestamp'])
                    a={'status change':type,'timestamps':list1}
                status_changes.append(a)
            except:
                pass;
            #print (json.dumps(status_changes,indent=4))
        if 'recognized_devices' in data.keys():

            pass
        if 'login_protection_data' in data.keys():
            #what to do?

            pass
        if 'account_accesses' in data.keys():
            #print ('login and logouts ')
            logs=[]
            accountaccess={}
            for ele in data['account_accesses']:

                act=ele['action']
                logs.append(act)
            logs=list(set(logs))

            for i in logs:
                for ele in data['account_accesses']:
                        time = ele['timestamp']
                        ip = ele['ip_address']
                try:
                        city = rawdata.record_by_name(ip)['city']
                        country=rawdata.record_by_name(ip)['country_name']
                except:
                        city='unknown'
                        country='unknown'
                if ele['action']==i:
                        list1.append({'timestamp':time,'ip':ip,'city':city,'country':country })
                accountaccess[i]=list1
            #print(json.dumps(accountaccess,indent=4))
            #what to do?
            pass
        if 'used_ip_address' in data.keys():
            ipinfo=[]
            for ele in data['used_ip_address']:
                try:
                    a={}
                    city = rawdata.record_by_name(ele)['city']
                    country = rawdata.record_by_name(ele)['country_name']
                    long=rawdata.record_by_name(ele)['longitude']
                    lat=rawdata.record_by_name(ele)['latitude']
                    postalcode=rawdata.record_by_name(ele)['postal_code']
                    a['ip'] = ele
                    a['city']=city
                    a['country']=country
                    a['long,lat']=long,lat
                    a['postalcode']=postalcode
                    ipinfo.append(a)
                except:
                    a={}
                    city = 'unknown'
                    country = 'unknown'
                    long='unknown'
                    lat='unknown'
                    postalcode='unknown'
                    a['ip']=ele
                    a['city'] = city
                    a['country'] = country
                    a['long,lat'] = long, lat
                    a['postalcode'] = postalcode
                    ipinfo.append(a)
            #print('number of ip addresses used '+ str(len(ipinfo)))

            #print ('data from ips' +json.dumps(ipinfo,indent=4))


        if 'active_sessions' in data.keys():
            # what to do?
            pass
    return {'city_activity_in':str(citysforactivity),"country_activity_in":str(countrycodesforactivity),'length_of_admin_records_changed':len_of_adminrecords,"admin_changes_countries":str(dict(Counter(adminchangescountry))),"admin_changes_city":str(dict(Counter(adminchangescity))),"admin_changes":adminchanges,"status_changes":status_changes,"ip_addresses_used":ipinfo}



def apps_and_websites(directory):

    jsonfiles = common(directory)
    noofadminapps = 0
    noofinstalledapps = 0
    noofappposts = 0
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        try:

            if 'installed_apps' in data.keys():

                noofinstalledapps=len(data['installed_apps'])
                #print('number of installed apps:'+str(noofinstalledapps))
        except:
            pass;
        try:
            if 'app_posts' in data.keys():

                noofappposts = len(data['app_posts'])
                #print('number of app posts:'+str(noofappposts))
        except:
            pass;
        try:
            if 'admined_apps' in data.keys():

                noofadminapps = len(data['admined_apps'])
                #print('no. of admin apps:'+ str(noofadminapps))
                #return {"number_of_installed_apps" : noofinstalledapps,"app_posts":noofappposts,"admined_apps":noofadminapps}
        except:
            pass;


    return {"number_of_installed_apps": noofinstalledapps, "app_posts":noofappposts, "admined_apps": noofadminapps}

#3
def friends(directory):
    lengthoffriends=0
    lengthofdeleted=0
    lengthofreceived=0
    lengthofrejected=0
    lengthofsent=0
    jsonfiles = common(directory)
    v = []
    w = []
    x = []
    y = []
    z = []
    a1 = []
    b1=[]
    c1=[]
    # #print("************************")
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        try:
            if 'received_requests' in data.keys():
                lengthofreceived = len(data['received_requests'])
                #print("length of received rquests are: " + str(lengthofreceived))
                for i in range(0, lengthofreceived):
                    a1 = data['received_requests'][i]['name']
                    b1 = data['received_requests'][i]['timestamp']
                    c1 = (a1, b1)
                    v.append(c1)
                v = sorted(v, key=lambda v: v[1], reverse=True)
                #for i in range(0, lengthofreceived):
                    #print(v[i])
        except:
            pass;
        try:
            if 'friends' in data.keys():
                lengthoffriends = len(data['friends'])
                #print("length of total friends are: " + str(lengthoffriends))
                for i in range(0, lengthoffriends):
                    a2 = data['friends'][i]['name']
                    b2 = data['friends'][i]['timestamp']
                    c2 = (a2, b2)
                    w.append(c2)
                w = sorted(w, key=lambda w: w[1], reverse=True)
                # for i in range(0, lengthoffriends):
                #     #print(w[i])
        except:
            pass;
        try:
            if 'rejected_requests' in data.keys():
                lengthofrejected = len(data['rejected_requests'])
                #print("rejected requests are: " + str(lengthofrejected))
                for i in range(0, lengthofrejected):
                    a3 = data['rejected_requests'][i]['name']
                    b3 = data['rejected_requests'][i]['timestamp']
                    c3 = (a3, b3)
                    x.append(c3)
                x = sorted(x, key=lambda x: x[1], reverse=True)
                # for i in range(0, lengthofrejected):
                #print(x[i])
        except:
            pass;
        try:
            if 'deleted_friends' in data.keys():
                lengthofdeleted = len(data['deleted_friends'])
                #print("removed friends are: " + str(lengthofdeleted))
                for i in range(0, lengthofdeleted):
                    a4 = data['deleted_friends'][i]['name']
                    b4 = data['deleted_friends'][i]['timestamp']
                    c4 = (a4, b4)
                    y.append(c4)
                y = sorted(y, key=lambda y: y[1], reverse=True)
                # for i in range(0, lengthofdeleted):
                #     #print(y[i])
        except:
            pass;
        try:
            if 'sent_requests' in data.keys():
                lengthofsent = len(data['sent_requests'])
                #print("sent requests are: " + str(lengthofsent))
                for i in range(0, lengthofsent):
                    a5 = data['sent_requests'][i]['name']
                    b5 = data['sent_requests'][i]['timestamp']
                    c5 = (a5, b5)
                    z.append(c5)
                z = sorted(z, key=lambda z: z[1], reverse=True)
                # for i in range(0, lengthofsent):
                #     #print(z[i])
        except:
            pass;
        #print("************************")

    #return {'lengthofreceived': lengthofreceived ,'lengthoffriends':lengthoffriends,'lengthofrejected':lengthofrejected,'lengthofdeleted':lengthofdeleted,'lengthofsent':lengthofsent}
    return{'total_friends':w,'received_friends':v ,'rejected_friends':x,'deleted_friends':y,'sent_requests':z,'lengthoffriends':lengthoffriends,'lengthofreceived': lengthofreceived,'lengthofrejected':lengthofrejected,'lengthofdeleted':lengthofdeleted,'lengthofsent':lengthofsent}


#4
def saved_items(directory):
    timestamp = []
    jsonfiles = common(directory)
    for file in jsonfiles:
        data=json.load(open(file))
        ##print ('number of photos and videos saved'+ str(len(data['saves'])))

        try:
            if 'saves' in data.keys():
                for ele in data['saves']:
                   timestamp.append(ele['timestamp'])
            ##print('timestamps of saves  '+str(timestamp))
        except:
            pass;
    return{'saved_items_timestamps':timestamp}
#5
def search_history(directory):
    maindirectory = os.path.dirname(directory)
    jsonfiles = common(directory)

    def find_words(text, search):
        """Find exact words"""
        dText = text.split()
        dSearch = search.split()

        found_word = 0

        for text_word in dText:
            for search_word in dSearch:
                if search_word == text_word:
                    found_word += 1

        if found_word == len(dSearch):
            return True
        else:
            return False

    path_to_json = maindirectory+'/search_history'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_search_history = json.load(json_file)
    path_to_json = maindirectory+'/friends/friends.json'
    with open(path_to_json) as json_file:
        json_friends = json.load(json_file)
    path_to_json = maindirectory+'/friends/received_friend_requests.json'
    with open(path_to_json) as json_file:
        json_received_friends_requests = json.load(json_file)
    path_to_json = maindirectory+'/friends/rejected_friend_requests.json'
    with open(path_to_json) as json_file:
        json_rejected_friends_requests = json.load(json_file)
    path_to_json = maindirectory+'/friends/removed_friends.json'
    with open(path_to_json) as json_file:
        json_removed_friends = json.load(json_file)
    path_to_json = maindirectory+'/friends/sent_friend_requests.json'
    with open(path_to_json) as json_file:
        json_sent_friend_requests = json.load(json_file)

    my_friends_searched = []
    my_friends_searched1={}
    names = []
    try:
        for ele in json_friends["friends"]:
            names.append(ele['name'])
        names = list(set(names))
        for m in range(0, len(names)):
            for i in range(0, len(json_search_history["searches"])):

                if json_search_history["searches"][i]["title"].lower().count(names[m].lower()) > 0:
                    my_friends_searched.append(names[m])
    except:
        pass;

    length_of_seach_history = len(json_search_history["searches"])
    counter_my_friends_searched = Counter(my_friends_searched)
    set_of_my_friends_searched = list(set(my_friends_searched))
    len(my_friends_searched)
    len(set_of_my_friends_searched)
    ##return  all this
    #print("counter of my friends searched", counter_my_friends_searched)
    #print("set of my friends searches", set_of_my_friends_searched)
    #print("The number of times I searched my friends", len(my_friends_searched))
    #print("The set of number times I searched my friends", len(set_of_my_friends_searched))
    #print("#######################################################################################################################################")
    my_friends_searched1={'counter_of_my_friends_searched':counter_my_friends_searched,'set_of_my_friends_searches':set_of_my_friends_searched,'The_number_of_times_I_searched_my_friends':len(my_friends_searched),'The_set_of_number_times_I_searched_my_friends':len(set_of_my_friends_searched)}
    name2 = []
    my_received_friend_requests = []
    try:
        for ele in json_received_friends_requests["received_requests"]:
            name2.append(ele["name"])
        name2 = list(set(name2))
        for m in range(0, len(name2)):
            for i in range(0, len(json_search_history["searches"])):

                ##         if(find_words(json_search_history["searches"][i]["title"].lower(),json_friends["friends"][m]["name"].lower())==True):
                ##            a.append(json_friends["friends"][m]["name"])
                if json_search_history["searches"][i]["title"].lower().count(name2[m].lower()) > 0:
                    my_received_friend_requests.append(name2[m])
    except:
        pass;

    counter_my_received_friend_requests = Counter(my_received_friend_requests)
    set_my_received_friend_requests = list(set(my_received_friend_requests))
    len(my_received_friend_requests)
    len(set_my_received_friend_requests)
    ##return  all this
    #print("counter of my received friends searched ", counter_my_received_friend_requests)
    #print("set of my  received friends searched", set_my_received_friend_requests)
    #print("The number of times I searched my received friends", len(my_received_friend_requests))
    #print("The set of number times I searched my  received friends", len(set_my_received_friend_requests))
    #print("#######################################################################################################################################")
    my_received_friend_searched1={'counter_of_my_received_friends_searched':counter_my_received_friend_requests,'set_of_my_received_friends searches':set_my_received_friend_requests,'The_number_of_times_I_searched_my_received_friends':len(my_received_friend_requests),'The_set_of_number_times_I_searched_my_received_friends': len(set_my_received_friend_requests)}

    name3 = []
    my_rejected_friend_requests = []
    try:
        for ele in json_rejected_friends_requests["rejected_requests"]:
            name3.append(ele["name"])
        name3 = list(set(name3))
        for m in range(0, len(name3)):
            for i in range(0, len(json_search_history["searches"])):

                ##         if(find_words(json_search_history["searches"][i]["title"].lower(),json_friends["friends"][m]["name"].lower())==True):
                ##            a.append(json_friends["friends"][m]["name"])
                if json_search_history["searches"][i]["title"].lower().count(name3[m].lower()) > 0:
                    my_rejected_friend_requests.append(name3[m])
    except:
        pass;

    counter_my_rejected_friend_requests = Counter(my_rejected_friend_requests)
    set_my_rejected_friend_requests = list(set(my_rejected_friend_requests))
    len(my_rejected_friend_requests)
    len(set_my_rejected_friend_requests)
    ##return  all this
    #print("counter of my rejected friends searched ", counter_my_rejected_friend_requests)
    #print("set of my  rejected friends searched", set_my_rejected_friend_requests)
    #print("The number of times I searched my rejected friends", len(my_rejected_friend_requests))
    #print("The set of number times I searched my  rejected friends", len(set_my_rejected_friend_requests))
    #print("#######################################################################################################################################")
    my_rejected_friend_searched1={'counter_of_my_rejected_friends_searched':counter_my_rejected_friend_requests,'set_of_my_rejected_friends_searches':set_my_rejected_friend_requests,'The_number_of_times_I_searched_my_rejected_friends':len(my_rejected_friend_requests),'The_set_of_number_times_I_searched_my_rejected_friends': len(set_my_rejected_friend_requests)}

    name4 = []
    my_removed_friend_requests = []
    try:
        for ele in json_removed_friends["deleted_friends"]:
            name4.append(ele["name"])
        name4 = list(set(name4))
        for m in range(0, len(name4)):
            for i in range(0, len(json_search_history["searches"])):

                ##         if(find_words(json_search_history["searches"][i]["title"].lower(),json_friends["friends"][m]["name"].lower())==True):
                ##            a.append(json_friends["friends"][m]["name"])
                if json_search_history["searches"][i]["title"].lower().count(name4[m].lower()) > 0:
                    my_removed_friend_requests.append(name4[m])
    except:
        pass;

    counter_my_removed_friend_requests = Counter(my_removed_friend_requests)
    set_my_removed_friend_requests = list(set(my_removed_friend_requests))
    len(my_removed_friend_requests)
    len(set_my_removed_friend_requests)
    ##return  all this
    #print("counter of my removed friends searched ", counter_my_removed_friend_requests)
    #print("set of my  removed friends searched", set_my_removed_friend_requests)
    #print("The number of times I searched my removed friends", len(my_removed_friend_requests))
    #print("The set of number times I searched my  removed friends", len(set_my_removed_friend_requests))
    #print("#######################################################################################################################################")
    my_removed_friend_searched1={'counter_of_my_removed_friends_searched':counter_my_removed_friend_requests,'set_of_my_removed_friends_searches':set_my_removed_friend_requests,'The_number_of_times_I_searched_my_removed_friends':len(my_removed_friend_requests),'The_set_of_number_times_I_searched_my_removed_friends': len(set_my_removed_friend_requests)}

    name5 = []
    my_sent_friend_requests = []
    try:
        for ele in json_sent_friend_requests["sent_requests"]:
            name5.append(ele["name"])
        name5 = list(set(name5))
        for m in range(0, len(name5)):
            for i in range(0, len(json_search_history["searches"])):

                ##         if(find_words(json_search_history["searches"][i]["title"].lower(),json_friends["friends"][m]["name"].lower())==True):
                ##            a.append(json_friends["friends"][m]["name"])
                if json_search_history["searches"][i]["title"].lower().count(name5[m].lower()) > 0:
                    my_sent_friend_requests.append(name5[m])
    except:
        pass;

    counter_my_sent_friend_requests = Counter(my_sent_friend_requests)
    set_my_sent_friend_requests = list(set(my_sent_friend_requests))
    len(my_sent_friend_requests)
    len(set_my_sent_friend_requests)
    ##return  all this
    #print("counter of my sent friends searched ", counter_my_sent_friend_requests)
    #print("set of my  sent friends searched", set_my_sent_friend_requests)
    #print("The number of times I searched my sent friends", len(my_sent_friend_requests))
    #print("The set of number times I searched my  sent friends", len(set_my_sent_friend_requests))
    #print("#######################################################################################################################################")
    my_sent_friend_searched1={'counter_of_my_sent_friends_searched':counter_my_sent_friend_requests,'set_of_my_sent_friends_searches':set_my_sent_friend_requests,'The_number_of_times_I_searched_my_sent_friends':len(my_sent_friend_requests),'The_set_of_number_times_I_searched_my_sent_friends': len(set_my_sent_friend_requests)}

    return {'my_friends_searched':my_friends_searched1,'my_received_friend_searched1':my_received_friend_searched1,'my_rejected_friend_searched1':my_rejected_friend_searched1,'my_removed_friend_searched1':my_removed_friend_searched1,'my_sent_friend_searched1':my_sent_friend_searched1}
#6
def posts(directory):

    jsonfiles = common(directory)

    timestamps=[]
    post=[]
    otherpeoplepost={}
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        friendlist=getfriendlist();
        if 'status_updates' in data.keys():
            pass;
        if 'wall_posts_sent_to_you' in data.keys():
            # for i in friendlist:
            #     for ele in data['wall_posts_sent_to_you']:
            #         if ele['title'].count(i)>0:
            #             try:
            #                 # #print('done')
            #                 otherperson.append((ele['timestamp'],ele['data'][0]['post']))
            #             except:
            #                 pass
            #         otherpeoplepost[i]=otherperson
            for i in range(0, len(friendlist)):
                substring = friendlist[i];
                otherperson=[]
                # #print(substring)
                for j in data['wall_posts_sent_to_you']:
                    c = j['title'].count(substring)

                    if c != 0:
                        try:
                            otherperson.append((j['timestamp'],j['data'][0]['post']))
                        except:
                            pass
                if(len(otherperson)>0):
                    otherpeoplepost[friendlist[i]]=otherperson
            #print(otherpeoplepost)
            #print(otherpeoplepost.keys())
    return {'other_people_post':otherpeoplepost}


#7
def about_you(directory):
    contactlist = []
    facecount1 = 0
    countrycodes = []
    jsonfiles = common(directory)

    for i in range(0, len(jsonfiles)):

        data = json.load(open(jsonfiles[i]))
        try:
            if 'facial_data' in data.keys():
                facecount = data['facial_data']["example_count"]
                facecount1 = str(facecount)
        except:
            pass;

        if 'address_book' in data.keys():
            # length
            #print("contacts" + str(len(data["address_book"]["address_book"])))
            # country codes
            for i in range(0, len(data["address_book"]["address_book"])):
                for i in range(0, len(data["address_book"]["address_book"][i]["details"])):
                    try:
                        pn = phonenumbers.parse(data["address_book"]["address_book"][i]["details"][0]["contact_point"])
                        countrycodes.append(region_code_for_country_code(pn.country_code))
                        # #print(region_code_for_country_code(pn.country_code))
                    except:
                        pass;
            countries = dict(Counter(countrycodes))
            # most recently created contacts and if messenger installed number of times and last time contacted
            createdtime = 0
            name = ''
            lasttimecontacted = 0
            messenger = 'messengerinstalled'
            nomessenger = 'no messenger'
            for i in range(0, len(data["address_book"]["address_book"])):
                for j in range(0, len(data["address_book"]["address_book"][i]['details'])):
                    try:

                        # if 'extra_data' in data["address_book"]["address_book"][i]['details'][j].keys():
                        #
                        #     if 'number_times_contacted' in data["address_book"]["address_book"][i]['details'][j]['extra_data']:
                                lasttimecontacted = data["address_book"]["address_book"][i]['details'][j]['extra_data'][
                                    'last_time_contacted']
                                number_times_contacted = data["address_book"]["address_book"][i]['details'][j]['extra_data']['number_times_contacted']
                                contactlist.append((data["address_book"]["address_book"][i]['created_timestamp'],
                                                        data["address_book"]["address_book"][i]['name'], lasttimecontacted,
                                                    number_times_contacted, messenger))
                    except:

                        contactlist.append((data["address_book"]["address_book"][i]['created_timestamp'],
                                            data["address_book"]["address_book"][i]['name'], nomessenger))

            ##                                      contactlist.append((data["address_book"]["address_book"][i]['created_timestamp'],data["address_book"]["address_book"][i]['name']))

            # contactlist=sorted(contactlist, key=lambda x: x[0],reverse=True)
            # for i in range(0, 6):
    #print(len(jsonfiles))
    return {'Contact_information' : contactlist,'Your_face_count_is' :facecount1,'Country_code_is' :countrycodes}



def ads(directory):

    jsonfiles = common(directory)
    u = []
    for i in range(0, len(jsonfiles)):
        #print("************************")
        data = json.load(open(jsonfiles[i]))
        try:
            if 'topics' in data.keys():
                lengthofinterestedads = len(data['topics'])
                #print("number of ads based on your facebook activity are: " + str(lengthofinterestedads))
        except:
            pass;
        try:
            if 'custom_audiences' in data.keys():
                lengthofinterestedads = len(data['custom_audiences'])
                #print("number of ads due to contact sharing are: " + str(lengthofinterestedads))
        except:
            pass;
        try:
            if 'history' in data.keys():
                lengthofinterestedads = len(data['history'])
                #print("number of ads you have interacted with are: " + str(lengthofinterestedads))
                for i in range(0, lengthofinterestedads):
                    a6 = data['history'][i]['action']
                    b6 = data['history'][i]['timestamp']
                    c6 = (a6, b6)
                    u.append(c6)
                u = sorted(u, key=lambda u: u[1], reverse=True)
                # for i in range(0, lengthofinterestedads):
                #     #print(u[i])
        except:
            pass;
        #print("************************")
    return {'ads_based_on_facebook_activity':lengthofinterestedads,'ads_due_to_contact_sharing':lengthofinterestedads,'ads_interacted_with':u}


def calls_and_messages(directory):
    n = []
    names = []
    unknowns = []
    try:
        maindirectory=os.path.dirname(directory)
        path_to_json = maindirectory + '/calls_and_messages'
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('call_logs.json')]
        for index, js in enumerate(json_files):
            with open(os.path.join(path_to_json, js)) as json_file:json_sext = json.load(json_file)

            d = list(json_sext["call_logs"].keys())
            a = ''
            name = ''


            for i in range(0, len(json_sext["call_logs"])):
                duration = []
                count = 0
                coun = 0
                cou = 0
                c = 0
                for m in range(0, len(json_sext["call_logs"][d[i]])):
                    a = d[i]
                    duration.append(json_sext["call_logs"][d[i]][m]["duration"])

                    count += 1
                    try:
                        if (json_sext["call_logs"][d[i]][m]["call_type"] == "INCOMING"):
                            coun += 1
                        elif (json_sext["call_logs"][d[i]][m]["call_type"] == "OUTGOING"):
                            cou += 1
                        elif (json_sext["call_logs"][d[i]][m]["call_type"] == "MISSED"):
                            c += 1

                        try:
                            name = json_sext["call_logs"][d[i]][m]["contact_name"]

                        except:
                            name = "NUMBER NOT SAVED"
                            pass;
                    except:
                        # #print(json_sext["call_logs"][d[i]][m])
                        pass;
                n.append(('name',name,'count',count,'number',a,'duration_of_each_call',duration,'incoming',coun,'outgoing',cou,'missed',c))

        json_filess = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('message_logs.json')]
        for index, js in enumerate(json_filess):
            with open(os.path.join(path_to_json, js)) as json_file: data = json.load(json_file)

            data=data['message_logs']['sms_logs']
            numbers = list(data.keys())
            for ele in numbers:

                e=getnamefromnumber(ele,directory)

                if e != None:
                    names.append((e,data[ele]))
                else:
                    unknowns.append((ele,data[ele]))


            #print(unknowns)

    except:
        pass
    return {'calls':n,'messages_information_known':names,'messages_information_unknown':unknowns}


def profile_information(directory):
    timewhenjoined = 0
    groupsjoined = 0
    categnames = []
    lengthofeducation = 0
    nooffamilymebers = 0
    family = []
    gender = 0
    dob = 0
    name=""
    type={}
    jsonfiles = common(directory)
    for ele in jsonfiles:
        data=json.load(open(ele))
        if 'profile' in data.keys():
            data=data['profile']
            name=data["name"]
            timewhenjoined=data.get('registration_timestamp')
            #print('time when joined'+str(timewhenjoined))
            try:
                groupsjoined=str(len(data.get('groups')))
            except:
                pass;
            #print('pages')
            try:
                for ele in data.get('pages'):
                    categnames.append((ele['name'],str(len(ele['pages']))))
                    noofpages = str(len(ele['pages']))
                ##print('name: '+ str(ele['name'])+'number of pages: '+str(len(ele['pages'])))
            except:
                pass;
            try:
                lengthofeducation = str(len(data.get('education_experiences')))
                #for ele in data.get('education_experiences'):
                    #if ele['graduated']=='false':
                        #print(ele)
            except:
                pass;
            try:
                nooffamilymebers = str(len(data['family_members']))
            except:
                nooffamilymebers=""
                pass;
            try:
                for ele in data['family_members']:
                    family.append((ele['name'],ele['relation']))
                    #print ('family members are'+ str(family))
            except:
                pass;
            gender = str(data['gender']['gender_option'])
            dob = str(data['birthday'])
    return {'name':name,'date_of_joining':timewhenjoined,'no_of_groups_joined':groupsjoined,'category_names':categnames,'education_experience':lengthofeducation,'no_of_family_members':nooffamilymebers,'family_members':family,'gender_is':gender,'date_of_birth':dob}



def payment_history(directory):
    payinfo = 0
    jsonfiles = common(directory)
    for el in jsonfiles:
        data=json.load(open(el))
        try:
            if 'payments' in data.keys():
                payinfo = data['payments']
        except:
            pass;
    return {'payment_information':payinfo}

def location_history(directory):
    jsonfiles = common(directory)
#TODO

def likes_and_reactions(directory):
    path_to_json = directory
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('pages.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_sext = json.load(json_file)

    # #print("Number of pages liked:"+ str(len(json_sext["page_likes"])))
    a = {"Number of pages liked": [len(json_sext["page_likes"])]}

    json_files1 = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('posts_and_comments.json')]
    for index, js in enumerate(json_files1):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)

    #print(len(json_text["reactions"]))
    count_likes = 0
    count_haha = 0
    count_love = 0
    count_anger = 0
    count_wow = 0
    count_sorry = 0
    count_dorothy = 0

    count_postsliked = 0
    count_videoliked = 0
    count_commentliked = 0
    count_photoliked = 0
    count_linkliked = 0
    count_albumliked = 0
    count_friendshipliked = 0
    count_eventliked = 0
    count_instaliked = 0
    count_restliked = 0

    count_postshaha = 0
    count_videohaha = 0
    count_commenthaha = 0
    count_photohaha = 0
    count_linkhaha = 0
    count_albumhaha = 0
    count_friendshiphaha = 0
    count_eventhaha = 0
    count_instahaha = 0
    count_resthaha = 0

    count_postslove = 0
    count_videolove = 0
    count_commentlove = 0
    count_photolove = 0
    count_linklove = 0
    count_albumlove = 0
    count_friendshiplove = 0
    count_eventlove = 0
    count_instalove = 0
    count_restlove = 0

    count_postsanger = 0
    count_videoanger = 0
    count_commentanger = 0
    count_photoanger = 0
    count_linkanger = 0
    count_albumanger = 0
    count_friendshipanger = 0
    count_eventanger = 0
    count_instaanger = 0
    count_restanger = 0

    count_postswow = 0
    count_videowow = 0
    count_commentwow = 0
    count_photowow = 0
    count_linkwow = 0
    count_albumwow = 0
    count_friendshipwow = 0
    count_eventwow = 0
    count_instawow = 0
    count_restwow = 0

    count_postssorry = 0
    count_videosorry = 0
    count_commentsorry = 0
    count_photosorry = 0
    count_linksorry = 0
    count_albumsorry = 0
    count_friendshipsorry = 0
    count_eventsorry = 0
    count_instasorry = 0
    count_restsorry = 0

    count_postsdorothy = 0
    count_videodorothy = 0
    count_commentdorothy = 0
    count_photodorothy = 0
    count_linkdorothy = 0
    count_albumdorothy = 0
    count_friendshipdorothy = 0
    count_eventdorothy = 0
    count_instadorothy = 0
    count_restdorothy = 0
    try:
        for i in range(0, len(json_text["reactions"])):

            if (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "LIKE"):
                count_likes += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True or find_words(
                        json_text["reactions"][i]["title"], "photo") == True):
                    count_photoliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshipliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instaliked += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postsliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postsliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentliked += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videoliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videoliked += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linkliked += 1
                else:
                    count_restliked

            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "HAHA"):
                count_haha += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photohaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photohaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumhaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumhaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshiphaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventhaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instahaha += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postshaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postshaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commenthaha += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videohaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videohaha += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linkhaha += 1
                else:
                    count_resthaha

            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "LOVE"):
                count_love += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photolove += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photolove += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumlove += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumlove += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshiplove += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventlove += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instalove += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postslove += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postslove += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentlove += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videolove += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videolove += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linklove += 1
                else:
                    count_restlove







            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "ANGER"):
                count_anger += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photoanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photoanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshipanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instaanger += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postsanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postsanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentanger += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videoanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videoanger += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linkanger += 1
                else:
                    count_restanger












            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "WOW"):
                count_wow += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photowow += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photowow += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumwow += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumwow += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshipwow += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventwow += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instawow += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postswow += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postswow += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentwow += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videowow += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videowow += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linkwow += 1
                else:
                    count_restwow







            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "SORRY"):
                count_sorry += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photosorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photosorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumsorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumsorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshipsorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventsorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instasorry += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postssorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postssorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentsorry += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videosorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videosorry += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linksorry += 1
                else:
                    count_restsorry

            elif (json_text["reactions"][i]["data"][0]["reaction"]["reaction"] == "DOROTHY"):
                count_dorothy += 1
                if (find_words(json_text["reactions"][i]["title"], "photo.") == True):
                    count_photodorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "photo") == True):
                    count_photodorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "album:") == True):
                    count_albumdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "album.") == True):
                    count_albumdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "friendship.") == True):
                    count_friendshipdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "event.") == True):
                    count_eventdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "Instagram.") == True):
                    count_instadorothy += 1

                elif (find_words(json_text["reactions"][i]["title"], "post.") == True):
                    count_postsdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "post") == True):
                    count_postsdorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "comment.") == True | find_words(
                        json_text["reactions"][i]["title"], "comment") == True):
                    count_commentdorothy += 1

                elif (find_words(json_text["reactions"][i]["title"], "video.") == True):
                    count_videodorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "video:") == True):
                    count_videodorothy += 1
                elif (find_words(json_text["reactions"][i]["title"], "link.") == True):
                    count_linkdorothy += 1
                else:
                    count_restdorothy
        dictlikes={'count_likes':count_likes,'count_postliked':count_postsliked,'count_videoliked':count_videoliked ,'count_commentliked':count_commentliked,'count_photoliked':count_photoliked,'count_linkliked':count_linkliked,'count_albumliked':count_albumliked,'countfriendshipliked':count_friendshipliked,'counteventliked':count_eventliked,'countinstaliked':count_instaliked,'countrestliked':count_restliked }
        dicthaha = {'count_haha': count_haha, 'count_posthaha': count_postshaha, 'count_videohaha': count_videohaha,
                    'count_commenthaha': count_commenthaha, 'count_photohaha': count_photohaha,
                    'count_linkhaha': count_linkhaha, 'count_albumhaha': count_albumhaha,
                    'countfriendshiphaha': count_friendshiphaha, 'counteventhaha': count_eventhaha,
                    'countinstahaha': count_instahaha, 'countresthaha': count_resthaha}

        dictlove = {'count_love': count_love, 'count_postlove': count_postslove, 'count_videolove': count_videolove,
                    'count_commentlove': count_commentlove, 'count_photolove': count_photolove,
                    'count_linklove': count_linklove, 'count_albumlove': count_albumlove,
                    'countfriendshiplove': count_friendshiplove, 'counteventlove': count_eventlove,
                    'countinstalove': count_instalove, 'countrestlove': count_restlove}

        dictanger = {'count_anger': count_anger, 'count_postanger': count_postsanger, 'count_videoanger': count_videoanger,
                     'count_commentanger': count_commentanger, 'count_photoanger': count_photoanger,
                     'count_linkanger': count_linkanger, 'count_albumanger': count_albumanger,
                     'countfriendshipanger': count_friendshipanger, 'counteventanger': count_eventanger,
                     'countinstaanger': count_instaanger, 'countrestanger': count_restanger}

        dictwow = {'count_wow': count_wow, 'count_postwow': count_postswow, 'count_videowow': count_videowow,
                   'count_commentwow': count_commentwow, 'count_photowow': count_photowow, 'count_linkwow': count_linkwow,
                   'count_albumwow': count_albumwow, 'countfriendshipwow': count_friendshipwow,
                   'counteventwow': count_eventwow, 'countinstawow': count_instawow, 'countrestwow': count_restwow}

        dictsorry = {'count_sorry': count_sorry, 'count_postsorry': count_postssorry, 'count_videosorry': count_videosorry,
                     'count_commentsorry': count_commentsorry, 'count_photosorry': count_photosorry,
                     'count_linksorry': count_linksorry, 'count_albumsorry': count_albumsorry,
                     'countfriendshipsorry': count_friendshipsorry, 'counteventsorry': count_eventsorry,
                     'countinstasorry': count_instasorry, 'countrestsorry': count_restsorry}

        dictdorothy = {'count_dorothy': count_dorothy, 'count_postdorothy': count_postsdorothy,
                       'count_videodorothy': count_videodorothy, 'count_commentdorothy': count_commentdorothy,
                       'count_photodorothy': count_photodorothy, 'count_linkdorothy': count_linkdorothy,
                       'count_albumdorothy': count_albumdorothy, 'countfriendshipdorothy': count_friendshipdorothy,
                       'counteventdorothy': count_eventdorothy, 'countinstadorothy': count_instadorothy,
                       'countrestdorothy': count_restdorothy}
    except:
        pass;

    return {'count_likes':dictlikes,'count_haha':dicthaha,'count_love':dictlove,'count_anger':dictanger,'count_wow':dictwow,'count_sorry':dictsorry,'count_dorothy':dictdorothy}

def events(directory):
    t = []
    lengthofeventinvited = 0
    lengthofeventrespondedorjoined = 0

    jsonfiles = common(directory)

    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        if 'events_invited' in data.keys():
            try:
                lengthofeventinvited = len(data['events_invited'])
                #print("number of events you have been invited too are : " + str(lengthofeventinvited))
                for i in range(0, lengthofeventinvited):
                    n7 =data['events_invited'][i]['name']
                    a7 = data['events_invited'][i]['start_timestamp']
                    b7 = data['events_invited'][i]['end_timestamp']
                    c7 = ("Name",n7,"Start_timestamp",a7,"End_timestamp", b7)
                    t.append(c7)
                t = sorted(t, key=lambda t: t[1], reverse=True)
                #for i in range(0, lengthofeventinvited):
                    #print(t[i])
            except:
                pass;
        if 'event_responses' in data.keys():
            try:
                lengthofeventrespondedorjoined = len(data['event_responses']['events_joined'])
            except:
                lengthofeventrespondedorjoined=""
            #print("number of events you joined are: " + str(lengthofeventrespondedorjoined))
    return {'length_of_event_invited':lengthofeventinvited,'event_details':t,'event_response':lengthofeventrespondedorjoined}


def other_activity(directory):


    timestamps=[] ;pokers=[]
    ts = 0
    jsonfiles = common(directory)
    for file in jsonfiles:
        data = json.load(open(file))
        if 'pokes'in data.keys():
            try:
                for ele in data['pokes']:
                    pokers.append(ele['poker'])
                    timestamps.append(ele['timestamp'])
                    ts=len(timestamps)
                #print ('number of pokes'+ str(ts))
                #print('pokes from '+ str(pokers))
                c = Counter()
                #print('poke timestamps'+ str(timestamps))
            except:
                pass;
    return{'Number_of_pokes': ts ,'pokes_from': pokers ,'poke_timestamp':timestamps}



def pages(directory):
    jsonfiles = common(directory)
    number_of_pages_created_by_user=""
    for ele in jsonfiles:
        data=json.load(open(ele))
        try:
            if 'pages' in data.keys():
                number_of_pages_created_by_user = str(len(data['pages']))
        except:
            pass;
    return {'number_of_pages_created_by_user':number_of_pages_created_by_user }

def comments(directory):

    # jsonfiles = common(directory)
    jsonfiles = common(directory)
    commentsdone=[]
    tagcount={}
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))

        if 'comments' in data.keys():
            for i in range(0,len(data['comments'])):
                try:
                    commentsdone.append(( data['comments'][i]['data'][0]['comment']['timestamp'],data['comments'][i]['data'][0]['comment']['comment']) )

                except:
                   pass;
                  #  if data['comments'][i]['attachments'][0]['author']!="Nitin Bhansali":
                   #     #print(data['comm)
        #for i in range(0,6):
            #print(commentsdone[i])
        friendlist=getfriendlist(directory);
        tagged=[]
        for i in range(0,len(friendlist)):
            substring=friendlist[i];
            ##print(substring)
            for i in range(0,len(commentsdone)):
                c=commentsdone[i][1].count(substring)
                if c!=0: tagged.append((substring,commentsdone[i][0]))
        tagcount=dict(Counter(t[0] for t in tagged))
        ##print(tagged)
        #tagcount contains timestamps and number of times tagged for each friend,can be used to find recent
        for i in range(0,len(tagcount.keys())):
            times=[]
            for elem in tagged:

                if elem[0]== list(tagcount.keys())[i]:
                    times.append(elem[1])
            times.sort(reverse=True)
            tagcount[list(tagcount.keys())[i]]={'tagged':len(times),'timestamps':times}
    ##print(tagcount)
        #for i in tagcount.keys():
       #     a={'name':tagcount.keys()[i],'taggedtimes':tagcount[i][1]}
    # except:
    #     pass;
    return {"comments_with_timestamps":commentsdone,"numberoftimestagged":tagcount}


def following_and_followers(directory):
    lengthoffollowing = 0
    jsonfiles = common(directory)
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        try:
            if 'following' in data.keys():
                lengthoffollowing = len(data['following'])
                #print("number of people you follow are (its not the friends you have) : " + str(lengthoffollowing))
        except:
            pass;
    return {'number_of_people_you_follow_is':lengthoffollowing}


def videos(directory):
    creation_timestamp = []
    upload_timestamp = []
    upload_ip = []
    jsonfiles = common(directory)
    lenofgroups=0
    for i in range(0, len(jsonfiles)):
        data = json.load(open(jsonfiles[i]))
        if 'videos' in data.keys():
            lenofgroups = len(data['videos'])
            try:
                for i in range(0, len(data['videos'])):
                    creation_timestamp.append(data['videos'][i]['creation_timestamp'])
                    upload_timestamp.append(data['videos'][i]['media_metadata']['video_metadata']['upload_timestamp'])
                    upload_ip.append(data['videos'][i]['media_metadata']['video_metadata']['upload_ip'])
                #creation_timestamp.sort(reverse=True)
                #print('timestamp of creation:'+str(creation_timestamp))
                #print('upload timestamp'+str(upload_timestamp))
                #print('ip addresses'+str(upload_ip))
                #print('number of videos '+str(lenofgroups))
            except:
                pass;
    return {'nos_videos':lenofgroups,'upload_timestamp':upload_timestamp,'ip_addresses':upload_ip,'creation_timestamp':creation_timestamp}

def album(directory):
    return
    maindirectory = os.path.dirname(directory)
    jsonfiles = common(directory)
    commentsdone=[]
    for ele in jsonfiles:
        data=json.load(open(ele))
        #print('number of photos in '+data['name']+ '   are  '+ str(len(data['photos'])))
        lenoffaces=0
        for photo in data['photos']:
            dir=photo['uri']
            photodir=maindirectory+'/'+dir
            img = cv.imread(photodir)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 3)

            # if len(faces)==21:
            #     for (x, y, w, h) in faces:
            #         cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #     cv.imshow('img', img)
            #     cv.waitKey(0)
            #     cv.destroyAllWindows()

            # #print( 'len of faces in this photo are : '+str(len(faces)))
            lenoffaces=lenoffaces+len(faces)
            try:
                for comment in photo['comments']:
                    commentsdone.append((comment['author'],comment['timestamp'],comment['comment']))
            except:
                pass
        #print('number of faces in this album are'+str(lenoffaces))
    #print(commentsdone)
    names=[]
    for ele in commentsdone:
        names.append(ele[0])
    names=list(set(names))
    commentsall={}
    for i in names:
        commentsbyperson = []
        for j in commentsdone:

            if j[0]==i:
                commentsbyperson.append(j[2])
                # #print 'yes'
        a={'commentsdone':commentsbyperson,'numberofcomments':len(commentsbyperson)}
        commentsall[i]=a
    #print (json.dumps(commentsall))



def groups(directory):
    gj=[]
    gp=[]
    jsonfiles = common(directory)
    for file in jsonfiles:
        data=json.load(open(file))


        if 'group_posts' in data.keys():
            gp = len(data['group_posts'])
            #print('length of your group posts and comments :'+str(gp))
        if 'groups_joined' in data.keys():
            gj = len(data['groups_joined'])
            #print('number of groups joined'+str(gj))
            pass;

    return{'Number_of_Groups_Joined':gj,'Group_posts_and_comments':gp}
def messages(directory):

    jsonfiles = common(directory)

    jf = [os.path.join(root, name)
          for root, dirs, files in os.walk(directory)
          for name in dirs]
    #print("Total message folder are:" + str(len(jf)))

    # THIS IS TO FIND JSON FILES

    # path_to_json = jf[7]
    # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    maindirectory=os.path.dirname(directory)
    path_to_json1 = maindirectory+'/profile_information'
    json_files1 = [pos_json for pos_json in os.listdir(path_to_json1) if pos_json.endswith('profile_information.json')]
    count = 0

    for index, js in enumerate(json_files1):
        with open(os.path.join(path_to_json1, js)) as json_file:
            json_sext = json.load(json_file)

    ct = []
    cm = []
    bt = []
    dictionary = {}
    # we need both the json and an index number so use enumerate()
    for h in range(0, len(jf)):
        path_to_json = jf[h]
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        count_of_messages_sent_by_profile_name = 0
        count_of_message_sent_by_title = 0
        a = ''
        b=''
        for index, js in enumerate(json_files):
            with open(os.path.join(path_to_json, js)) as json_file:
                json_text = json.load(json_file)
                # len(json_text['messages'])
                contentbyself=""
                contentbyother=""
                b=json_sext["profile"]["name"]
                for i in range(0, len(json_text['messages'])):
                    try:
                        if (json_text["messages"][i]["sender_name"] == json_sext["profile"]["name"]):
                            count_of_messages_sent_by_profile_name += 1
                            a = json_text["title"]
                            contentbyself=contentbyself+' '+ json_text["messages"][i]['content']
                        elif (json_text["messages"][i]["sender_name"] == json_text["title"]):
                            count_of_message_sent_by_title += 1
                            a = json_text["title"]
                            contentbyother=contentbyother+' '+json_text["messages"][i]['content']
                    except:
                        pass;
                # #print contentbyself
                # #print contentbyother
                # yoursentiment=TextBlob(contentbyself).sentiment
                # othersentiment= TextBlob(contentbyother).sentiment
                # #print yoursentiment
                # #print othersentiment

                cm.append((a,count_of_message_sent_by_title,b,count_of_messages_sent_by_profile_name))
                #bt.append(count_of_message_sent_by_title)
                # jsons_data = json_text['messages'][i]['sender_name']

    # #print("Total messages"+str(len(json_text['messages'])))
    # #print('Messages sent by'+" "+str(json_sext["profile"]["name"])+" "+str(count))
    # #print('Messages sent by'+" "+str(json_text['title'])+" "+str(len(json_text['messages'])-count))
    #for i in range(0, len(ct)):
     #   a = {json_sext["profile"]["name"]: cm[i], ct[i]: bt[i]}
        # #print(ct[i]+" sent these many messages: "+str(cm[i])+" and "+json_sext["profile"]["name"]+" sent "+ str(bt[i])+" number of messages")
    #for i in dictionary.items():
     #   #print (i)
    return {'sentby':ct,'messages':cm}

def common(directory):
    #print('******************************************************')
    #print (inspect.stack()[1][3])
    jsonfiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                jsonfiles.append(os.path.join(root, file))
    return jsonfiles;


# paste your directory here
 # '/Users/apple/Downloads/facebook-avadecha'
jsonfiles = []
folders = []

# finding all the json files
# for root, dirs, files in os.walk(maindirectory):
#     for file in files:
#         if file.endswith(".json"):
#             jsonfiles.append(os.path.join(root, file))
#
# # getting root directories
# for i in range(0, len(jsonfiles)):
#     data = json.load(open(jsonfiles[i]))
#     if 'messages' not in data.keys():
#         folders.append(os.path.dirname(jsonfiles[i]))
#     else:
#         folders.append(os.path.dirname(os.path.dirname(jsonfiles[i])))
# # deleting duplicates
# folders = list(set(folders))
#
# # calling respective functions
# for i in range(0, len(folders)):
#     ###print(folders[i])
#
#     eval(os.path.basename(folders[i]))(folders[i])
