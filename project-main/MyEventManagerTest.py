import unittest
import datetime as dt
from unittest.mock import MagicMock, Mock, patch
from googleapiclient.errors import HttpError
import MyEventManager
from MyEventManager import *
from Classes import *
import json
import os
import shutil
import sys
from contextlib import contextmanager
from io import StringIO
from MyEventManagerApp import *


@contextmanager
def generateAutoInputAndOutput(inputList=[]):
    inIO = StringIO("\n".join(inputList))
    outIO = StringIO()
    prevIn = sys.stdin
    prevOut = sys.stdout
    try:
        sys.stdin = inIO
        sys.stdout = outIO
        yield sys.stdin, sys.stdout
    finally:
        sys.stdin = prevIn
        sys.stdout = prevOut
def createMockEvent(api=MagicMock(name="calendarMock"),name= "Party",location=Location("98 Shirley Street PIMPAMA QLD 4209"),attendees=[Attendee("bobross@gmail.com")],owner=Attendee("bobross@gmail.com"),organizer=Attendee("bobross@gmail.com",True),startDate=Date("2022-02-22"),endDate=Date("2022-02-22"),isAttending=False):
    return  Event(api,name,location,attendees,organizer,owner,startDate,endDate,isAttending,emailNotifMinuteList=[],popupNotifMinuteList=[])
def createEventData(name="Party",address='98 Shirley Street PIMPAMA QLD 4209',attendees=["bobross@gmail.com"],organiser='fakeemail@gmail.com',owner='mariosusanto161@gmail.com',startDateStr='2022-09-22T02:00:00+08:00',endDateStr='2022-09-24T12:00:00+08:00',cancelled=False,organiserIsSelf=True,ownerIsSelf=True):
    return  {
                'kind': 'calendar#event', 'etag': '"3327157843918000"', 'id': '7tddvde2rgaobf7qam30r7pteg', 
                'status': 'cancelled' if cancelled else 'confirmed', 
                'htmlLink': 'https://www.google.com/calendar/event?eid=N3RkZHZkZTJyZ2FvYmY3cWFtMzByN3B0ZWcgbWFyaW9zdXNhbnRvMTYxQG0', 
                'created': '2022-09-19T09:15:21.000Z', 'updated': '2022-09-19T09:15:22.084Z', 
                'summary': name, 'location': address, 
                'creator': {'email': owner, 'self': ownerIsSelf}, 
                'organizer': {'email': organiser, 'self': organiserIsSelf}, 
                'start': {'dateTime': startDateStr, 'timeZone': 'Asia/Singapore'}, 
                'end': {'dateTime': endDateStr, 'timeZone': 'Asia/Singapore'}, 
                'iCalUID': '7tddvde2rgaobf7qam30r7pteg@google.com', 'sequence': 0, 
                'attendees': [{'email': email, 'responseStatus': 'needsAction'} for email in attendees], 
                'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 60}]}, 
                'eventType': 'default'
            }
