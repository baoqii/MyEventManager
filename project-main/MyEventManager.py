# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
from dateutil.relativedelta import relativedelta
from googleapiclient.errors import HttpError
import datetime as dt
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Classes import *
import MyEventManagerApp
from pprint import pprint
import json
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


eventList = []
cancelledEventList = []

def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def get_all_events(api):
    """
    Returns a list of all events in the user's calendar within the past 5 years and 5 years in the future.
    It takes one argument, which is an instance of the Google Calendar API.
    
    :param api: Google Calendar API
    :return: A list of Event objects
    :References: https://stackoverflow.com/questions/49226162/google-calendar-api-querying-all-events-for-the-last-1-months-in-python
    """
    end_time = (dt.datetime.utcnow() + relativedelta(years=5)).isoformat() + 'Z'
    start_time = (dt.datetime.utcnow() - relativedelta(years=5)).isoformat()+'Z'
    events_result = api.events().list(calendarId='primary', timeMax=end_time,
                                        timeMin = start_time, 
                                        singleEvents=True, orderBy='startTime',showDeleted=True).execute()
    eventItems = events_result.get('items', [])
    eventList.clear()
    for data in eventItems:
        try:
            event = Event.fromData(api,data)
            eventList.append(event)
        except:
            pass  
    return eventList
    
def acceptEventInvite(api, eventId):
    """
    Takes in an event ID and accepts the invite for that event, this action is only allowed for attendees of that event.
    If it is an attendee, the email of the attendee will be obtained and the responseStatus of that attendee will be changed to ‘accepted’.
    It returns the updatedEvent if successful, False otherwise.
    
    :param api: Google Calendar API
    :param eventId: a string representing the Event ID of the event that the user wants to update
    :return: The updated event
    """
    event = api.events().get(calendarId='primary',eventId=eventId).execute()
    isAttendee = Attendee.checkIsAttendee(event)
    try:
        if not isAttendee:
            raise Exception("Only attendees can change their response status to an event")
        new_attendee_list = []
        for attendee in event['attendees']:
            if attendee.get('self', attendee.get('self')) == True:
                attendeeEmail = attendee.get('email', attendee.get('email'))
                attendeeRS ={'email': attendeeEmail, 'self': 'True', 'responseStatus':"accepted"}
                new_attendee_list.append(attendeeRS)
            else:
                new_attendee_list.append(attendee)
        updatedEvent = api.events().patch(calendarId='primary',
                                                    eventId=eventId,
                                                    body={"attendees":new_attendee_list},
                                                    sendUpdates="all").execute() 
        print(f'Response status was successfully updated')
        return updatedEvent
    except Exception as e:
        print(e)
        print(f'Response Status was not successfully updated')
        return False

def rejectEventInvite(api, eventId):
    """
    Takes in an event ID and rejects the invite for that event, this action is only allowed for attendees of that event.
    It returns the updatedEvent if successful, False otherwise.
    
    :param api: Google Calendar API
    :param eventId: a string representing the Event ID of the event that the user wants to update
    :return: The updated event
    """
    event = api.events().get(calendarId='primary',eventId=eventId).execute()
    isAttendee = Attendee.checkIsAttendee(event)
    try:
        if not isAttendee:
            raise Exception("Only attendees can change their response status to an event")
        new_attendee_list = []
        for attendee in event['attendees']:
            if attendee.get('self', attendee.get('self')) == True:
                attendeeEmail = attendee.get('email', attendee.get('email'))
                attendeeRS ={'email': attendeeEmail, 'self': 'True', 'responseStatus':"declined"}
                new_attendee_list.append(attendeeRS)
            else:
                new_attendee_list.append(attendee)
        updatedEvent = api.events().patch(calendarId='primary',
                                                    eventId=eventId,
                                                    body={"attendees":new_attendee_list},
                                                    sendUpdates="all").execute() 

        print(f'Response status was successfully updated')
        return updatedEvent
    except Exception as e:
        print(e)
        print(f'Response Status was not successfully updated')
        return False

