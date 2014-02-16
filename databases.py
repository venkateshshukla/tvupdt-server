from google.appengine.ext import db
'''
This class contains the main database of the application. In this database, there are following entries

tvid    : IMDb id of the the Series
title   : Title of the Series
epname  : Name of the next Episode
epinfo  : Season And Episode Number in format S.E
epdate  : Date of the Next episode as available on IMDb servers
Rely codes
 0   - Running today
-1   - Past episode
 1   - Future episode
 2   - Incomplete information present - Either month or day absent
 3   - Air date is absent. No information about air date of this episode
 4   - Series is on hold - In between seasons. Its the last episode of last season
 99  - Default rely code on creating entry

 Status Codes
 99  - Series has probably ended. If not, next episode is not announced.
 1   - Series is running
 -1  - Default status on creating entry
'''

class Series(db.Model):
    tvid = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    status = db.IntegerProperty()
    epname = db.StringProperty()
    epinfo = db.StringProperty()
    epdate = db.StringProperty()
    rely = db.IntegerProperty()
    up_cycle = db.IntegerProperty()
    comments = db.StringProperty()


'''
This class contains the Series whose next episodes are to be found out.
'''
class ListSeries(db.Model):
    tvid = db.StringProperty(required=True)
    slno = db.IntegerProperty()
    title = db.StringProperty(required=True)

class UserPrefs(db.Model):
    regid = db.StringProperty(required=True)
    grey = db.IntegerProperty()             #Grey's Anatomy
    bones = db.IntegerProperty()            #Bones
    himym = db.IntegerProperty()            #How I Met Your Mother
    dexter = db.IntegerProperty()           #Dexter
    burn = db.IntegerProperty()             #Burn Notice
    bbt = db.IntegerProperty()              #The Big Band Theory
    bbad = db.IntegerProperty()             #The Breaking Bad
    naruto = db.IntegerProperty()           #Naruto Shippuden
    mentl = db.IntegerProperty()            #The Mentalist
    castle = db.IntegerProperty()           #Castle
    glee = db.IntegerProperty()             #Glee
    vamp = db.IntegerProperty()             #The Vampire's Diary
    walk = db.IntegerProperty()             #The Walking Dead
    suits = db.IntegerProperty()            #Suits
    home = db.IntegerProperty()             #Homeland

class Total(db.Model):
    total = db.IntegerProperty(required = True)
