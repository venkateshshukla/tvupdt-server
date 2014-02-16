'''
Module to get running status of a series given its imdb id
It takes IMDb id of any series as input and returns the latest episode object.
Rely codes
 0   - Running today
-1   - Past episode
 1   - Future episode
 2   - Incomplete information present - Either month or day absent
 3   - Air date is absent. No information about air date of this episode
 4   - Series is on hold - In between seasons. Its the last episode of last season

 Status Codes
 99  - Series has probably ended. If not, next episode is not announced.
 1   - Series is running
'''

def getNextEp(tvid):
    import imdb
    import re
    from datetime import date
    from IMDbDate import formatDate
    from ConvertUnicode import convert
    import logging

    logging.info("initialized")
    i = imdb.IMDb('mobile')

    series = i.get_movie(tvid)
    title = convert(series['title'])
    logging.info(title)
    if(series['kind'] == 'tv series'):
        i.update(series, "episodes")
        logging.info("updated")
        series = convert(series)
        series = series["episodes"]

        # taking up first episode of the last season and last episode of the second last
        # season to determine the present season

        # for some series, -1 key appears in the end of the list
        if(series.has_key(-1)):
          series.pop(-1);

        season_seclast = series[len(series) -1]
        season_last = series[len(series)]

        #in case of naruto the first episode doesn't have the key 1. Rather it is 25.
        # so the keys are sorted and then the smallest key is chosen. 
        if(season_last.has_key(1)):
            fdate = season_last[1]["original air date"]
        else:
            fdate = season_last.get(sorted(season_last.keys())[0])["original air date"]

        pdate = season_seclast[len(season_seclast)]["original air date"]

        bitch_present = re.split("-", str(date.today()))

        bitch_past = formatDate(pdate)
        bitch_future = formatDate(fdate)

        ypa = bitch_past[0][0]
        ypr = bitch_present[0]
        yfu = bitch_future[0][0]

        mpa = bitch_past[0][1]
        mpr = bitch_present[1]
        mfu = bitch_future[0][1]

        dpa = bitch_past[0][2]
        dpr = bitch_present[2]
        dfu = bitch_future[0][2]

        flag = 0
        if(ypa < ypr):
            flag = 1
        elif(ypa == ypr):
            if(mpa == 0):
                pass
            else:
                if(mpa < mpr):
                    flag = 1
                elif(mpa == mpr):
                    if(dpa == 0):
                        pass
                    else:
                        if(dpa < dpr):
                            flag = 1

        if(flag == 1):
            if(ypr < yfu):
                flag = 2
            elif(ypr == yfu):
                if(mfu == 0):
                    flag = 2
                else:
                    if(mpr < mfu):
                        flag = 2
                    elif(mpr == mfu):
                        if(dfu == 0):
                            pass
                        else:
                            if(dpr < dfu):
                                flag = 2
        if(flag == 0):
            status = "Sec Last"
            current_season = season_seclast
        elif(flag == 1):
            status = "Last"
            current_season = season_last
        elif(flag == 2):
            status = "on Hold"
            

        logging.info(status)

        if(flag == 2):
            nextEp = season_last[sorted(season_last.keys())[0]]
            nextEp["status"] = 0 # On hold
            nextEp["rely"] = 4   # On hold
            nextEp["comments"] = 'Between seasons'
            
        else: 
            for k in current_season.keys():
                try:
                    forDate = formatDate(current_season[k]["original air date"])
                except:
                    logging.error('No original air date is found for episode ' + str(k))
                    forDate = [[9999,0,0],0] # 0 implies no original air date on the episode
                current_season[k]["date"] = forDate[0]
                dt = current_season[k]["date"]
                if forDate[1] == 0:
                    current_season[k]["rely"] = 3  # No air date is present
                    current_season[k]['comments'] = 'No air date present'
                elif forDate[1] == 1:
                    current_season[k]["rely"] = 2  # Incomplete information present
                    current_season[k]['comments'] = 'Incomplete air date - YYYY'
                elif forDate[1] == 2 :
                    current_season[k]["rely"] = 2  # Incomplete information present
                    current_season[k]['comments'] = 'Incomplete air date - YYYY MM'
                else:
                    num = 365*(int(dt[0]) - int(ypr)) + 31*(int(dt[1]) - int(mpr)) + (int(dt[2]) - int(dpr))
                    running_status = num/abs(num)
                    current_season[k]["rely"] = running_status
                    if running_status == 1:
                        current_season[k]["comments"] = 'Not Aired yet'
                    elif running_status == -1:
                        current_season[k]["comments"] = 'Already aired'
                    elif running_status == 0:
                        current_season[k]["comments"] = 'Being aired today'

            keySet = sorted(current_season.keys())

            start = keySet[0]
            n = keySet[len(keySet) - 1]

            while(n >= start):
                if(current_season[n]["rely"] == -1):
                  lastKnown = n
                  break
                n -= 1

            if n != (start + len(keySet) -1) :
                nextEp = current_season[n+1]
                nextEp["status"] = 1
            elif n == start:
                logging.error("Something is wrong. This shouldn't have happened")
            else:
                nextEp = current_season[n]
                nextEp["status"] = 99
                nextEp["comments"] = 'Series ended'
                logging.info("No info about Season. Probably the series has ended.")
        return nextEp
    else:
        logging.info("given imdb id is not a tv series")