def getCancelledEvents(api):
    events_result = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime',showDeleted=True).execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    successful = 0
    failed = 0
    cancelledEventList.clear()
    for event in events:
        if(event['status']=='cancelled'):
            try:
                eventObj = Event.fromData(api,event)
                start = event['start'].get('dateTime', event['start'].get('date'))
                if(dt.datetime.now()<=eventObj.startDate.getTime()):
                    cancelledEventList.append(eventObj)    
                    print(start, event['summary'])
                    successful += 1
            except:
                failed += 1
    print("valid events: %d" % successful)
    print("invalid events: %d" % failed)
    return cancelledEventList 

def changeOrganiser(api, eventId, newOrganiserEmail):
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")


        if not Attendee.isEmailValid(newOrganiserEmail):
            raise Exception("Invalid email")

        updatedEvent = api.events().move(calendarId='primary',eventId=eventId,destination=newOrganiserEmail,sendUpdates="all").execute()

        print(f'Event Organiser changed successfully to {newOrganiserEmail} on {updatedEvent["updated"]}.')
        return True
    except Exception as e:
        print(e)
        print(f'Event Organiser was not changed successfully.')
        return False

def addAttendee(api, eventId,newAttendeeEmail):
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")

        if not Attendee.isEmailValid(newAttendeeEmail):
            raise Exception("Invalid email")

        attendees = event['attendees']
        nbrOfInitialAttendees = len(attendees)

        if nbrOfInitialAttendees == 20:
            raise Exception("Event has reached a maximum of 20 attendees")

        attendees.append({"email":newAttendeeEmail})
        updatedEvent = api.events().patch(calendarId='primary',eventId=eventId,body={"attendees":attendees},sendUpdates="all").execute()

        if (len(updatedEvent['attendees']) == nbrOfInitialAttendees):
            raise Exception(f'{newAttendeeEmail} is already an attendee in this event')
        else:
            print(f'{newAttendeeEmail} was added to event {eventId} on {updatedEvent["updated"]}.')

        return updatedEvent['attendees']
    except Exception as e:
        print(e)
        print(f'{newAttendeeEmail} was not added successfully to event {eventId} as attendee.')
        return False

def removeAttendee(api, eventId,attendeeEmail):
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")

        if not Attendee.isEmailValid(attendeeEmail):
            raise Exception("Invalid email")

        attendees = event['attendees']
        nbrOfInitialAttendees = len(attendees)
        attendees = list(filter(lambda attendee: attendee['email'] != attendeeEmail, attendees)) # get attendees that are not attendeeEmail
        updatedEvent = api.events().patch(calendarId='primary',eventId=eventId,body={"attendees":attendees},sendUpdates="all").execute() # update event with new attendee list

        if len(attendees) == (nbrOfInitialAttendees-1):
            print(f'{attendeeEmail} was removed from event {eventId} on {updatedEvent["updated"]}.')
        else:
            raise Exception(f'{attendeeEmail} is not an attendee in this event.')
        return updatedEvent['attendees']
    except Exception as e:
        print(e)
        print(f'{attendeeEmail} was not removed successfully from event {eventId} as attendee')
        return False

def changeEventDate(api,eventId,startDate,startTime,endDate,endTime): 
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")

        if not (Date.isDateValid(startDate) and Date.isTimeValid(startTime)):
            raise Exception("Do ensure start date and time is in correct format")

        if not (Date.isDateValid(endDate) and Date.isTimeValid(endTime)):
            raise Exception("Do ensure end date and time is in correct format")

        if not (Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime)):
            raise Exception("Start date and time must be before end date and time")

        start = Date(startDate,startTime)
        end = Date(endDate,endTime)
        
        updatedEvent = api.events().patch(calendarId='primary',
                                            eventId=eventId,
                                            body={
                                                "start":{"dateTime":str(start)},
                                                "end":{"dateTime":str(end)}
                                            },
                                            sendUpdates="all").execute() 
        print(f'Date was successfully updated')
        return updatedEvent
    except Exception as e:
        print(e)
        print(f'Date was not successfully updated')
        return False

