import webapp2, logging
from google.appengine.ext import db
from databases import Total

class AddTotalDb(webapp2.RequestHandler):
    def get(self):
        logging.info('POST recieved')
        q = Total(0)
        q.put()
        logging.info('O stored in Total')
        
application= webapp2.WSGIApplication([("/addtotaldb",AddTotalDb),],debug=True)
