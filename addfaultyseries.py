import webapp2, logging
from google.appengine.ext import db
from google.appengine.api import memcache
from FaultyDatabases import FaultySeries, FaultyListSeries, FaultyTotal

class AddFaultySeries(webapp2.RequestHandler):
    def post(self):
        data = self.request.params
        if 'auth' not in data.keys():
            self.response.write('Unauthorised Request.')
            logging.error('Unauthorised Request.')
        else:
            auth = data['auth']
            if auth != 'NarutoStark':
                self.response.write('Unauthorised Request.')
                logging.error('Unauthorised Request.')
            else:
                logging.info('Recieved an Entry')

                # Get total number of series in use from memcache. If unavailable try datastore
                mem_total = memcache.get('faultytotal')
                db_total_entry = FaultyTotal.all().get()
                db_total = db_total_entry.total
                logging.debug('old mem_total = ' + str(mem_total))
                logging.debug('old db_total = ' + str(db_total))
                if mem_total is None:
                    total = db_total + 1
                    logging.debug('No total in memcache. Using datastore')
                else:
                    total = mem_total + 1
                    logging.debug('total found in memcache')
                # End
                
                title   = data['title']
                tvid    = data['tvid']
                slno    = total
                logging.info('title = ' + str(title))
                logging.info('tvid = ' + str(tvid))

                # Put the given series in ListSeries after checking if its already present
                lsquery = FaultyListSeries.all()
                lsquery.filter('tvid =', tvid)
                lsout = lsquery.get()
                if lsout is None:
                    listseries = FaultyListSeries(tvid=tvid, title=title)
                    listseries.slno = slno
                    listseries.put()
                    logging.info('Entry put in FaultyListSeries database')
                    # End

                    # Put the given series in Series after checking if its already present
                    # If already present then, reset the values
                    squery = FaultySeries.all()
                    squery.filter('tvid =', tvid)
                    sout = squery.get()
                    if sout is not None:
                        db_series = sout
                    else:
                        db_series = FaultySeries(tvid=tvid, title=title)
                    db_series.status    = -1            #Default
                    db_series.rely      = 99            #Default
                    db_series.epname    = 'None'        #Default
                    db_series.epinfo    = '0.0'         #Default
                    db_series.epdate    = 'dd mm yyyy'  #Default
                    db_series.up_cycle  = 0             #Default
                    db_series.comments  = 'No Comments' #Default
                    db_series.put()
                    logging.info('Entry put in FaultySeries database')
                    #End

                    # Now put the updated value in datastore and memcache
                    logging.debug('slno = ' + str(total))
                    db_total_entry.total = total
                    db_total_entry.put()
                    memcache.set('faultytotal', total)
                    logging.debug('Put new total in memcache and db')
                    # End
                    
                    self.response.write(title + ' put into the faultydatabase.\n')
                else:
                    self.response.write('The series is already present in FaultyListSeries database')
                    logging.error('Series already in FaultyListSeries database')

application= webapp2.WSGIApplication([("/addfaultyseries",AddFaultySeries),],debug=True)