getDateTime = lambda year, month, day, hour, minute: dt.datetime(year,month,day,hour,minute)
class GetAllEventsTest(unittest.TestCase):
    def setUp(self):
        """
        The setUp function is called before each test function. It is used to
        set up the objects that the tests will use. 
        """
        self.eventsOn2023Nov = [{'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                                {'email': 'gtan0021@student.monash.edu',
                                                'organizer': True,
                                                'responseStatus': 'needsAction',
                                                'self': True}],
                                'created': '2022-09-23T19:31:23.000Z',
                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'end': {'dateTime': '2023-11-12T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                'etag': '"3327998803674000"',
                                'eventType': 'default',
                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                'kind': 'calendar#event',
                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                            {'method': 'popup', 'minutes': 10}],
                                                'useDefault': False},
                                'sequence': 1,
                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                'status': 'confirmed',
                                'summary': 'Party 1',
                                'updated': '2022-09-24T16:35:19.824Z'},
                                {'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                                {'email': 'gtan0021@student.monash.edu',
                                                'organizer': True,
                                                'responseStatus': 'needsAction',
                                                'self': True}],
                                'created': '2022-09-23T19:25:04.000Z',
                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'end': {'dateTime': '2023-11-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                'etag': '"3327998329967000"',
                                'eventType': 'default',
                                'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                                'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                                'kind': 'calendar#event',
                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                            {'method': 'popup', 'minutes': 10}],
                                                'useDefault': False},
                                'sequence': 4,
                                'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                'status': 'confirmed',
                                'summary': 'Party 1',
                                'updated': '2022-09-24T16:33:45.612Z'}]
        self.eventResultsFor2023Nov = {'accessRole': 'owner',
                                    'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                    'etag': '"p33kdp2t0tqmvk0g"',
                                    'items': [{'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:31:23.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-12T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998803674000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 1,
                                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:35:19.824Z'},
                                            {'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:25:04.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-26T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998329967000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                                                'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 4,
                                                'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:33:45.612Z'}],
                                    'kind': 'calendar#events',
                                    'summary': 'gtan0021@student.monash.edu',
                                    'timeZone': 'Asia/Singapore',
                                    'updated': '2022-09-24T16:36:04.625Z'}

    def test_get_all_events(self):
        """
        Tests whether the get_all_events function in MyEventManager.py
        It does this by creating a mock object for the Google Calendar API and then calling 
        the get_all_events function with that mock object as an argument. It then checks to see if 
        the events returned is equal to the exmaple Events provided.
        
        :return: A list of all the events that are in the calendar within 5 years in the past and 5 yearrs in the future.
        """
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value = self.eventResultsFor2023Nov
        events = MyEventManager.get_all_events(mock_api)
        for i,event in enumerate(events):
            self.assertEqual(event.id, self.eventsOn2023Nov[i]['id'])

class GetCancelledEventsTest(unittest.TestCase):
    @patch("MyEventManager.dt")
    def testGetCancelledEvents(self,mockDT):
        """
        Test that checks whether cancelled events can be obtained from the API correctly
        """
        api = MagicMock()
        data = {
            'items' : [
                createEventData(name="event1",cancelled=True),
                createEventData(name="event2",cancelled=False),
                createEventData(name="event3",cancelled=True,startDateStr='2019-12-30T18:00:00+08:00',endDateStr='2019-12-30T20:00:00+08:00'),
                createEventData(name="event4",cancelled=True)
            ]
        }
        api.events.return_value.list.return_value.execute.return_value = data
        mockDT.datetime.now.return_value = dt.datetime(2020,4,10,8,30)
        cancelledEventsList = getCancelledEvents(api)
        self.assertEqual(2,len(cancelledEventsList))
        self.assertEqual('event1',cancelledEventsList[0].name)
        self.assertEqual('event4',cancelledEventsList[1].name)

class LocationTest(unittest.TestCase):    
    def setUp(self):
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': False},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '5 Dalmation Road LA 33311',
                                    'organizer': {'email': 'georgetan615@gmail.com','self':False},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '3 Las Vegas Street LV 21458',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleNewLocationEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '48 King Country Square TX 31113',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'New title',
                                    'updated': '2022-09-20T04:30:29.245Z'}

    def testLocationNoAddressVirtual(self):
        """
        Test that checks if the location creation fails if the location is considered physical
        despite the location address being online
        """
        location = Location("Online"); 
        location.isPhysical = True 
        self.assertRaises(AssertionError,lambda: location.validateSelf()) 
    def testLocationNoAddressPhysical(self):
        """
        Test that checks if online locations are created correctly
        """
        address = "Online"
        event = createMockEvent(location=Location(address))
        self.assertEqual(address,event.location.address)
    def testLocationNoValidStreetOrEquivalent(self):
        """
        Test that checks if location creation fails if there isn't the word "Street" or a synonym thereof
        within the address
        """
        self.assertRaises(AssertionError,lambda: Location("76 Golden Bridge CA 93431")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("76 Golden Bridge CA 93431"))) 
    def testLocationNotEnoughWordsInAddress(self):
        """
        Test that checks if location creation fails if there are less than two distinct words within the
        address (IE if there isn't both a postal code and a state code separated by a space)
        """
        self.assertRaises(AssertionError,lambda: Location("beststreet12345")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113ForestStreetTX42119"))) 
    def testLocationStateCodeNonAlphabetical(self):
        """
        Test that checks if location creation fails if the statecode contains characters that aren't letters
        """
        self.assertRaises(AssertionError,lambda: Location("219 Frozen St. VI3 2238")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street 6X 42119"))) 
    def testLocationStateCodeNonAllCaps(self):
        """
        Test that checks if location creation fails if the state code contains lowercase letters
        """
        self.assertRaises(AssertionError,lambda: Location("42 Red Avenue ny 99112")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street tx 42119"))) 
    def testLocationStateCodeWrongLength(self):
        """
        Test that checks if location creation fails if the state code isn't either 2 or 3 characters long
        """
        self.assertRaises(AssertionError,lambda: Location("941 Rainbow Road Street CALI 32444")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street TXAV 42119"))) 
    def testLocationNonNumericPostalCode(self):
        """
        Test that checks if location creation fails if the postal code contains a character that isn't a number
        """
        self.assertRaises(AssertionError,lambda: Location("3 Golden Fire Ave QLD post")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street TX 4211."))) 
    def testLocationAustralianPostalCodeWrongLength(self):
        """
        Test that checks if location creation fails if the state code is australian but the postal code
        isn't 4 numbers long
        """
        self.assertRaises(AssertionError,lambda: Location("42 Silver Lining Avenue VIC 23845")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street TXA 42119"))) 
    def testLocationAmericanPostalCodeWrongLength(self):
        """
        Test that checks if location creation fails if the state code is american but the postal code
        isn't 5 letters long
        """
        self.assertRaises(AssertionError,lambda: Location("22 Green Lake Street NY 1234")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(location=Location("113 Forest Street TX 4219"))) 
    def testLocationValidAustralianPostalCode(self):
        """
        Test that checks if location creation succeeds with a valid australian location
        """
        address = "8 Clear Sky Ave SYD 3914"
        event = createMockEvent(location=Location(address))
        self.assertEqual(address,event.location.address)
    def testLocationValidAmericanPostalCode(self):
        """
        Test that checks if location creation succeeds with a valid american location
        """
        address = "113 Forest Street TX 42119"
        event = createMockEvent(location=Location(address))
        self.assertEqual(address,event.location.address)
    def testChangeLocationValid(self):
        """
        Test that checks if a location can be changed if the location address is valid
        """
        address = "ONLINE"
        mockApi = MagicMock()
        event = createMockEvent(api=mockApi,location=Location(address))
        self.assertFalse(event.location.isPhysical)
        result = event.setEventAddress("3 Clydale Av VIC 2020")
        self.assertTrue(mockApi.events.return_value.patch.called)
        self.assertTrue(result)
        self.assertEqual("3 Clydale Av VIC 2020",event.location.address)
        self.assertTrue(event.location.isPhysical)
    def testChangeLocationInvalid(self):
        """
        Test that checks if the location stays the same if an attempt is made to
        change it to an invalid address
        """
        address = "17 Wide Dale St NJ 31139"
        mockApi = MagicMock()
        event = createMockEvent(api=mockApi,location=Location(address))
        self.assertFalse(mockApi.events.return_value.patch.called)
        result = event.setEventAddress("5 Gold Street 8123 NYC")
        self.assertFalse(result)
        self.assertEqual("17 Wide Dale St NJ 31139",event.location.address)

    def test_isNotOrganizer(self):
        """
        Test that checks if the location stays the same if an attempt is made to
        change it despite the user not being the event's organizer
        """
        mock_api = Mock()
        #eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newLocation= '48 King Country Square TX 31113'
        #mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        #self.assertFalse(MyEventManager.changeEventLocation(mock_api,eventId,newLocation))
        event = Event.fromData(mock_api,self.exampleEventNotOrganiser)
        self.assertEqual(self.exampleEventNotOrganiser['location'],event.location.address)
        self.assertFalse(event.setEventAddress(newLocation))
        self.assertEqual(self.exampleEventNotOrganiser['location'],event.location.address)

    def test_newLocationIsEmpty(self):
        """
        Test that checks if the location stays the same if an attempt is made to
        change it to an empty address
        """
        mock_api = Mock()
        newLocation= ''
        event = Event.fromData(mock_api,self.exampleEvent)
        self.assertEqual(self.exampleEvent['location'],event.location.address)
        self.assertFalse(event.setEventAddress(newLocation))
        self.assertEqual(self.exampleEvent['location'],event.location.address)

class ImportEventFromAPITest(unittest.TestCase):

    def testFromData(self):
        """
        Test that checks whether the fromDate function works
        """
        data = {
            'kind': 'calendar#event', 'etag': '"3327157843918000"', 'id': '7tddvde2rgaobf7qam30r7pteg', 'status': 'confirmed', 
            'htmlLink': 'https://www.google.com/calendar/event?eid=N3RkZHZkZTJyZ2FvYmY3cWFtMzByN3B0ZWcgbWFyaW9zdXNhbnRvMTYxQG0', 
            'created': '2022-09-19T09:15:21.000Z', 'updated': '2022-09-19T09:15:22.084Z', 
            'summary': 'Party', 'location': '98 Shirley Street PIMPAMA QLD 4209', 
            'creator': {'email': 'mariosusanto161@gmail.com', 'self': True}, 
            'organizer': {'email': 'fakeemail@gmail.com', 'self': True}, 
            'start': {'dateTime': '2022-09-22T02:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
            'end': {'dateTime': '2022-09-24T12:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
            'iCalUID': '7tddvde2rgaobf7qam30r7pteg@google.com', 'sequence': 0, 
            'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'}], 
            'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 60}]}, 
            'eventType': 'default'}
        event = Event.fromData(MagicMock(),data)
        self.assertEqual('7tddvde2rgaobf7qam30r7pteg',event.id)
        self.assertEqual('Party',event.name)
        self.assertEqual('98 Shirley Street PIMPAMA QLD 4209',event.location.address)
        self.assertEqual(1,len(event.attendees)) # single attendee + organizer
        self.assertEqual("bobross@gmail.com",event.attendees[0].email)
        self.assertEqual('fakeemail@gmail.com',event.organiser.email)
        self.assertEqual('mariosusanto161@gmail.com',event.owner.email)
        self.assertEqual(2022,event.startDate.year)
        self.assertEqual(9,event.startDate.month)
        self.assertEqual(22,event.startDate.day)
        self.assertEqual(2022,event.endDate.year)
        self.assertEqual(9,event.endDate.month)
        self.assertEqual(24,event.endDate.day)
        self.assertEqual([10],event.popupNotifMinuteList)
        self.assertEqual([60],event.emailNotifMinuteList)
    def testFromDateVirtual(self):
        """
        Test that checks whether importing an online event works
        """
        data = createEventData(address="ONLINE")
        event = Event.fromData(MagicMock(),data)
        self.assertEqual("ONLINE",event.location.address)

class DeleteEventTest(unittest.TestCase):
    @patch("Classes.dt")
    def testDeleteSucceed(self,mockDT):
        """
        Test to see if a successful event deletion worked
        """
        print(mockDT)
        event = createMockEvent(startDate=Date("2015-04-10","04:00"),endDate=Date("2015-04-10","06:00"))
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,8,30)
        mockDT.datetime.side_effect = getDateTime
        print(event)
        result = event.deleteFromCalendar()
        self.assertTrue(result)
    @patch("Classes.dt")
    def testDeleteFutureEvent(self,mockDT):
        """
        Test to see if attempting to delete a future event fails
        """
        event = createMockEvent(startDate=Date("2015-04-11"),endDate=Date("2015-04-11"))
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,0,30)
        mockDT.datetime.side_effect = getDateTime
        result = event.deleteFromCalendar()
        self.assertFalse(result)

    @patch("Classes.dt")
    def testDeleteAsNonOrganiser(self,mockDT):
        """
        Test to see if attempting to delete an event as a non-organizer fails
        """
        event = createMockEvent(startDate=Date("2015-04-10","04:00"),endDate=Date("2015-04-10","06:00"),organizer=Attendee("jill123@gmail.com",False))
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,0,30)
        mockDT.datetime.side_effect = getDateTime
        result = event.deleteFromCalendar()
        self.assertFalse(result)

class CancelAndRestoreEventTest(unittest.TestCase):
    @patch("Classes.dt")
    def testCancelEventFutureEvent(self,mockDT):
        """
        Test to see if cancelling a future event as an organizer works
        """
        mockApi = MagicMock(name="calendarMock")
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,4,30)
        mockDT.datetime.side_effect = getDateTime
        event = createMockEvent(api=mockApi,startDate=Date("2015-04-10","04:30"),endDate=Date("2015-04-10","04:30"))
        result = event.cancelEvent()
        self.assertTrue(result)
        mockApi.events.return_value.patch.assert_called_once_with(calendarId='primary', eventId=event.id,body={'status' : 'cancelled'})
    @patch("Classes.dt")
    def testCancelEventPastEvent(self,mockDT):
        """
        Test to see if cancelling a past event fails
        """
        mockApi = MagicMock(name="calendarMock")
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,4,30)
        mockDT.datetime.side_effect = getDateTime
        event = createMockEvent(api=mockApi,startDate=Date("2015-04-10","04:29"),endDate=Date("2015-04-10","04:29"))
        result = event.cancelEvent()
        self.assertFalse(result)
        self.assertFalse(mockApi.events.return_value.patch.called)

    @patch("Classes.dt")
    def testRestoreEvent(self,mockDT):
        """
        Test to see if restoring an event works
        """
        mockApi = MagicMock(name="calendarMock")
        mockDT.datetime.now.return_value = dt.datetime(2015,4,10,4,30)
        mockDT.datetime.side_effect = getDateTime
        event = createMockEvent(api=mockApi,startDate=Date("2015-04-10","04:30"),endDate=Date("2015-04-10","04:30"))
        event.restoreEvent()
        mockApi.events.return_value.patch.assert_called_once_with(calendarId='primary', eventId=event.id,body={'status' : 'confirmed'})

class DateTest(unittest.TestCase):
    """
    This test suite is to test if inputted dates in YYYY-MM-DD or DD-MON-YY format are valid. 
    When viewing is False, dates within 2050 are valid. When viewing is True, dates that are within 5 years from now
    and 5 years in the past are valid.
    """
    def test_dateInYYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-MM-DD format and within 2050 is valid.
        """
        date = "2049-12-31"
        self.assertTrue(Date.isDateValid(date))

    def test_dateOver2050_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-MM-DD format and after 2050 is invalid.
        """
        date = "2051-01-01"
        self.assertFalse(Date.isDateValid(date))    

    def test_dateInDD_MON_YYFormat(self):
        """
        Test if date in DD-MOM-YY format and within 2050 is valid.
        """
        date = "01-JAN-50"
        self.assertTrue(Date.isDateValid(date))
         
    def test_yearNumeric_ButNotLengthOf2_DD_MON_YYFormat(self):
        """
        Test if date in DD-MOM-YY format, year is numeric but not length 4, is invalid.
        """
        date = "06-FEB-122"
        self.assertFalse(Date.isDateValid(date))
         
    def test_yearNumeric_ButLaterThan51_DD_MON_YYFormat(self):
        """
        Test if date in DD-MOM-YY format, year is numeric and length of 2, but is over 51 is valid, as it would be converted to 1951.
        """
        date = "06-FEB-51"
        self.assertTrue(Date.isDateValid(date))
         
    def test_yearIsNotNumeric_DD_MON_YYFormat(self):
        """
        Test if date in DD-MOM-YY format, but year is not numeric, is invalid.
        """
        date = "06-FEB-nice"
        self.assertFalse(Date.isDateValid(date))

    def test_yearIsNotNumeric_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-MM-DD format, but year is not numeric, is invalid.
        """
        date = "tttt-04-15"
        self.assertFalse(Date.isDateValid(date))
         
    def test_monthNumeric_ButLengthOf2_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-DD-MM format, but month is not of length 2, is invalid.
        """
        date = "2021-6-06"
        self.assertFalse(Date.isDateValid(date))
         
    def test_monthNumeric_ButNotWithin1and12_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-DD-MM format, but month is not within 1 and 12,  is invalid.
        """
        date = "2021-13-06"
        self.assertFalse(Date.isDateValid(date))
         
    def test_monthNotInMONFormat_DD_MON_YYFormat(self):
        """
        Test if date in DD-MON-YY format, but month is not in format of MON, is invalid
        """
        date = "06-jan-21"
        self.assertFalse(Date.isDateValid(date))
         
    def test_dayNumeric_ButLengthof2_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-MM-DD format, day is numeric but day is not of length 2, is invalid
        """
        date = "2021-11-1"
        self.assertFalse(Date.isDateValid(date))
         
    def test_dayNumeric_ButNotWithin1and31_YYYY_MM_DDFormat(self):
        """
        Test if date in YYYY-MM-DD format, day is numeric and length of 2, but day is not within 1 and 31, is invalid
        """
        date = "2021-11-32"
        self.assertFalse(Date.isDateValid(date))

    def test_dayNotNumeric(self):
        """
        Test if date in YYYY-MM-DD format, but day is not numeric, is invalid
        """
        date = "2023-10-hh"
        self.assertFalse(Date.isDateValid(date))

    def test_dateNotSeparatedWithDash(self):
        """
        Test if date is not separated with '-', is invalid
        """
        date = "2021-11:51"
        self.assertFalse(Date.isDateValid(date))

    def test_dateNotIn_YYYY_MM_DD_or_DD_MM_YYFormat(self):
        """
        Test if date is not in either YYYY-MM-DD or DD-MOn-YY format, is invalid
        """
        date = "2439-03-04-34"
        self.assertFalse(Date.isDateValid(date))

    def test_dayNumeric_ButNotLengthof2_DD_MON_YYFormat(self):
        """
        Test if date is in DD-MON-YY format, day is numeric but not of length 2, is invalid
        """
        date = "2-JAN-93"
        self.assertFalse(Date.isDateValid(date))

    def test_yearNumeric_ButNotLengthOf4_YYYY_MM_DDFormat(self):
        """
        Test if date is in YYYY-MM-DD format, year is numeric but not of length 4, is invalid
        """
        date = "95-05-15"
        self.assertFalse(Date.isDateValid(date))
    
    def test_yearInYYYY_MM_DDFormat_ButOver5YearFutureCap_viewingTrue(self):
        """
        Test if viewing is True, date is in YYYY-MM-DD format, but year is over 5 years from now, is invalid.
        """
        date = "2028-05-15"
        self.assertFalse(Date.isDateValid(date,viewing=True))
    
    def test_yearInYYYY_MM_DDFormat_ButOver5YearPastCap_viewingTrue(self):
        """
        Test if viewing is True, date is in YYYY-MM-DD format, but year is over 5 years in the past from now, is invalid.
        """
        date = "2016-05-15"
        self.assertFalse(Date.isDateValid(date,viewing=True))

    def test_yearInYYYY_MM_DDFormat_Within5YearFuturePastCap_viewingTrue(self):
        """
        Test if viewing is True, date is in YYYY-MM-DD format and is within the 5 years future and past cap. is valid.
        """
        date = "2023-05-15"
        self.assertTrue(Date.isDateValid(date,viewing=True))

    def test_yearInDD_MON_YYFormat_ButOver5YearFutureCap_viewingTrue(self):
        """
        Test if viewing is True, date is in DD-MON-YY format, but year is over 5 years from now, is invalid.
        """
        date = "15-JUN-28"
        self.assertFalse(Date.isDateValid(date,viewing=True))
    
    def test_yearInDD_MON_YYFormat_ButOver5YearPastCap_viewingTrue(self):
        """
        Test if viewing is True, date is in DD-MON-YY format, but year is over 5 years in the past from now, is invalid.
        """
        date = "15-MAY-16"
        self.assertFalse(Date.isDateValid(date,viewing=True))

    def test_yearInDD_MON_YYFormat_Within5YearFuturePastCap_viewingTrue(self):
        """
        Test if viewing is True, date is in DD-MON-YY format and is within the 5 years future and past cap. is valid.
        """
        date = "15-MAY-23"
        self.assertTrue(Date.isDateValid(date,viewing=True))
    
    def test_emptyDate(self):
        """
        Test if empty date is invalid.
        """
        date = ""
        self.assertFalse(Date.isDateValid(date))

class TimeTest(unittest.TestCase):
    """
    This test suites tests the validty of the input time using line coverage,branch coverage and condition coverage.
    """
    def test_validTime(self):
        """
        Tests if HH:MM format time is valid.
        """
        time = "23:59"
        self.assertTrue(Date.isTimeValid(time))
         
    def test_hourNotOfLength2_notInHHFormat(self):
        """
        Tests if hour which is not of length 2 and not in HH format is invalid.
        """
        time = "6:00"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_hourNotWithin_0_and_23(self):
        """
        Tests if hour which is not between 0 and 23 is invalid.
        """
        time = "24:00"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_hourNotNumeric(self):
        """
        Tests if non numeric hour is invalid.
        """
        time = "gg:00"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_minuteNotOfLength2_notInMMFormat(self):
        """
        Tests if minute which is not of length 2 and not in MM format is invalid.
        """
        time = "06:5"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_minuteNotWithin_0_and_59(self):
        """
        Tests if minute which is not between 0 and 59 is invalid.
        """
        time = "06:60"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_minuteNotNumeric(self):
        """
        Tests if non numeric minute is invalid.
        """
        time = "16:hi"
        self.assertFalse(Date.isTimeValid(time))
         
    def test_timeNotSeparatedWithColon(self):
        """
        Test if time is invalid when HH and MM is not separated with colon.
        """
        time = "23-31"
        self.assertFalse(Date.isTimeValid(time))

    def test_emptyTime(self):
        """
        Test if time is invalid when time is empty
        """
        time = ""
        self.assertFalse(Date.isTimeValid(time))
         
class EmailTest(unittest.TestCase):
    """
    This test suite tests the validity of input email comprehensively using line coverage, branch coverage and condition coverage.
    """
    def test_validEmailFormat(self):
        """
        Test if email is valid where email is in valid format.
        """
        email = "georgetan615@gmail.com"
        self.assertTrue(Attendee.isEmailValid(email))
         
    def test_invalidEmailMissingSymbolAt(self):
        """
        Test if email is invalid where email is missing a @
        """
        email = "georgetangmail.com"
        self.assertFalse(Attendee.isEmailValid(email))
         
    def test_invalidEmailDoesNotEndWithDomain(self):
        """
        Test if email is invalid where email does not end with email domain.
        """
        email = "georgetan615@"
        self.assertFalse(Attendee.isEmailValid(email))
         
    def test_invalidEmailMissingEmailInitials(self):
        """
        Test if email is invalid where email initials are missing.
        """
        email = "@gmail.com"
        self.assertFalse(Attendee.isEmailValid(email))

    def test_emptyEmail(self):
        """
        Test if email is invalid where email is empty.
        """
        email = ""
        self.assertFalse(Attendee.isEmailValid(email))

class NotifTest(unittest.TestCase):
    @patch("MyEventManager.dt")
    def testCheckNotifs(self,mockDT):
        """
        Test to see if filtering for events with an incoming notification works correctly
        """
        eventList = []
        eventList.append(createMockEvent(name="event1",startDate=Date("2008-01-01","07:19"),endDate=Date("2008-01-01","07:49")))
        eventList.append(createMockEvent(name="event2",startDate=Date("2008-01-01","07:20"),endDate=Date("2008-01-01","07:50")))
        eventList.append(createMockEvent(name="event3",startDate=Date("2008-01-01","07:50"),endDate=Date("2008-01-01","08:20")))
        for event in eventList:
            event.addPopupReminder(10)
        mockDT.datetime.now.return_value = dt.datetime(2008,1,1,7,30)
        mockDT.timedelta.side_effect = lambda minutes: dt.timedelta(minutes=minutes)
        notifiableEventList = MyEventManager.checkForEventNotifications(eventList)
        self.assertEqual(1,len(notifiableEventList))
        self.assertEqual(notifiableEventList[0].name,"event2")
    
    def testEmailNotif(self):
        """
        Test to see if adding multiple email notifications works
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.emailNotifMinuteList)
        event.addEmailReminder(60)
        event.addEmailReminder(30)
        event.addEmailReminder(5)
        self.assertEqual([60,30,5],event.emailNotifMinuteList)
        api.events.return_value.patch.return_value.execute.assert_called
    def testEmailNotifTooShort(self):
        """
        Test to see if adding an email notification with a negative length fails
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.emailNotifMinuteList)
        event.addEmailReminder(-1)
        self.assertEqual([],event.emailNotifMinuteList)
        self.assertFalse(api.events.return_value.patch.return_value.execute.called)
    def testEmailNotifTooLong(self):
        """
        Test to see if adding an email notification with too long of a length fails
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.emailNotifMinuteList)
        event.addEmailReminder(40321)
        self.assertEqual([],event.emailNotifMinuteList)
        self.assertFalse(api.events.return_value.patch.return_value.execute.called)
    def testPopupNotif(self):
        """
        Test to see if adding multiple popup notifications works
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.popupNotifMinuteList)
        event.addPopupReminder(60)
        event.addPopupReminder(30)
        event.addPopupReminder(5)
        self.assertEqual([60,30,5],event.popupNotifMinuteList)
        api.events.return_value.patch.return_value.execute.assert_called
    def testPopupNotifTooShort(self):
        """
        Test to see if adding a popup notification with a negative length fails
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.popupNotifMinuteList)
        event.addPopupReminder(-1)
        self.assertEqual([],event.popupNotifMinuteList)
        self.assertFalse(api.events.return_value.patch.return_value.execute.called)
    def testPopupNotifTooLong(self):
        """
        Test to see if adding a popup notification with too long of a length fails
        """
        api = MagicMock()
        event = createMockEvent(api=api)
        self.assertEqual([],event.popupNotifMinuteList)
        event.addPopupReminder(40321)
        self.assertEqual([],event.popupNotifMinuteList)
        self.assertFalse(api.events.return_value.patch.return_value.execute.called)

class StartDateTimeIsBeforeEndDateTimeTest(unittest.TestCase):
    """
    This test suite tests if the provided start date and start time are before end date and end time.
    """
    def test_startEndSameYearMonthDayHour_StartMinuteBeforeEndMinute(self):
        """
        Tests when start date and time are of the same year,month,day,hour as end date and time,
        and start time's minutes is before end time's minutes.
    
        """ 
        startDate = "2022-11-12"
        startTime = "11:12"
        endDate = "2022-11-12"
        endTime = "11:12"
        self.assertTrue(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYearMonthDayHour_StartMinuteAfterEndMinute(self):
        """
        Tests when start date and time are of the same year,month,day,hour as end date and time,
        but start time's minutes is after end time's minutes.
        """ 
        startDate = "2022-11-12"
        startTime = "11:13"
        endDate = "2022-11-12"
        endTime = "11:12"
        self.assertFalse(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYearMonthDay_StartHourBeforeEndHour(self):
        """
        Tests when start date and time are of the same year,month,day as end date and time,
        but start time's hour is before end time's hour.
        """ 
        startDate = "2022-11-12"
        startTime = "11:13"
        endDate = "2022-11-12"
        endTime = "12:12"
        self.assertTrue(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYearMonthDay_StartHourAfterEndHour(self):
        """
        Tests when start date and time are of the same year,month,day as end date and time,
        but start time's hour is after end time's hour.
        """ 
        startDate = "2022-11-12"
        startTime = "13:13"
        endDate = "2022-11-12"
        endTime = "12:12"
        self.assertFalse(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYearMonth_StartDayBeforeEndDay(self):
        """
        Tests when start date and time are of the same year,month as end date and time,
        but start date's day is before end date's day.
        """ 
        startDate = "2022-11-13"
        startTime = "05:12"
        endDate = "2022-11-14"
        endTime = "08:32"
        self.assertTrue(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYearMonth_StartDayAfterEndDay(self):
        """
        Tests when start date and time are of the same year,month as end date and time,
        but start date's day is after end date's day.
        """ 
        startDate = "2022-11-15"
        startTime = "05:12"
        endDate = "2022-11-14"
        endTime = "08:32"
        self.assertFalse(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYear_StartMonthBeforeEndMonth(self):
        """
        Tests when start date and time are of the same year as end date and time,
        but start date's month is before end date's month.
        """ 
        startDate = "2022-11-13"
        startTime = "05:12"
        endDate = "2022-12-14"
        endTime = "08:32"
        self.assertTrue(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startEndSameYear_StartMonthAfterEndMonth(self):
        """
        Tests when start date and time are of the same year as end date and time,
        but start date's month is after end date's month.
        """ 
        startDate = "2022-11-15"
        startTime = "05:12"
        endDate = "2022-10-14"
        endTime = "08:32"
        self.assertFalse(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
    def test_startyearBeforeEndYear(self):
        """
        Tests when start date's year is before end date's year.
        """ 
        startDate = "2022-11-13"
        startTime = "05:12"
        endDate = "2023-11-14"
        endTime = "08:32"
        self.assertTrue(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))

    def test_startyearAfterEndYear(self):
        """
        Tests when start date's year is after end date's year.
        """ 
        startDate = "2022-11-13"
        startTime = "05:12"
        endDate = "2021-11-14"
        endTime = "08:32"
        self.assertFalse(Date.isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime))
         
class ChangeEventDateTest(unittest.TestCase):
    def setUp(self): 
        self.exampleReturnedEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self':True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleUpdatedEvent = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2025-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
    
    def test_userNotOrganiser(self):
        """
        Test to see if attempting to change the date as a non-organizer fails
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        startDate = '2025-09-19'
        startTime = '23:11'
        endDate = '2034-09-24'
        endTime = '05:14'
        
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertEqual(False,MyEventManager.changeEventDate(mock_api,eventId,startDate,startTime,endDate,endTime))

    def test_invalidStartDateStartTime(self):
        """
        Test to see if attempting to change the start date to an invalid date fails
        """
        mock_api = Mock()
        eventId = "a304hihaikc6khdlpbbb2prnlk"
        startDate = "170-09-19"
        startTime = "45:76"
        endDate = "2034-09-24"
        endTime = "23:42"
        
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.changeEventDate(mock_api,eventId,startDate,startTime,endDate,endTime))

    def test_invalidEndDateEndTime(self):
        """
        Test to see if attempting to change the end date to an invalid date fails
        """
        mock_api = Mock()
        eventId = "a304hihaikc6khdlpbbb2prnlk"
        startDate = "2021-11-11"
        startTime = "07:59"
        endDate = "3123-31-43"
        endTime = "123:1234"
        
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.changeEventDate(mock_api,eventId,startDate,startTime,endDate,endTime))

    def test_startDateTimeNotBeforeEndDateTime(self):
        """
        Test to see if changing event date fails if the start date occurred after the end date
        """
        mock_api = Mock()
        eventId = "a304hihaikc6khdlpbbb2prnlk"
        startDate = "2021-12-11"
        startTime = "07:59"
        endDate = "2021-11-11"
        endTime = "07:59"
        
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.changeEventDate(mock_api,eventId,startDate,startTime,endDate,endTime))
    
    def test_changeEventDate(self):
        """
        Test to see if changing event date with correct values as an organizer works
        """
        mock_api = Mock()
        eventId = "a304hihaikc6khdlpbbb2prnlk"
        startDate = '2025-09-19'
        startTime = '08:00'
        endDate = '2034-09-24'
        endTime = '08:00'
        
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleUpdatedEvent

        updatedEvent = MyEventManager.changeEventDate(mock_api,eventId,startDate,startTime,endDate,endTime)
        self.assertEqual(updatedEvent['start']['dateTime'][:10],startDate)
        self.assertEqual(updatedEvent['end']['dateTime'][:10],endDate)
        self.assertEqual(updatedEvent['start']['dateTime'][11:16],startTime)
        self.assertEqual(updatedEvent['end']['dateTime'][11:16],endTime)

