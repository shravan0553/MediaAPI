#!/usr/bin/python
# Libraries needed to perform actions
from collections import OrderedDict
import requests
from akamai.edgegrid import EdgeGridAuth
from urlparse import urljoin
import json
import sys
import csv
import argparse


# Set headers
headers = {'Content-Type': 'application/json'}

# credential file location
credential_file = 'credentials'

# ADD LIST OF STREAM ID's IN HERE
bkpPreferredRegions = [31363, 31364]
priPreferredRegions = [31438, 31439]

# input file location
input_file = 'turner_nba_streams1.csv'

# initialize the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--xbc', help='use this option to update XBC regions',action='store_true')
parser.add_argument('--ent', help='use this option to update entrypoint regions',action='store_true')
parser.add_argument('--arc', help='use this option to update Archive Settings',action='store_true')
parser.add_argument('--rem', help='use this option to delete the streams',action='store_true')
args = parser.parse_args()

###################### FUNCTIONS #######################################

# Prints JSON objects for Debugging

def print_response(response):
    print json.dumps(response, indent=4, sort_keys=False)

################# Get the streamId JSON via GET request  ###################

def update_stream_id(s, streamId, accountSwitchKey,baseUrl):
    response = s.get(urljoin(baseUrl, '/config-media-live/v2/msl-origin/streams/' +streamId))
    data = json.loads(response.text, object_pairs_hook=OrderedDict)
    xbcRegionUpdated = False
    xbcBkpRegionUpdated = False
    streamUpdated = False
    tpsData = data.get('tpsSettings', None)
    if tpsData == None:
    	##del data['tpsSettings']
    	data.update(tpsSettings={"inactiveOnly": True})

################### Updating XBC Regions #########################

    if args.xbc:
        xbcBkpRegionUpdated = False
        xbcRegionUpdated = False
        print "######### Updating XBC Regions ###########"
        xbcData = data.get("preferredXBCSettings", None)
        if xbcData != None:
            xbcRegions = data["preferredXBCSettings"]["primary"]["regions"]
            for i, regId in enumerate(xbcRegions):
                if regId == 31441:
                    xbcRegions[i] = 33022
                    xbcRegionUpdated = True
                if regId == 31325:
                    xbcRegions[i] = 33012
                    xbcRegionUpdated = True
            xbcBkpRegions = data["preferredXBCSettings"]["backup"]["regions"]
            for i, regId in enumerate(xbcBkpRegions):
                if regId == 31325:
                    xbcBkpRegions[i] = 33012
                    xbcBkpRegionUpdated = True
                if regId == 31441:
                    xbcBkpRegions[i] = 33022
                    xbcBkpRegionUpdated = True
            if xbcRegionUpdated == True:
                data["preferredXBCSettings"]["primary"]["regions"] = xbcRegions
            if xbcBkpRegionUpdated == True:
                data["preferredXBCSettings"]["backup"]["regions"] = xbcBkpRegions
            if xbcRegionUpdated == True or xbcBkpRegionUpdated == True:
                streamUpdated=True
            else:
                print "########## XBC Region match not found for " + streamId
        else:
            print "########## XBC Regions dont exist for " + streamId

################### Updating Entry Point Regions #########################

    if args.ent:
        print "######### Updating Entrypoint Regions ###########"
        #Set Preferred regions
        data["backupPreferredSettings"]["preferredRegions"] = bkpPreferredRegions
        data["primaryPreferredSettings"]["preferredRegions"] = priPreferredRegions
        streamUpdated=True
        print "######### Updated Entrypoint Regions ###########"

################### Updating Archive Settings #########################
    if args.arc:
        print "######### Updating Archive Settings ###########"
        archiveData  = data.get("events", None)
        if archiveData != None:
            data["events"] = []
            data.update(streamLevelPurgeDays=1)
            streamUpdated=True
            ##print_response(data)
        print "Updated Archive Settings for " + streamId

################## Update the streamId JSON via PUT request ########################

    if streamUpdated == True:
        response = s.put(urljoin(baseUrl, '/config-media-live/v2/msl-origin/streams/' + streamId), data=json.dumps(data, sort_keys=False), headers=headers)
        if response.status_code == 202:
            print "########## Succesfully updated the stream ID " + streamId + " Code:" + str(response.status_code)
        else :
            print "########## Failed updating the stream ID " + streamId + " Error Code: " + str(response.text)
            
################### Stream deletion #########################

    if args.rem:
        print "######### Deleting Streams ###########"
        response = s.delete(urljoin(baseUrl, '/config-media-live/v2/msl-origin/streams/' + streamId + '?accountSwitchKey=' + accountSwitchKey),headers=headers)
        if response.status_code == 202:
            print "########## Succesfully deleted the stream ID " + streamId + " Code:" + str(response.status_code)
        else :
            print "########## Failed deleting the stream ID " + streamId + " Error Code: " + str(response.text)
        print "#########  End Deleting Streams  ###########"
        
########################### MAIN #######################################

if len(sys.argv) > 1:
    try:
        with open(credential_file, mode='r') as readfile:
            credential = dict(x.replace(' ','').rstrip().split('=', 1) for x in readfile)  
    except:
        print('Error: Cannot find credential file or wrong format')

    baseUrl = 'https://' + str(credential['host']) + '/'
    clientToken = str(credential['client_token'])
    clientSecret = str(credential['client_secret'])
    accessToken = str(credential['access_token'])   
    s = requests.Session()
    s.auth = EdgeGridAuth(
    client_token=clientToken,
    client_secret=clientSecret,
    access_token=accessToken
    )
    with open(input_file, mode='r') as readfile:
        reader = csv.reader(readfile)
        for row in reader:
            # skip the 1st row as it is the column name
            if reader.line_num == 1:
                continue
            else:
                ## extract StreamID and contractID from each row ##
                streamId = row[1]
                # print streamId
                ## make API call to get stream info ##
                update_stream_id(s, streamId, accountSwitchKey,baseUrl)
    print("DONE: all streams have been updated")
    exit(0)
else:
    parser.print_help()

