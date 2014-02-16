# Script to manipulate imdb dates

def formatDate(strdate):
    import re
    array = re.split("\. |, | ", strdate)
    month_dict = {"Jan" :"01", "Feb" : "02", "Mar" : "03",
              "Apr" : "04", "May" : "05", "Jun" : "06",
              "Jul" : "07", "Aug" : "08", "Sep" : "09",
              "Oct" : "10", "Nov" : "11", "Dec" : "12"
              }

    arr = [0,0]
    
    if(len(array) == 1):
        arr[1] = 1
        array.insert(1,0)
        array.insert(2,0)
        
    elif(len(array) == 2):
        arr[1] = 2
        a = array[0]
        array[1] = month_dict.get(array[1])
        array[0] = a
        array.insert(2,0)
        
    elif(len(array) == 3):
        arr[1] = 3
        a = array[0]
        b = array[2]
        array[1] = month_dict.get(array[1])
        array[0] = b
        array[2] = a

    arr[0] = array
    return arr    