def importEventFromJSON(api,jsonFilePath):
    '''
    Loads a JSON file in valid format and adds as event
    '''
    try:
        f = open(jsonFilePath)
        event = json.load(f)
        event = api.events().insert(calendarId='primary', body=event).execute()
        print (f'Event created: %s' % (event.get("htmlLink")))
        return True
    
    except FileNotFoundError as e:
        print(e)
        return "File not found"
    
    except json.JSONDecodeError as e:
        print(e)
        return "Incorrect JSON file format"
    
    except HttpError as e:
        print(e)
        return "Incorrect format for creation of event"

def checkForEventNotifications(eventList):
    notifiableEventList = []
    for event in eventList:
        for notif in event.popupNotifMinuteList:
            timeDifference = abs(dt.datetime.now() - event.startDate.getTime())
            if(timeDifference <= dt.timedelta(minutes=notif)):
                notifiableEventList.append(event)
                break
    return notifiableEventList  

def exportEventToJSON(api,eventId,exportLocation=None):
    '''
    Exports an event into JSON file. 
    Export location path accepts separator with / only. 
    If exportLocation is None, export to current directiory
    '''
    try:
        event = api.events().get(calendarId='primary', eventId=eventId).execute()
        fileName = '_'.join(event['summary'].split()) + ".json"

        if not exportLocation:
            path = fileName
        else:
            exportLocation = exportLocation.split("/")
            exportLocation.append(fileName)
            path = os.path.join(*exportLocation)

        with open(path,"w") as outfile:
            json.dump(event,outfile,indent=4)
        print(f"Event JSON file created at {path}")
        return path
    
    except FileNotFoundError:
        print("Directory not found")
        return False

def changeEventTitle(api,eventId,newTitle):
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")
        
        if not newTitle:
            raise Exception("New event tile cannot be empty")

        updatedEvent = api.events().patch(calendarId='primary',
                                            eventId=eventId,
                                            body={
                                                "summary":newTitle
                                            },
                                            sendUpdates="all").execute() 
        print(f'Title was successfully updated to {newTitle}')
        return updatedEvent["summary"]
    except Exception as e:
        print(e)
        print(f'Title was not successfully updated')
        return False

def changeEventDescription(api,eventId,newDescription):
    try:
        event = api.events().get(calendarId='primary',eventId=eventId).execute()

        # Check if is organiser
        isOrganiser = Attendee.checkIsOrganiser(event)
        if not isOrganiser:
            raise Exception("Only organisers are allowed to update the event details")

        if not newDescription:
            raise Exception("New event description cannot be empty")

        updatedEvent = api.events().patch(calendarId='primary',
                                            eventId=eventId,
                                            body={
                                                "description":newDescription
                                            },
                                            sendUpdates="all").execute() 
        print(f'Description was successfully updated to {newDescription}')
        return updatedEvent["description"]
    except Exception as e:
        print(e)
        print(f'Description was not successfully updated')
        return False

def getNavigatedEvents(api,year="",month="",day=""):
    if year and not month and not day:
        if Date.isDateValid("-".join([year,"01","01"]),viewing=True):
            timeMin = Date("-".join([year,"01","01"]),"00:00")
            timeMax = Date("-".join([year,"12","31"]),"23:59")
            

            events_result = api.events().list(calendarId='primary', 
                                            timeMin=str(timeMin),
                                            timeMax=str(timeMax),
                                            timeZone="Asia/Singapore",
                                            singleEvents=True,
                                            orderBy='startTime').execute()
            events = events_result.get('items', [])
        else:
            return False

    elif year and month and not day:
        if Date.isDateValid("-".join([year,month,"01"]),viewing=True):
            timeMin = Date("-".join([year,month,"01"]),"00:00")
            timeMax = Date("-".join([year,month,"28"]),"23:59")
            events_result = api.events().list(calendarId='primary', 
                                            timeMin=str(timeMin),
                                            timeMax=str(timeMax),
                                            timeZone="Asia/Singapore",
                                            singleEvents=True,
                                            orderBy='startTime').execute()
            events = events_result.get('items', [])
        else:
            return False

    elif year and month and day:
        if Date.isDateValid("-".join([year,month,day]),viewing=True):
            timeMin = Date("-".join([year,month,day]),"00:00")
            timeMax = Date("-".join([year,month,day]),"23:59")
            events_result = api.events().list(calendarId='primary', 
                                            timeMin=str(timeMin),
                                            timeMax=str(timeMax),
                                            timeZone="Asia/Singapore",
                                            singleEvents=True,
                                            orderBy='startTime').execute()
            events = events_result.get('items', [])
        else:
            return False

    else:
        print("Specify either year, or year and month, or year and month and day") 
        return False   


    # if not events:
    #     print('No upcoming events found.')
    # for i,event in enumerate(events):
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(f"{i+1}) {start} {event['summary']}")
    return events

