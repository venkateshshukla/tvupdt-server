import webapp2, logging
from google.appengine.ext import db
from google.appengine.api import memcache
from databases import Series, ListSeries, Total

class AddSeries(webapp2.RequestHandler):
    def post(self):
        data = self.payload
        auth = data['auth']
        if auth != 'NarutoStark':
            self.response.write('Unauthorised Request.')
        else:
            num = data['num']
            logging.info('Recieved ' + str(num) + ' Entries')
            
            allseries = data['allseries']
            for series in allseries:
                title = series['title']
                tvid = series['tvid']
                logging.info('title = ' + title)
                logging.info('tvid = ' + tvid)
                # Get total number of series in use from memcache. If unavailable try datastore
                mem_total = memcache.get('total')
                db_total_entry = Total.all().get()
                db_total = db_total_entry.total
                logging.debug('old mem_total = ' + str(mem_total))
                logging.debug('old db_total = ' + str(db_total))
                if mem_total is None:
                    slno = db_total +1
                    logging.debug('No total in memcache. Using datastore')
                else:
                    slno = total + 1
                    logging.debug('total found in memcache')
                logging.debug('slno = ' + str(slno))
                db_total_entry.total = slno
                db_total_entry.put()
                memcache.put('total', slno)
                logging.debug('Put new total in memcache and db')
                # End

                # Put the given series in ListSeries
                listseries = ListSeries(tvid=tvid, title=title)
                listseries.slno = slno
                listseries.put()
                logging.info('Entry put in ListSeries database')
                # End

                # Put the given series in Series
                db_series = Series(tvid=tvid, title=title)
                db_series.status    = -1            #Default
                db_series.rely      = 99            #Default
                db_series.epname    = 'None'        #Default
                db_series.epinfo    = '0.0'         #Default
                db_series.epdate    = 'dd mm yyyy'  #Default
                db_series.up_cycle  = 0             #Default
                db_series.comments  = 'No Comments' #Default
                db_series.put()
                logging.info('Entry put in Series database')
                #End
                self.response.write(title + ' put into the database.\n')
        
application= webapp2.WSGIApplication([("/addseries",AddSeries),],debug=True)