class ChangeOrganiserTest(unittest.TestCase):
    """
    This test suite tests if the change organiser process is successful depending on
    if the current user is an organiser and if the input email is valid.
    """
    def setUp(self): 
        self.exampleReturnedEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleUpdatedOrganiserEvent = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2025-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}

    def test_changeOrganiser_whenUserIsNotOrganizer(self):
        """
        Tests if the change of organiser is successful when the user is not an organiser.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'

        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertFalse(MyEventManager.changeOrganiser(mock_api,eventId,'georgetan615@gmail.com'))
    
    def test_changeOrganiser_withInvalidNewOrganiserEmail(self):
        """
        Tests if the change of organiser is successful when the input new organiser email is invalid.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'

        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.changeOrganiser(mock_api,eventId,"georgetan.com"))


    def test_changeOrganiser_whenUserIsOrganiser_ValidNewOrganiserEmail(self):
        """
        Tests if the change of organiser is successful when the user is an organiser and the input email is valid.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'

        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        mock_api.events.return_value.move.return_value.execute.return_value = self.exampleUpdatedOrganiserEvent
        self.assertTrue(MyEventManager.changeOrganiser(mock_api,eventId,"georgetan615@gmail.com"))

class RemoveAttendeeTest(unittest.TestCase):
    """
    This test suite tests if the remove attendee process is successful depending if the
    user is an organiser, the input email is of valid format and the email user is an attendee
    in the event specified by the eventId.
    """
    def setUp(self): 
        self.exampleReturnedEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleRemovedAttendeeEvent = {'attendees': [],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
    
    def test_userIsNotOrganizer(self):
        """
        Test if the remove attendee process is unsuccessful when user is not organiser.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertFalse(MyEventManager.removeAttendee(mock_api,eventId,'georgetan615@gmail.com'))
    
    def test_invalidEmailFormat_forToBeRemovedAttendeeEmail(self):
        """
        Test if the remove attendee process is unsuccessful when provided email is invalid.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'

        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.removeAttendee(mock_api,eventId,"georgetan@"))

    def test_removeAttendee_whereEmailUserIsNotAttendee(self):
        """
        Test if the remove attendee process is unsuccessful when the email user is not in the event specified by the eventId.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.removeAttendee(mock_api,eventId,'georgetan615@gmail.com'))

    def test_removeAttendee_userIsOrganiser_ValidEmail_EmailUserIsAttendee(self):
        """
        Test if the remove attendee process is successful when user is organiser, the email is valid
        and the email user is an attendee in the event.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        nbrOfInitialAttendees = len(self.exampleReturnedEvent['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleRemovedAttendeeEvent
        self.assertEqual(nbrOfInitialAttendees-1,len(MyEventManager.removeAttendee(mock_api,eventId,'georgetan.business@gmail.com')))

class AddAttendeeTest(unittest.TestCase):
    """
    This test suite tests if the add attendee process is successful depending if the
    user is an organiser, the input email is of valid format and the email user is
    not already an attendee in the event specified by the eventId.
    """
    def setUp(self): 
        self.exampleReturnedEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleAttendeeAlreadyExistEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleAddedAttendeeEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'},
                                                    {'displayName': 'George Tan JS',
                                                    'email': 'georgetanjuansheng@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleMaxedAttendeeEvent = {'attendees': [{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},
                                                        {'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},{'displayName': 'George Tan2', 'email': 'georgetan.business@gmail.com','responseStatus': 'needsAction'},],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}

    def test_userIsNotOrganizer(self):
        """
        Tests if the adding of attendee is unsuccessful when user is not an organiser.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertFalse(MyEventManager.addAttendee(mock_api,eventId,'georgetanjuansheng@gmail.com'))
    
    def test_invalidEmailFormat_forToBeAddedAttendeeEmail(self):
        """
        Tests if the adding of attendee is unsuccessful when the input email is of invalid format.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'

        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        self.assertFalse(MyEventManager.addAttendee(mock_api,eventId,""))

    def test_addAttendee_WhenNumberOfAttendeeMaxed(self):
        """
        Tests if the adding of attendee is unsuccessful when the number of attendees in the event has already reached
        maximum capacity, which is 20 in our case.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleMaxedAttendeeEvent
        self.assertFalse(MyEventManager.addAttendee(mock_api,eventId,'georgetanjuansheng@gmail.com'))

    def test_addAttendee_WhenAttendeeAlreadyExists(self):
        """
        Tests if the adding of attendee is unsuccessful when that email user is already an attendee in that event
        specified by the eventId.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleAttendeeAlreadyExistEvent
        self.assertFalse(MyEventManager.addAttendee(mock_api,eventId,'georgetan.business@gmail.com'))

    def test_addAttendee_WhenUserIsOrganiser_InputEmailValidFormat_EmailUserIsNotAlreadyAnAttendee(self):
        """
        Tests if the adding of attendee is successful when user is organiser, input email is of valid format
        and that email user is not already an attendee in the event.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleReturnedEvent
        nbrOfInitialAttendees = len(self.exampleReturnedEvent['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleAddedAttendeeEvent
        self.assertEqual(nbrOfInitialAttendees+1,len(MyEventManager.addAttendee(mock_api,eventId,'georgetan.business@gmail.com')))

class EventCreationAttendeeTest(unittest.TestCase):

    def testAttendeesOffPoint(self):
        """
        Test to see if creating an event with too many attendees fails
        """
        attendees = []
        for _ in range(21):
            attendees.append(Attendee("bobross@gmail.com")) 
        self.assertRaises(AssertionError,lambda: createMockEvent(attendees=attendees)) 

    def testAttendeesOnPoint(self):
        """
        Test to see if creating an event with the maximum attendees succeeds
        """
        attendees = []
        for _ in range(20):
            attendees.append(Attendee("bobross@gmail.com")) 
        event = createMockEvent(attendees=attendees)
        self.assertEqual(len(event.attendees),20)

class ImportEventFromJSONTest(unittest.TestCase):
    """
    This test suite tests if users are able to import events when users
    provide a file with the correct event's details in json syntax.
    """
    def test_importEvent_FromNonExistingFilePath_FileNotFound(self):
        """
        Tests if import event was unsuccessful due to specifying a file that does not exist.
        """
        mock_api = Mock()
        file = "testJsonFiles/myFile.json"
        self.assertEqual("File not found",MyEventManager.importEventFromJSON(mock_api,file))

    def test_importEvent_FromFileThatIsNotInJSONSyntax_JSONDecodeError(self):
        """
        Tests if import event was unsuccessful due to specifying a file that does not have proper JSON syntax.
        """
        mock_api = Mock()
        file = "testJsonFiles/invalidJSONFormat.json"
        self.assertEqual("Incorrect JSON file format",MyEventManager.importEventFromJSON(mock_api,file))

    def test_importEvent_FromFileThatDoesNotHaveCorrectFieldsForEvent_HttpError(self):
        """
        Tests if import event was unsuccessful due to specifying a file that does not have correct fields for event creation.
        """
        mock_api = Mock()
        mockReason = Mock()
        mockReason.reason.return_value = "Invalid format"
        mock_api.events.return_value.insert.return_value.execute.side_effect = HttpError(mockReason,bytes(1))
        file = "testJsonFiles/validEvent.json"
        self.assertEqual("Incorrect format for creation of event",MyEventManager.importEventFromJSON(mock_api,file))

    def test_importEvent_FromExistingFileThatHasCorrectFieldsInJSONSyntax_Successful(self):
        """
        Tests if import event was successful when we specify an existing file that has the correct fields
        for event creation and is in JSON syntax. 
        """
        importedEvent = {'attendees': [{'displayName': 'George Tan2',
                                        'email': 'georgetan.business@gmail.com',
                                        'responseStatus': 'needsAction'}],
                        'created': '2022-09-22T18:52:11.000Z',
                        'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                        'end': {'dateTime': '2022-09-24T10:25:00+08:00',
                                'timeZone': 'Asia/Singapore'},
                        'etag': '"3327745463532000"',
                        'eventType': 'default',
                        'htmlLink': 'https://www.google.com/calendar/event?eid=M3Z2M2g5MTRnMmpkdjNmYWN0bjRhazYzaG8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                        'iCalUID': '3vv3h914g2jdv3factn4ak63ho@google.com',
                        'id': '3vv3h914g2jdv3factn4ak63ho',
                        'kind': 'calendar#event',
                        'location': 'Somewhere',
                        'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                        'reminders': {'useDefault': True},
                        'sequence': 0,
                        'start': {'dateTime': '2022-09-23T06:00:00+08:00',
                                    'timeZone': 'Asia/Singapore'},
                        'status': 'confirmed',
                        'summary': 'Networking Session',
                        'updated': '2022-09-22T18:52:11.766Z'}
        mock_api = Mock()
        file = "testJsonFiles/validEvent.json"
        mock_api.events.return_value.insert.return_value.execute.return_value = importedEvent
        self.assertTrue(MyEventManager.importEventFromJSON(mock_api,file))

class ExportEventToJSONTest (unittest.TestCase):
    """
    This test suite tests if event can be successfully exported when user 
    does not provide any export location (file path) or when user provides an existing
    export location.
    
    """
    def setUp(self):
        self.exampleExportEvent = {'attendees': [{'displayName': 'George Tan2',
                                'email': 'georgetan.business@gmail.com',
                                'responseStatus': 'needsAction'}],
                'created': '2022-09-22T18:52:11.000Z',
                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                'end': {'dateTime': '2022-09-24T10:25:00+08:00',
                        'timeZone': 'Asia/Singapore'},
                'etag': '"3327745463532000"',
                'eventType': 'default',
                'htmlLink': 'https://www.google.com/calendar/event?eid=M3Z2M2g5MTRnMmpkdjNmYWN0bjRhazYzaG8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                'iCalUID': '3vv3h914g2jdv3factn4ak63ho@google.com',
                'id': '3vv3h914g2jdv3factn4ak63ho',
                'kind': 'calendar#event',
                'location': 'Somewhere',
                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                'reminders': {'useDefault': True},
                'sequence': 0,
                'start': {'dateTime': '2022-09-23T06:00:00+08:00',
                            'timeZone': 'Asia/Singapore'},
                'status': 'confirmed',
                'summary': 'Networking Session',
                'updated': '2022-09-22T18:52:11.766Z'}

    def test_exportEventToCurrentDirectory_FilePathNotProvided(self):
        """
        Tests if event is exported successfully to current directory when
        file path is not provided.
        """
        mock_api = Mock()
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleExportEvent
        eventId = "3vv3h914g2jdv3factn4ak63ho"
        path = MyEventManager.exportEventToJSON(mock_api,eventId)
        self.assertTrue(os.path.exists(path))
        os.remove('Networking_Session.json')
    
    def test_exportEventToSpecifiedDirectory(self):
        """
        Tests if event is exported successfully to specified directory when
        valid file path is provided.
        """
        mock_api = Mock()
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleExportEvent
        eventId = "3vv3h914g2jdv3factn4ak63ho"
        os.mkdir("testExport")
        path = MyEventManager.exportEventToJSON(mock_api,eventId,"testExport")
        self.assertTrue(os.path.exists(path))
        shutil.rmtree("testExport") # Remove file once test case finishes

    def test_exportEvent_whereSpecifiedDirectoryDoesNotExist_FileNotFoundError(self):
        """
        Tests if event is exported unsuccessfully when file path provided does not exist.
        """
        mock_api = Mock()
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleExportEvent
        eventId = "3vv3h914g2jdv3factn4ak63ho"
        self.assertFalse(MyEventManager.exportEventToJSON(mock_api,eventId,"NonExistentDirectory"))

class ChangeEventTitleTest(unittest.TestCase):
    """
    This test suite tests if an event's title can be updated to a new title when the 
    user is organiser and the input new title is not empty.
    """
    def setUp(self):
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 

                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleNewTitleEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': 'Somewhere',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'New title',
                                    'updated': '2022-09-20T04:30:29.245Z'}
    
    def test_test_changeEventTitle_userIsNotOrganizer(self):
        """
        Tests if event's title is not changed successfully when user is not organiser.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newTitle= 'Hello World'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertFalse(MyEventManager.changeEventTitle(mock_api,eventId,newTitle))

    def test_changeEventTitle_newTitleIsEmpty(self):
        """
        Tests if event's title is not changed successfully when the new title specified is empty.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newTitle= ''
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEvent
        self.assertFalse(MyEventManager.changeEventTitle(mock_api,eventId,newTitle))
    def test_changeEventTitle_userIsOrganiser_newTitleIsNotEmpty(self):
        """
        Tests if event's title is changed successfully when user is the organiser
        and the new title is not empty.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newTitle= 'New title'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEvent
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleNewTitleEvent
        self.assertEqual(newTitle,MyEventManager.changeEventTitle(mock_api,eventId,newTitle))

class ChangeEventDescriptionTest(unittest.TestCase):
    """
    This test suite tests if an event's description can be updated to a new description when the 
    user is organiser and the input new description is not empty.
    """
    def setUp(self):
        self.exampleEventNotOrganiser = {'attendees': [{'displayName': 'George Tan2', 

                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2034-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '4 Green Rd VIC 33139',
                                    'organizer': {'email': 'georgetan615@gmail.com'},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2020-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'description':'Old description',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '4 Green Rd VIC 33139',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'description':'Old description',
                                    'summary': 'Networking Session',
                                    'updated': '2022-09-20T04:30:29.245Z'}
        self.exampleNewDescriptionEvent = {'attendees': [{'displayName': 'George Tan2',
                                                    'email': 'georgetan.business@gmail.com',
                                                    'responseStatus': 'needsAction'}],
                                    'created': '2022-09-19T09:26:44.000Z',
                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'end': {'dateTime': '2022-09-24T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                    'etag': '"3327296458490000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=YTMwNGhpaGFpa2M2a2hkbHBiYmIycHJubGsgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': 'a304hihaikc6khdlpbbb2prnlk@google.com',
                                    'id': 'a304hihaikc6khdlpbbb2prnlk',
                                    'kind': 'calendar#event',
                                    'location': '4 Green Rd VIC 33139',
                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': True},
                                    'sequence': 2,
                                    'start': {'dateTime': '2022-09-19T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                    'status': 'confirmed',
                                    'summary': 'Networking Session',
                                    'description': 'This is a new event',
                                    'updated': '2022-09-20T04:30:29.245Z'}
    
    def test_changeEventDescription_userIsNotOrganizer(self):
        """
        Tests if event's description is not changed successfully when user is not organiser.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newDescription= 'This is a new event'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEventNotOrganiser
        self.assertFalse(MyEventManager.changeEventDescription(mock_api,eventId,newDescription))

    def test_changeEventDescription_newDescriptionIsEmpty(self):
        """
        Tests if event's description is not changed successfully when new description provided is empty.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newDescription= ''
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEvent
        self.assertFalse(MyEventManager.changeEventDescription(mock_api,eventId,newDescription))

    def test_changeEventDescription_userIsOrganiser_newDescriptionIsNotEmpty(self):
        """
        Tests if event's description is changed successfully when user is the organiser
        and the new description is not empty.
        """
        mock_api = Mock()
        eventId = 'a304hihaikc6khdlpbbb2prnlk'
        newDescription= 'This is a new event'
        mock_api.events.return_value.get.return_value.execute.return_value = self.exampleEvent
        mock_api.events.return_value.patch.return_value.execute.return_value = self.exampleNewDescriptionEvent
        self.assertEqual(newDescription,MyEventManager.changeEventDescription(mock_api,eventId,newDescription))

class AcceptEventInviteTest(unittest.TestCase):
    def setUp(self):
        """
        The setUp function is called before each test function. It is used to set up the objects that are needed for testing.
        """
        self.sampleEventAttendee =  {'attendees': [{'email': 'blee0047@student.monash.edu',
                                    'responseStatus': 'needsAction',
                                    'self': True},
                                    {'email': 'baoqii13@gmail.com',
                                    'organizer': True,
                                    'responseStatus': 'accepted'}],
                                    'created': '2022-09-25T07:39:38.000Z',
                                    'creator': {'email': 'baoqii13@gmail.com'},
                                    'end': {'date': '2022-10-24'},
                                    'etag': '"3328183169030000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=NjByMDQ2ZXBvaWVtMHJrYWd0YzF1Z2FxMzIgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': '60r046epoiem0rkagtc1ugaq32@google.com',
                                    'id': '60r046epoiem0rkagtc1ugaq32',
                                    'kind': 'calendar#event',
                                    'organizer': {'email': 'baoqii13@gmail.com'},
                                    'reminders': {'useDefault': False},
                                    'sequence': 1,
                                    'start': {'date': '2022-10-23'},
                                    'status': 'confirmed',
                                    'summary': 'Test event for attendee',
                                    'transparency': 'transparent',
                                    'updated': '2022-09-25T07:39:44.515Z'}
        self.sampleEventAttendeeAccepted = {'attendees': [{'email': 'blee0047@student.monash.edu',
                                            'responseStatus': 'accepted',
                                            'self': True},
                                            {'email': 'baoqii13@gmail.com',
                                            'organizer': True,
                                            'responseStatus': 'accepted'}],
                                            'created': '2022-09-25T07:39:38.000Z',
                                            'creator': {'email': 'baoqii13@gmail.com'},
                                            'end': {'date': '2022-10-24'},
                                            'etag': '"3328191850878000"',
                                            'eventType': 'default',
                                            'htmlLink': 'https://www.google.com/calendar/event?eid=NjByMDQ2ZXBvaWVtMHJrYWd0YzF1Z2FxMzIgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                            'iCalUID': '60r046epoiem0rkagtc1ugaq32@google.com',
                                            'id': '60r046epoiem0rkagtc1ugaq32',
                                            'kind': 'calendar#event',
                                            'organizer': {'email': 'baoqii13@gmail.com'},
                                            'reminders': {'useDefault': False},
                                            'sequence': 1,
                                            'start': {'date': '2022-10-23'},
                                            'status': 'confirmed',
                                            'summary': 'Test event for attendee',
                                            'transparency': 'transparent',
                                            'updated': '2022-09-25T08:52:05.439Z'}
        self.sampleEventOrganizerNotAttending = {'created': '2022-09-25T08:13:11.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2022-09-29T19:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                                'etag': '"3328187183444000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=cHNnOXR0YjRiMmxmOGJzNTlhbXA2ZGw1NzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'psg9ttb4b2lf8bs59amp6dl570@google.com',
                                                'id': 'psg9ttb4b2lf8bs59amp6dl570',
                                                'kind': 'calendar#event',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'popup', 'minutes': 0}],
                                                            'useDefault': False},
                                                'sequence': 0,
                                                'start': {'dateTime': '2022-09-28T19:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'deded',
                                                'updated': '2022-09-25T08:13:11.853Z'}

    def test_isNotAttendee(self):
        """
        Tests whether the acceptEventInvite function in MyEventManager.py will return False if an event is not being attended by the user

        :return: False because the event organizer is not attending the event
        """
        mock_api = Mock()
        eventId = 'psg9ttb4b2lf8bs59amp6dl570'
        mock_api.events.return_value.get.return_value.execute.return_value = self.sampleEventOrganizerNotAttending
        self.assertFalse(MyEventManager.acceptEventInvite(mock_api,eventId))

    def test_acceptEventInvite(self):
        """
        Tests whether the acceptEventInvite function in MyEventManager.py will return the updatedEvent with responseStatus set to 'accepted'
        """
        mock_api = Mock()
        eventId = '60r046epoiem0rkagtc1ugaq32'
        mock_api.events.return_value.get.return_value.execute.return_value = self.sampleEventAttendee
        mock_api.events.return_value.patch.return_value.execute.return_value = self.sampleEventAttendeeAccepted
        self.assertEqual(MyEventManager.acceptEventInvite(mock_api,eventId), self.sampleEventAttendeeAccepted)

class RejectEventInviteTest(unittest.TestCase):
    def setUp(self):
        """
        The setUp function is called before each tests function. It is used to set up the objects that are needed for testing.
        """
        self.sampleEventAttendee =  {'attendees': [{'email': 'blee0047@student.monash.edu',
                                    'responseStatus': 'needsAction',
                                    'self': True},
                                    {'email': 'baoqii13@gmail.com',
                                    'organizer': True,
                                    'responseStatus': 'accepted'}],
                                    'created': '2022-09-25T07:39:38.000Z',
                                    'creator': {'email': 'baoqii13@gmail.com'},
                                    'end': {'date': '2022-10-24'},
                                    'etag': '"3328183169030000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=NjByMDQ2ZXBvaWVtMHJrYWd0YzF1Z2FxMzIgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': '60r046epoiem0rkagtc1ugaq32@google.com',
                                    'id': '60r046epoiem0rkagtc1ugaq32',
                                    'kind': 'calendar#event',
                                    'organizer': {'email': 'baoqii13@gmail.com'},
                                    'reminders': {'useDefault': False},
                                    'sequence': 1,
                                    'start': {'date': '2022-10-23'},
                                    'status': 'confirmed',
                                    'summary': 'Test event for attendee',
                                    'transparency': 'transparent',
                                    'updated': '2022-09-25T07:39:44.515Z'}
        self.sampleEventAttendeeRejected =  {'attendees': [{'email': 'blee0047@student.monash.edu',
                                                            'responseStatus': 'declined',
                                                            'self': True},
                                                            {'email': 'baoqii13@gmail.com',
                                                            'organizer': True,
                                                            'responseStatus': 'accepted'}],
                                                            'created': '2022-09-25T07:39:38.000Z',
                                                            'creator': {'email': 'baoqii13@gmail.com'},
                                                            'end': {'date': '2022-10-24'},
                                                            'etag': '"3328197966284000"',
                                                            'eventType': 'default',
                                                            'htmlLink': 'https://www.google.com/calendar/event?eid=NjByMDQ2ZXBvaWVtMHJrYWd0YzF1Z2FxMzIgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                                            'iCalUID': '60r046epoiem0rkagtc1ugaq32@google.com',
                                                            'id': '60r046epoiem0rkagtc1ugaq32',
                                                            'kind': 'calendar#event',
                                                            'organizer': {'email': 'baoqii13@gmail.com'},
                                                            'reminders': {'useDefault': False},
                                                            'sequence': 1,
                                                            'start': {'date': '2022-10-23'},
                                                            'status': 'confirmed',
                                                            'summary': 'Test event for attendee',
                                                            'transparency': 'transparent',
                                                            'updated': '2022-09-25T09:43:03.142Z'}
        self.sampleEventOrganizerNotAttending = {'created': '2022-09-25T08:13:11.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2022-09-29T19:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                                'etag': '"3328187183444000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=cHNnOXR0YjRiMmxmOGJzNTlhbXA2ZGw1NzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'psg9ttb4b2lf8bs59amp6dl570@google.com',
                                                'id': 'psg9ttb4b2lf8bs59amp6dl570',
                                                'kind': 'calendar#event',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'popup', 'minutes': 0}],
                                                            'useDefault': False},
                                                'sequence': 0,
                                                'start': {'dateTime': '2022-09-28T19:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'deded',
                                                'updated': '2022-09-25T08:13:11.853Z'}

    def test_isNotAttendee(self):
        """
        Tests whether the rejectEventInvite function in MyEventManager.py will return False if an event is not being attended by the user
        
        :return: False because the event organizer is not attending the event
        """
        mock_api = Mock()
        eventId = 'psg9ttb4b2lf8bs59amp6dl570'
        mock_api.events.return_value.get.return_value.execute.return_value = self.sampleEventOrganizerNotAttending
        self.assertFalse(MyEventManager.rejectEventInvite(mock_api,eventId))

    def test_rejectEventInvite(self):
        """
        Tests whether the rejectEventInvite function in MyEventManager.py will return the updatedEvent with responseStatus set to 'declined'
        """
        mock_api = Mock()
        eventId = '60r046epoiem0rkagtc1ugaq32'
        mock_api.events.return_value.get.return_value.execute.return_value = self.sampleEventAttendee
        mock_api.events.return_value.patch.return_value.execute.return_value = self.sampleEventAttendeeRejected
        self.assertEqual(MyEventManager.rejectEventInvite(mock_api,eventId), self.sampleEventAttendeeRejected)

class TestGetNavigatedEvents(unittest.TestCase):
    """
    This test suite tests if events on a certain year, or certain year's month,
    or certain year's month's day, can be obtained successfully.
    """
    def setUp(self):
        self.eventsIn2023 = [{'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                            {'email': 'gtan0021@student.monash.edu',
                                            'organizer': True,
                                            'responseStatus': 'needsAction',
                                            'self': True}],
                            'created': '2022-09-23T19:31:27.000Z',
                            'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'end': {'dateTime': '2023-06-16T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                            'etag': '"3327998852039000"',
                            'eventType': 'default',
                            'htmlLink': 'https://www.google.com/calendar/event?eid=ZmlkNWJ1ODNuY2o4OTRxNTRzZnRiaDI1bG8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                            'iCalUID': 'fid5bu83ncj894q54sftbh25lo@google.com',
                            'id': 'fid5bu83ncj894q54sftbh25lo',
                            'kind': 'calendar#event',
                            'location': '98 Shirley Street PIMPAMA QLD 4209',
                            'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                        {'method': 'popup', 'minutes': 10}],
                                            'useDefault': False},
                            'sequence': 1,
                            'start': {'dateTime': '2023-06-15T08:00:00+08:00',
                                        'timeZone': 'Asia/Singapore'},
                            'status': 'confirmed',
                            'summary': 'Party 1',
                            'updated': '2022-09-24T16:36:04.625Z'},
                            {'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                            {'email': 'gtan0021@student.monash.edu',
                                            'organizer': True,
                                            'responseStatus': 'needsAction',
                                            'self': True}],
                            'created': '2022-09-23T19:31:23.000Z',
                            'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'end': {'dateTime': '2023-11-12T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                            'etag': '"3327998803674000"',
                            'eventType': 'default',
                            'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                            'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                            'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                            'kind': 'calendar#event',
                            'location': '98 Shirley Street PIMPAMA QLD 4209',
                            'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                        {'method': 'popup', 'minutes': 10}],
                                            'useDefault': False},
                            'sequence': 1,
                            'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                        'timeZone': 'Asia/Singapore'},
                            'status': 'confirmed',
                            'summary': 'Party 1',
                            'updated': '2022-09-24T16:35:19.824Z'},
                            {'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                            {'email': 'gtan0021@student.monash.edu',
                                            'organizer': True,
                                            'responseStatus': 'needsAction',
                                            'self': True}],
                            'created': '2022-09-23T19:25:04.000Z',
                            'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'end': {'dateTime': '2023-11-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                            'etag': '"3327998329967000"',
                            'eventType': 'default',
                            'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                            'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                            'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                            'kind': 'calendar#event',
                            'location': '98 Shirley Street PIMPAMA QLD 4209',
                            'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                            'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                        {'method': 'popup', 'minutes': 10}],
                                            'useDefault': False},
                            'sequence': 4,
                            'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                        'timeZone': 'Asia/Singapore'},
                            'status': 'confirmed',
                            'summary': 'Party 1',
                            'updated': '2022-09-24T16:33:45.612Z'}]
        self.eventsResultsFor2023 = {'accessRole': 'owner',
                                    'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                    'etag': '"p33kdp2t0tqmvk0g"',
                                    'items': [{'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:31:27.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-06-16T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998852039000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=ZmlkNWJ1ODNuY2o4OTRxNTRzZnRiaDI1bG8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'fid5bu83ncj894q54sftbh25lo@google.com',
                                                'id': 'fid5bu83ncj894q54sftbh25lo',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 1,
                                                'start': {'dateTime': '2023-06-15T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:36:04.625Z'},
                                            {'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:31:23.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-12T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998803674000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 1,
                                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:35:19.824Z'},
                                            {'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:25:04.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-26T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998329967000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                                                'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 4,
                                                'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:33:45.612Z'}],
                                    'kind': 'calendar#events',
                                    'summary': 'gtan0021@student.monash.edu',
                                    'timeZone': 'Asia/Singapore',
                                    'updated': '2022-09-24T16:36:04.625Z'}
        self.eventsOn2023Nov = [{'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                                {'email': 'gtan0021@student.monash.edu',
                                                'organizer': True,
                                                'responseStatus': 'needsAction',
                                                'self': True}],
                                'created': '2022-09-23T19:31:23.000Z',
                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'end': {'dateTime': '2023-11-12T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                'etag': '"3327998803674000"',
                                'eventType': 'default',
                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                'kind': 'calendar#event',
                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                            {'method': 'popup', 'minutes': 10}],
                                                'useDefault': False},
                                'sequence': 1,
                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                'status': 'confirmed',
                                'summary': 'Party 1',
                                'updated': '2022-09-24T16:35:19.824Z'},
                                {'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                                {'email': 'gtan0021@student.monash.edu',
                                                'organizer': True,
                                                'responseStatus': 'needsAction',
                                                'self': True}],
                                'created': '2022-09-23T19:25:04.000Z',
                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'end': {'dateTime': '2023-11-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                'etag': '"3327998329967000"',
                                'eventType': 'default',
                                'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                                'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                                'kind': 'calendar#event',
                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                            {'method': 'popup', 'minutes': 10}],
                                                'useDefault': False},
                                'sequence': 4,
                                'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                'status': 'confirmed',
                                'summary': 'Party 1',
                                'updated': '2022-09-24T16:33:45.612Z'}]
        self.eventResultsFor2023Nov = {'accessRole': 'owner',
                                    'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                    'etag': '"p33kdp2t0tqmvk0g"',
                                    'items': [{'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:31:23.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-12T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998803674000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 1,
                                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:35:19.824Z'},
                                            {'attendees': [{'email': 'bobross@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'gtan0021@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'needsAction',
                                                            'self': True}],
                                                'created': '2022-09-23T19:25:04.000Z',
                                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'end': {'dateTime': '2023-11-26T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'etag': '"3327998329967000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=cWNiazlxMWdhMWJoYmFoNzg2ZXU2bmxtbzAgZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                'iCalUID': 'qcbk9q1ga1bhbah786eu6nlmo0@google.com',
                                                'id': 'qcbk9q1ga1bhbah786eu6nlmo0',
                                                'kind': 'calendar#event',
                                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                'reminders': {'overrides': [{'method': 'email', 'minutes': 60},
                                                                            {'method': 'popup', 'minutes': 10}],
                                                            'useDefault': False},
                                                'sequence': 4,
                                                'start': {'dateTime': '2023-11-25T08:00:00+08:00',
                                                        'timeZone': 'Asia/Singapore'},
                                                'status': 'confirmed',
                                                'summary': 'Party 1',
                                                'updated': '2022-09-24T16:33:45.612Z'}],
                                    'kind': 'calendar#events',
                                    'summary': 'gtan0021@student.monash.edu',
                                    'timeZone': 'Asia/Singapore',
                                    'updated': '2022-09-24T16:36:04.625Z'}
        self.eventsOn2023Nov11 = [{'attendees': [{'email': 'bobross@gmail.com', 'responseStatus': 'needsAction'},
                                                {'email': 'gtan0021@student.monash.edu',
                                                'organizer': True,
                                                'responseStatus': 'needsAction',
                                                'self': True}],
                                'created': '2022-09-23T19:31:23.000Z',
                                'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'end': {'dateTime': '2023-11-12T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                'etag': '"3327998803674000"',
                                'eventType': 'default',
                                'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                'kind': 'calendar#event',
                                'location': '98 Shirley Street PIMPAMA QLD 4209',
                                'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                'reminders': {'overrides': [{'method': 'popup', 'minutes': 10},
                                                            {'method': 'email', 'minutes': 60}],
                                                'useDefault': False},
                                'sequence': 1,
                                'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                            'timeZone': 'Asia/Singapore'},
                                'status': 'confirmed',
                                'summary': 'Party 1',
                                'updated': '2022-09-24T16:35:19.824Z'}]    
        self.eventsResultFor2023Nov11 = {'accessRole': 'owner',
                                        'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                        'etag': '"p33kdp2t0tqmvk0g"',
                                        'items': [{'attendees': [{'email': 'bobross@gmail.com',
                                                                'responseStatus': 'needsAction'},
                                                                {'email': 'gtan0021@student.monash.edu',
                                                                'organizer': True,
                                                                'responseStatus': 'needsAction',
                                                                'self': True}],
                                                    'created': '2022-09-23T19:31:23.000Z',
                                                    'creator': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                    'end': {'dateTime': '2023-11-12T08:00:00+08:00',
                                                            'timeZone': 'Asia/Singapore'},
                                                    'etag': '"3327998803674000"',
                                                    'eventType': 'default',
                                                    'htmlLink': 'https://www.google.com/calendar/event?eid=c2ZubGRkMGk0bW00ZnQwbzBybmpjZHM2aW8gZ3RhbjAwMjFAc3R1ZGVudC5tb25hc2guZWR1&ctz=Asia/Singapore',
                                                    'iCalUID': 'sfnldd0i4mm4ft0o0rnjcds6io@google.com',
                                                    'id': 'sfnldd0i4mm4ft0o0rnjcds6io',
                                                    'kind': 'calendar#event',
                                                    'location': '98 Shirley Street PIMPAMA QLD 4209',
                                                    'organizer': {'email': 'gtan0021@student.monash.edu', 'self': True},
                                                    'reminders': {'overrides': [{'method': 'popup', 'minutes': 10},
                                                                                {'method': 'email', 'minutes': 60}],
                                                                'useDefault': False},
                                                    'sequence': 1,
                                                    'start': {'dateTime': '2023-11-11T08:00:00+08:00',
                                                            'timeZone': 'Asia/Singapore'},
                                                    'status': 'confirmed',
                                                    'summary': 'Party 1',
                                                    'updated': '2022-09-24T16:35:19.824Z'}],
                                        'kind': 'calendar#events',
                                        'summary': 'gtan0021@student.monash.edu',
                                        'timeZone': 'Asia/Singapore',
                                        'updated': '2022-09-24T16:36:04.625Z'}
    
    def test_getNavigatedEvents_nonEmptyValidYear_emptyMonthDay(self):
        """
        Tests if navigated events can be obtained successfully when only year 
        is specified, and year is in valid format.
        """
        mock_api = Mock()
        year = "2023"
        month = ""
        day = ""
        mock_api.events.return_value.list.return_value.execute.return_value = self.eventsResultsFor2023
        self.assertEqual(self.eventsIn2023,MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_nonEmptyInvalidYear_emptyMonthDay(self):
        """
        Tests if navigated events can't be obtained when only year 
        is specified, but year is in valid format.
        """
        mock_api = Mock()
        year = "202"
        month = ""
        day = ""
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_emptyYear_nonEmptyMonthDay(self):
        """
        Tests if navigated events can't be obtained when year 
        is not specified, but month and day are specified.
        """
        mock_api = Mock()
        year = ""
        month = "11"
        day = "12"
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_nonEmptyYearMonth_validYearMonth_emptyDay(self):
        """
        Tests if navigated events can be obtained successfully when only year 
        and month are specified, and year and and month are in valid format.
        """
        mock_api = Mock()
        year = "2023"
        month = "11"
        day = ""
        mock_api.events.return_value.list.return_value.execute.return_value = self.eventResultsFor2023Nov
        self.assertEqual(self.eventsOn2023Nov,MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_nonEmptyYearMonth_invalidMonth_emptyDay(self):
        """
        Tests if navigated events can't be obtained when only year and month 
        is specified, but month is not in between 1 and 12.
        """
        mock_api = Mock()
        year = "2021"
        month = "13"
        day = ""
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))
        
    def test_getNavigatedEvents_emptyYearMonth_nonEmptyDay(self):
        """
        Tests if navigated events can't be obtained when year and month
        are not specified, but day is specified.
        """
        mock_api = Mock()
        year = ""
        month = ""
        day = "12"
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_nonEmptyYearMonthDay_validYearMonthDay(self):
        """
        Tests if navigated events can be obtained successfully when year, month
        and day are specified in the valid format. 
        """
        mock_api = Mock()
        year = "2023"
        month = "12"
        day = "31"
        mock_api.events.return_value.list.return_value.execute.return_value = self.eventsResultFor2023Nov11
        self.assertEqual(self.eventsOn2023Nov11,MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_nonEmptyYearMonthDay_validYearMonth_invalidDay(self):
        """
        Tests if navigated events can't be obtained when year, month and day
        are specified, but day is not in between 1 and 31.
        """
        mock_api = Mock()
        year = "2021"
        month = "11"
        day = "32"
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))

    def test_getNavigatedEvents_emptyYearMonthDay(self):
        """
        Tests if navigated events can't be obtained when year, month
        and day are not specified.
        """
        mock_api = Mock()
        year = ""
        month = ""
        day = ""
        self.assertFalse(MyEventManager.getNavigatedEvents(mock_api,year,month,day))

class TestNavigateForward(unittest.TestCase):
    def test_nonEmptyValidYear_emptyMonth_emptyDay(self):
        """
        Tests the navigateForward function in MyEventManger.py
        It tests that if a non-empty valid year is entered, but no month or day, then it will increment to the next year
        """
        year = "2022"
        month = ""
        day = ""
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2023', '', ''))

    def test_emptyYear_nonEmptyMonth_nonEmptyDay(self):
        """
        Tests whether the navigateForward function in MyEventManager.py
        returns false when given an empty year, non-empty month and non-empty day.
        """
        year = ""
        month = "11"
        day = "12"
        self.assertFalse(MyEventManager.navigateForward(year, month, day))

    def test_nonEmptyValidYear_nonEmptyValidMonth_emptyDay_beforeDec(self):
        """
        Tests whether navigateForward function in MyEventManager.py navigates to next month when current month is before December
        when given a year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "11"
        day = ""
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2022', '12', ''))
    
    def test_nonEmptyValidYear_nonEmptyValidMonth_emptyDay_afterDec(self):
        """
        Tests whether navigateForward function in MyEventManager.py navigates to next year January when current month is December
        when given a year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "13"
        day = ""
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2023', '01', ''))

    def test_emptyYear_emptyMonth_nonEmptyDay(self):
        """
        Test whether navigateForward function returns false when given an empty year, empty month, and a non-empty day.
        """
        year = ""
        month = ""
        day = "12"
        self.assertFalse(MyEventManager.navigateForward(year, month, day))

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_before31(self):
        """
        Test whether navigateForward function in MyEventManager.py navigates to next day when current day is lesser
        than 31 when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "11"
        day = "12"
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2022', '11', '13'))  

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_after31_notDec(self):
        """
        Test whether navigateForward function in MyEventManager.py navigates to first day of next month when current day is greater
        than 31 when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "11"
        day = "32"
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2022', '12', '01'))     

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_after31_Dec(self):
        """
        Test whether navigateForward function in MyEventManager.py navigates to first day of next year when current day is greater
        than 31 and current month is December when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "12"
        day = "32"
        self.assertEqual(MyEventManager.navigateForward(year, month, day), ('2023', '01', '01')) 

    def test_emptyYear_emptyMonth_emptyDay(self):
        """
        Tests if the navigateForward function in MyEventManager.py returns false when given an empty year, month and day
        """
        year = ""
        month = ""
        day = ""
        self.assertFalse(MyEventManager.navigateForward(year, month, day))                                
    
