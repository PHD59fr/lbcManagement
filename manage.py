#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os
import core

from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    ##### Logger Settings #####
    logFormatter    = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger          = logging.getLogger()
    logger.setLevel(logging.INFO)

    fileLog         = os.path.splitext("/var/log/" + os.path.basename(__file__))[0] + ".log"
    fileHandler     = RotatingFileHandler(fileLog, maxBytes=1000, backupCount=5)  # Max 6 mb of logs
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler  = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    ###########################
    try:
        user = core.User()
        
        #Login
        login = user.auth()
        #logger.info(login['message']) if login['code'] == 200 else logger.error(login) and exit(1)
        
        #get Me
        myprofile = user.me()
        #logger.info(myprofile['message']) if myprofile['code'] == 200 else logger.error(myprofile) and exit(1)

        #get ADS
        myads = user.getAds()
        #logger.info(myads['message']) if myads['code'] == 200 else logger.error(myads) and exit(1)
        totalAds = len(myads['message'])
#        if totalAds:
#            for i in myads['message']:
#                print (i['url'])
#                print (i['subject'])
#                print (i['category_id'])
#                print (i['category_name'])
#                print (i['first_publication_date'])
#                print (i['expiration_date'])
#                print (i['has_phone'])
#                print (''.join(str(e) for e in i['price']))
#                print (i['location'])
#                print (i['body'])
        print (myads['message'])

    except KeyboardInterrupt:
        logger.warning("Exit instance")
