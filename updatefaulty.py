# This script updates the database on getting a GET request by CRON jobs.

import webapp2, logging, imdb
from google.appengine.ext import db
from google.appengine.api import memcache
from NextEp import getNextEp
from FaultyDatabases import FaultySeries, FaultyListSeries, FaultyTotal

class UpdateFaultySeries(webapp2.RequestHandler):
    '''
    On receiving a GET request (From a cron job mainly) these steps are undertaken

    1. Extractor iterator value from Memcache and the maximum value
    2. Corresponding to the iterator value, extract the movie ID from ListSeries class
    3. Extract all the information of the series and update the database
    '''
    def get(self):
        logging.info("Received a GET Request")

        iterator = memcache.get('faultyiterator')     #Get value of iterator in memcache
        total = memcache.get('faultytotal')           #Get value of total in memcache

        if iterator is None:                    # In case there is no iterator, make an iterator and initialise with value 0
            iterator = 0
            memcache.add('faultyiterator',iterator)

        if total is None:                       # In case there is no total in the memcache, get total from datastore and add to memcache
            db_total = FaultyTotal.all().get()
            total = db_total.total
            memcache.add('faultytotal', total)

        iterator = iterator + 1                 #Incrementing the iterator and reset if equal to max
        if(iterator >= total+1):
            iterator = 1

        memcache.set('faultyiterator', iterator)
        logging.info("New Iterator Value " + str(iterator))
        # Now get the corresponding id from ListSeries

        lsquery = FaultyListSeries.all()
        lsquery.filter("slno =", iterator)
        serial = lsquery.get()
        
        stvid = serial.tvid
        logging.info("IMDb ID " + stvid)
        self.response.write(stvid)   

        episode = getNextEp(stvid)

        epNum = episode["episode"]
        seaNum = episode["season"]
        epName = episode["title"]
        epStat = episode["status"]
        epRely = episode["rely"]
        epComments = episode['comments']
        
        if epRely == 3:                                 # No air date present
            epDate = 'Unavailable'
        else:
            epDate = episode["original air date"]   

        if epStat != 99:
            logging.info("Episode Number " + str(epNum))
            logging.info("Season Number " + str(seaNum))
            logging.info("Episode Title " + epName)
            logging.info("Status " + str(epStat))
            logging.info("Reliable " + str(epRely))
            logging.info("Next Episode date " + epDate)
            logging.info("Comments " + epComments)
        else:
            logging.warn("There is no information about the next episode. Probably the series has been terminated.")
            logging.info("Last Known Episode Number " + str(epNum))
            logging.info("Last Known Season Number " + str(seaNum))
            logging.info("Last Known Episode Title " + epName)
            logging.info("Status " + str(epStat))
            logging.info("Reliable " + str(epRely))
            logging.info("Last Known Episode date " + epDate)
            logging.info("Comments " + epComments)

        Ser = FaultySeries.all()
        Ser.filter('tvid = ', str(stvid))
        ser1 = Ser.get()

        logging.info("entry extracted from FaultyDatastore")

        ser1.status = epStat
        ser1.rely = epRely
        ser1.epname = epName
        ser1.epinfo = str(seaNum) + "." + str(epNum)
        ser1.epdate = epDate
        ser1.up_cycle = ser1.up_cycle + 1
        ser1.comments = epComments

        ser1.put()

        logging.info(" Updated data written to FaultyDatastore")

application= webapp2.WSGIApplication([("/updatefaulty",UpdateFaultySeries),],debug=True)