class TestNavigateBackward(unittest.TestCase):
    def test_nonEmptyValidYear_emptyMonth_emptyDay(self):
        """
        Tests the navigateBackward function in MyEventManger.py
        It tests that if a non-empty valid year is entered, but no month or day, then it will navigate to the previous year
        """
        year = "2022"
        month = ""
        day = ""
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2021', '', ''))

    def test_emptyYear_nonEmptyMonth_nonEmptyDay(self):
        """
        Tests whether the navigateBackward function in MyEventManager.py
        returns false when given an empty year, non-empty month and non-empty day.
        """
        year = ""
        month = "1"
        day = "13"
        self.assertFalse(MyEventManager.navigateBackward(year, month, day))

    def test_nonEmptyValidYear_nonEmptyValidMonth_emptyDay_afterJan(self):
        """
        Tests whether navigateBackward function in MyEventManager.py navigates to previous month when current month is after January
        when given a year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "2"
        day = ""
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2022', '01', ''))
    
    def test_nonEmptyValidYear_nonEmptyValidMonth_emptyDay_beforeJan(self):
        """
        Tests whether navigateBackward function in MyEventManager.py navigates to previous year December when current month is less than January
        when given a year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "0"
        day = ""
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2021', '12', ''))

    def test_emptyYear_emptyMonth_nonEmptyDay(self):
        """
        Test whether navigateBackward function returns false when given an empty year, empty month, and a non-empty day.
        """
        year = ""
        month = ""
        day = "13"
        self.assertFalse(MyEventManager.navigateBackward(year, month, day))

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_afterD1(self):
        """
        Test whether navigateBackward function in MyEventManager.py navigates to previous day when current day is greater
        than 1 when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "2"
        day = "13"
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2022', '02', '12'))  

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_beforeD1_notJan(self):
        """
        Test whether navigateBackward function in MyEventManager.py navigates to last day of previous month when current day is lesser
        than 1 when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "2"
        day = "0"
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2022', '01', '31'))     

    def test_nonEmptyValidYear_nonEmptyValidMonth_nonEmptyValidDay_beforeD1_Jan(self):
        """
        Test whether navigateBackward function in MyEventManager.py navigates to last day of previous year when current day is lesser
        than 1 and current month is January when given year, month, and day that are all valid inputs. 
        """
        year = "2022"
        month = "1"
        day = "0"
        self.assertEqual(MyEventManager.navigateBackward(year, month, day), ('2021', '12', '31')) 

    def test_emptyYear_emptyMonth_emptyDay(self):
        """
        Tests if the navigateForward function in MyEventManager.py returns false when given an empty year, month and day
        """
        year = ""
        month = ""
        day = ""
        self.assertFalse(MyEventManager.navigateBackward(year, month, day))