def navigateForward(year="", month="", day=""):
    """
    Takes year, month and day as arguments.
    If no arguments are given it will return False.
    If only year is given it will return the next year.
    If both year and month are given it will return the next month.
    If all three are given it will return the next day.
    These return arguments will be passed to function getNavigatedEvents to retrieve the list of events.
    
    :param year: The year that the user is currently in
    :param month: The month the user is currently in
    :param day: The day the user is currently in
    :return: The new year, month, day to be navigate to
    """
    # return the new year month day
    if year and not month and not day:
        year = str(int(year) + 1)
        return year,month,day

    elif year and month and not day:
        month = int(month) + 1
        if month > 12:
            return str(int(year)+1),"01",""
        return year,str(month).rjust(2,"0"),day

    elif year and month and day:
        day = int(day) + 1
        month = int(month)
        year = int(year)
        if day > 31:
            if month == 12:
                return str(year+1),"01","01"
            else:
                return str(year),str(month+1).rjust(2,"0"),"01"
        else:
            return str(year),str(month).rjust(2,"0"),str(day).rjust(2,"0")
    else:
        return False

def navigateBackward(year="", month="", day=""):
    """
    Takes year, month and day as arguments.
    If only the year is passed in, it will return the previous year. 
    If both the year and month are passed in, it will return that previous month. 
    If all three are passed in, it will return that previous day.
    These return arguments will be passed to function getNavigatedEvents to retrieve the list of events.
    
    :param year: The year that the user is currently in
    :param month: The month the user is currently in
    :param day: The day the user is currently in
    :return: The previous day, month and year to be navigated to
    """
    if year and not month and not day:
        year = str(int(year) - 1)
        return year,month,day

    elif year and month and not day:
        month = int(month) - 1
        if month < 1:
            return str(int(year)-1),"12",""
        return year, str(month).rjust(2,"0"), day

    elif year and month and day:
        day = int(day) - 1
        month = int(month)
        year = int(year)
        if day < 1:
            if month == 1:
                return str(year-1),"12","31"
            else:
                return str(year),str(month-1).rjust(2,"0"),"31"
        else:
            return str(year), str(month).rjust(2,"0"), str(day).rjust(2,"0")
    else:
        return False
        
def searchEvent_by_name_keyword(api, query):
    """
    Searches for events in the user's primary calendar that matches event name or contains a keyword and returns them.
    
    :param api: Google Calendar API
    :param query: String representing the event name or keyword the user wants to search for
    :return: A list of events that match the query, if there is no matching events an empty list will be returned
    """
    query = query.lower()
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                        q=query,orderBy='startTime').execute()
    return events_result.get('items', [])

def searchEvent_by_date(api, event_date):
    """
    Searches for events in the user's primary calendar that start on the specified date.
    It returns a list of all events found on that day.
    
    :param api: Google Calendar API
    :param event_date: Specify the date of the event in YYYY-MM-DD or DD-MON-YY format
    :return: A list of events that matches the specified date, if there is no matching events an empty list will be returned
    """
    if Date.isDateValid(event_date):
        event_start = Date(event_date, "00:00")
        event_end = Date(event_date,"23:59")
        events_result = api.events().list(calendarId='primary', singleEvents=True,
                                        timeMin=str(event_start), timeMax =str(event_end),
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
    
    else:
        print("Specify a valid date to search for events")
        return False

    return events

if __name__ == "__main__":
    try:
        console = MyEventManagerApp.App(get_calendar_api())
        console.start()
    except FileNotFoundError as e:
        print(e)
