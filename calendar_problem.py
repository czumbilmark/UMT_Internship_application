
#reads the input information, from the console
def readFromConsole():
    #read info, from the console
    cal1 = eval(input("booked calendar1:"))
    range1 = eval(input("calendar1 range limits:"))
    cal2 = eval(input("booked calendar2:"))
    range2 = eval(input("calendar2 range limits:"))
    meetingTime = int(input("Meeting Time Minutes: "))
    return cal1,range1,cal2,range2,meetingTime

# reads the input information, from a file formated strictly 
def readFromFile(inFile):
    with open(inFile, 'r') as file: #read the file line by line
        lines = file.readlines()

    #import calendars and ranges, from corresponding ,line
    cal1 = eval(lines[0].split(': ')[1])
    range1 = eval(lines[1].split(': ')[1])
    cal2 = eval(lines[2].split(': ')[1])
    range2 = eval(lines[3].split(': ')[1])
    meetingTime = int(lines[4].split(': ')[1])

    return cal1,range1,cal2,range2,meetingTime

#Converts "hh:mm" format, to minute (integer), so it can be used as index 
def timeToIndex(time):
    index = 0
    time = time.split(":")
    index += int(time[0]) * 60
    index += int(time[1])
    return index

#Converts an index to its correspondint time string in "hh:mm" format
def indexToTime(index):
    h = int(index/60)
    min = int(index%60)
    if min < 10:
        min = '0' + str(min)
    time = str(h) + ':' + str(min)
    return(time)

#increments the values of cal from index start, to index end *(start does not necessarily has to be smaller then end)
#start and end should be in bounds ov the cal, so 0 <= start,end <= 1440
def incFromTo(start, end, cal):
    if(start > end):
        tmp = start
        start = end
        end = tmp
    for i in range(start,end+1):
        cal[i] += 1
    return cal


#generates a filed calendar, in which the free meeting times are the minutes vith value 0
def fillCalendar(cal1,range1,cal2,range2):
    #calendar is a list initialised with zeros
    finalCalendar = [0] * 1440         # 1440 minutes in a day

    #We start with a calendar full of zeros, and increment each unavailable minute, by both booked calendar inputs
    #in the end we should see a calendar containing 0,1 or 2 values, 2 meaning it is unavailable for both, 1 meaning
    #it is unavailable for one of the two, and 0 meaning it is available for both

    #we incremen the minutes outside of the calendar ranges
    finalCalendar = incFromTo( 0 ,timeToIndex(range1[0])-1,finalCalendar)
    finalCalendar = incFromTo(timeToIndex(range1[1])+1,1439,finalCalendar)
    finalCalendar = incFromTo(0, timeToIndex(range2[0])-1,finalCalendar)
    finalCalendar = incFromTo(timeToIndex(range2[1])+1,1439,finalCalendar)

    

    # and increment the already booked time of the first calendar 
    for item in cal1:
        finalCalendar = incFromTo(timeToIndex(item[0])+1,timeToIndex(item[1])-1,finalCalendar)

    # and increment the already booked time of the second calendar 
    for item in cal2:
        finalCalendar = incFromTo(timeToIndex(item[0])+1,timeToIndex(item[1])-1,finalCalendar)

    return finalCalendar

# generates the list of all available at least "minTime" minute long meeting times, in "hh:mm" format 
def findMeetTimes(cal, minTime):
    index = 0
    freeTime = []
    while (index < 1440):
        count = 0
        start = index
        
        #we measure the length of a potential 0 sequence
        while(index < 1440 and cal[index] == 0):
            count += 1
            index += 1
        
        #we check if we had more than minTime free time, if yes, we store this time frame in our list
        if count >= minTime:
            freeTime.append([indexToTime(start),indexToTime(index-1)])
        
        #we can increment, because we know, that this index's value is not 0 because it stoped the while
        index += 1

    return freeTime


#prints the liset to given output file
def printToFile(filename, mTimes):
    f = open(filename,'a')
    f.write(str(mTimes))
    f.close()




cal1,range1,cal2,range2,minutes = readFromConsole()
# alternatively:
#cal1,range1,cal2,range2,minutes = readFromFile("input.txt")

finalCalendar = fillCalendar(cal1,range1,cal2,range2)
meetTimes = findMeetTimes(finalCalendar,minutes)
print(meetTimes)
printToFile("output.txt", meetTimes)