class SearchEventByDateTest(unittest.TestCase):
    def setUp(self):
        """
        The setUp function is called before each test function. It is used to
        set up the objects that the tests will use. 
        """
        self.searchedEventsForDec = [{'attendees': [{'email': 'baoqii13@gmail.com',
                                    'responseStatus': 'needsAction'},
                                    {'email': 'blee0047@student.monash.edu',
                                    'organizer': True,
                                    'responseStatus': 'accepted',
                                    'self': True}],
                                    'created': '2022-09-25T10:03:12.000Z',
                                    'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'end': {'date': '2022-12-22'},
                                    'etag': '"3328200385304000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=NnQ2Y2Fubm1pOWNxODk0MXVtZThxYm1uNGMgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': '6t6cannmi9cq8941ume8qbmn4c@google.com',
                                    'id': '6t6cannmi9cq8941ume8qbmn4c',
                                    'kind': 'calendar#event',
                                    'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': False},
                                    'sequence': 0,
                                    'start': {'date': '2022-12-21'},
                                    'status': 'confirmed',
                                    'summary': 'Test event for search event part 2',
                                    'transparency': 'transparent',
                                    'updated': '2022-09-25T10:03:12.652Z'}]
        self.searchEventResults = {'accessRole': 'owner',
                                    'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                    'etag': '"p33g9bql6r2nvk0g"',
                                    'items': [{'attendees': [{'email': 'baoqii13@gmail.com',
                                                            'responseStatus': 'needsAction'},
                                                            {'email': 'blee0047@student.monash.edu',
                                                            'organizer': True,
                                                            'responseStatus': 'accepted',
                                                            'self': True}],
                                                'created': '2022-09-25T10:03:12.000Z',
                                                'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                'end': {'date': '2022-12-22'},
                                                'etag': '"3328200385304000"',
                                                'eventType': 'default',
                                                'htmlLink': 'https://www.google.com/calendar/event?eid=NnQ2Y2Fubm1pOWNxODk0MXVtZThxYm1uNGMgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                                'iCalUID': '6t6cannmi9cq8941ume8qbmn4c@google.com',
                                                'id': '6t6cannmi9cq8941ume8qbmn4c',
                                                'kind': 'calendar#event',
                                                'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                'reminders': {'useDefault': False},
                                                'sequence': 0,
                                                'start': {'date': '2022-12-21'},
                                                'status': 'confirmed',
                                                'summary': 'Test event for search event part 2',
                                                'transparency': 'transparent',
                                                'updated': '2022-09-25T10:03:12.652Z'}],
                                    'kind': 'calendar#events',
                                    'summary': 'blee0047@student.monash.edu',
                                    'timeZone': 'Asia/Kuala_Lumpur',
                                    'updated': '2022-09-25T10:03:12.652Z'}
                    
    def test_searchWithInvalidDate(self):
        """
        Tests whether the searchEvent_by_date function in MyEventManager.py returns False if give an invalid date to search for.
        """
        mock_api = Mock()
        event_date = ""
        self.assertFalse(MyEventManager.searchEvent_by_date(mock_api,event_date))

    def test_searchWithValidDate(self):
        """
        Tests whether the searchEvent_by_date function in MyEventManager.py returns a list of events that match the specified date.
        """
        mock_api = Mock()
        event_date = "2022-12-21"
        mock_api.events.return_value.list.return_value.execute.return_value = self.searchEventResults
        self.assertEqual(self.searchedEventsForDec, MyEventManager.searchEvent_by_date(mock_api,event_date))

class SearchEventByNameKeywordTest(unittest.TestCase):
    def setUp(self):
        """
        The setUp function is called before each test function. It is used to
        set up the objects that the tests will use. 
        """
        self.sampleUppercaseEvent = [{'created': '2022-09-25T12:48:01.000Z',
                                    'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'end': {'date': '2022-11-16'},
                                    'etag': '"3328222324804000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=MDhlc2hxcWh1Z2dqbHI5N2hrNnFoZG91Y3QgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': '08eshqqhuggjlr97hk6qhdouct@google.com',
                                    'id': '08eshqqhuggjlr97hk6qhdouct',
                                    'kind': 'calendar#event',
                                    'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': False},
                                    'sequence': 0,
                                    'start': {'date': '2022-11-15'},
                                    'status': 'confirmed',
                                    'summary': 'uppercase SEARCH EVENT',
                                    'transparency': 'transparent',
                                    'updated': '2022-09-25T13:06:02.402Z'}]
        self.sampleUppercaseEventResults = {'accessRole': 'owner',
                                            'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                            'etag': '"p33ofl6lvgqofk0g"',
                                            'items': [{'created': '2022-09-25T12:48:01.000Z',
                                                        'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                        'end': {'date': '2022-11-16'},
                                                        'etag': '"3328222324804000"',
                                                        'eventType': 'default',
                                                        'htmlLink': 'https://www.google.com/calendar/event?eid=MDhlc2hxcWh1Z2dqbHI5N2hrNnFoZG91Y3QgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                                        'iCalUID': '08eshqqhuggjlr97hk6qhdouct@google.com',
                                                        'id': '08eshqqhuggjlr97hk6qhdouct',
                                                        'kind': 'calendar#event',
                                                        'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                        'reminders': {'useDefault': False},
                                                        'sequence': 0,
                                                        'start': {'date': '2022-11-15'},
                                                        'status': 'confirmed',
                                                        'summary': 'uppercase SEARCH EVENT',
                                                        'transparency': 'transparent',
                                                        'updated': '2022-09-25T13:06:02.402Z'}],
                                            'kind': 'calendar#events',
                                            'summary': 'blee0047@student.monash.edu',
                                            'timeZone': 'Asia/Kuala_Lumpur',
                                            'updated': '2022-09-25T13:29:51.814Z'}
        self.sampleEventToSearch =  [{'created': '2022-09-25T12:48:22.000Z',
                                    'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'end': {'date': '2022-11-24'},
                                    'etag': '"3328220205154000"',
                                    'eventType': 'default',
                                    'htmlLink': 'https://www.google.com/calendar/event?eid=MGZwNnAxNTcwcWY5cWJ2MHRmM2trMHF2Y2EgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                    'iCalUID': '0fp6p1570qf9qbv0tf3kk0qvca@google.com',
                                    'id': '0fp6p1570qf9qbv0tf3kk0qvca',
                                    'kind': 'calendar#event',
                                    'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                    'reminders': {'useDefault': False},
                                    'sequence': 0,
                                    'start': {'date': '2022-11-23'},
                                    'status': 'confirmed',
                                    'summary': 'Add title and time',
                                    'transparency': 'transparent',
                                    'updated': '2022-09-25T12:48:22.577Z'}]
        self.sampleEventToSearchResults = {'accessRole': 'owner',
                                            'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                            'etag': '"p33ofl6lvgqofk0g"',
                                            'items': [{'created': '2022-09-25T12:48:22.000Z',
                                                        'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                        'end': {'date': '2022-11-24'},
                                                        'etag': '"3328220205154000"',
                                                        'eventType': 'default',
                                                        'htmlLink': 'https://www.google.com/calendar/event?eid=MGZwNnAxNTcwcWY5cWJ2MHRmM2trMHF2Y2EgYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                                        'iCalUID': '0fp6p1570qf9qbv0tf3kk0qvca@google.com',
                                                        'id': '0fp6p1570qf9qbv0tf3kk0qvca',
                                                        'kind': 'calendar#event',
                                                        'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                        'reminders': {'useDefault': False},
                                                        'sequence': 0,
                                                        'start': {'date': '2022-11-23'},
                                                        'status': 'confirmed',
                                                        'summary': 'Add title and time',
                                                        'transparency': 'transparent',
                                                        'updated': '2022-09-25T12:48:22.577Z'}],
                                            'kind': 'calendar#events',
                                            'summary': 'blee0047@student.monash.edu',
                                            'timeZone': 'Asia/Kuala_Lumpur',
                                            'updated': '2022-09-25T13:29:51.814Z'}
        self.sampleEventToSearchByKeyword =  [{'created': '2022-09-25T12:49:04.000Z',
                                            'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                            'description': 'Can search by keyword too',
                                            'end': {'date': '2022-11-25'},
                                            'etag': '"3328220288258000"',
                                            'eventType': 'default',
                                            'htmlLink': 'https://www.google.com/calendar/event?eid=NzFhNWdsaGRjdG9zcDhxdmtoc2U5OGI4OG8gYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                            'iCalUID': '71a5glhdctosp8qvkhse98b88o@google.com',
                                            'id': '71a5glhdctosp8qvkhse98b88o',
                                            'kind': 'calendar#event',
                                            'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                            'reminders': {'useDefault': False},
                                            'sequence': 0,
                                            'start': {'date': '2022-11-24'},
                                            'status': 'confirmed',
                                            'summary': 'Test Event for search event',
                                            'transparency': 'transparent',
                                            'updated': '2022-09-25T12:49:04.129Z'}]
        self.sampleEventToSearchByKeywordResults = {'accessRole': 'owner',
                                                    'defaultReminders': [{'method': 'popup', 'minutes': 10}],
                                                    'etag': '"p33ofl6lvgqofk0g"',
                                                    'items': [{'created': '2022-09-25T12:49:04.000Z',
                                                                'creator': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                                'description': 'Can search by keyword too',
                                                                'end': {'date': '2022-11-25'},
                                                                'etag': '"3328220288258000"',
                                                                'eventType': 'default',
                                                                'htmlLink': 'https://www.google.com/calendar/event?eid=NzFhNWdsaGRjdG9zcDhxdmtoc2U5OGI4OG8gYmxlZTAwNDdAc3R1ZGVudC5tb25hc2guZWR1',
                                                                'iCalUID': '71a5glhdctosp8qvkhse98b88o@google.com',
                                                                'id': '71a5glhdctosp8qvkhse98b88o',
                                                                'kind': 'calendar#event',
                                                                'organizer': {'email': 'blee0047@student.monash.edu', 'self': True},
                                                                'reminders': {'useDefault': False},
                                                                'sequence': 0,
                                                                'start': {'date': '2022-11-24'},
                                                                'status': 'confirmed',
                                                                'summary': 'Test Event for search event',
                                                                'transparency': 'transparent',
                                                                'updated': '2022-09-25T12:49:04.129Z'}],
                                                    'kind': 'calendar#events',
                                                    'summary': 'blee0047@student.monash.edu',
                                                    'timeZone': 'Asia/Kuala_Lumpur',
                                                    'updated': '2022-09-25T13:29:51.814Z'}

    def test_searchEventWithUppercase(self):
        """
        Tests whether the searchEvent_by_name_keyword function in MyEventManager.py returns events even if the input query is uppercase letters
        """
        mock_api = Mock()
        query = "UPPERCASE"
        mock_api.events.return_value.list.return_value.execute.return_value = self.sampleUppercaseEventResults
        self.assertEqual(self.sampleUppercaseEvent, MyEventManager.searchEvent_by_name_keyword(mock_api,query))

    def test_searchEventByName(self):
        """
        Tests whether the searchEvent_by_name_keyword function in MyEventManager.py returns events that matches the event name given a query        
        """
        mock_api = Mock()
        query = "Add title"
        mock_api.events.return_value.list.return_value.execute.return_value = self.sampleEventToSearchResults
        self.assertEqual(self.sampleEventToSearch, MyEventManager.searchEvent_by_name_keyword(mock_api,query))

    def test_searchEventByKeyword(self):
        """
        Tests whether the searchEvent_by_name_keyword function in MyEventManager.py returns events that matches the event keyword given a query  
        """
        mock_api = Mock()
        query = "keyword"
        mock_api.events.return_value.list.return_value.execute.return_value = self.sampleEventToSearchByKeywordResults
        self.assertEqual(self.sampleEventToSearchByKeyword, MyEventManager.searchEvent_by_name_keyword(mock_api,query))


if __name__ == "__main__":
    unittest.main(verbosity=2)
