import datetime as dt
from os import times_result
import statistics
import time
import re

monthStrDict = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
viewYYYYLowerBound = dt.datetime.now().year - 5
viewYYYYUpperBound = dt.datetime.now().year + 5
viewYYLowerBound = int(str(dt.datetime.now().year)[2:4])-5
viewYYUpperBound = int(str(dt.datetime.now().year)[2:4])+5
streetStrVariantList = ["Street", "St", "Avenue", "Ave", "Av","Alley","Aly","Bend","Bnd","Cape","Cpe",
	"Creek","Crk","Field","Fld","Junction","Jct","Lane","Ln","Rdige","Rdg","Road","Rd","Square","Sq","Valley","Vly"]



class Event:
	def __init__(self,api,name,location,attendees,organiser,owner,startDate,endDate,status="",isAttending=False,uploadEvent=True,emailNotifMinuteList=[],popupNotifMinuteList=[]):

		self.api = api
		self.id = None
		self.name = name
		self.location = location
		assert len(attendees) <= 20, "Number of attendees exceeded 20"
		self.attendees = attendees
		self.organiser = organiser
		self.owner = owner
		self.startDate = startDate
		self.endDate = endDate
		self.isAttending = isAttending
		self.status = status
		self.emailNotifMinuteList = emailNotifMinuteList
		self.popupNotifMinuteList = popupNotifMinuteList
		if isAttending:
			self.attendees.append(organiser)
		if uploadEvent:
			self.addToCalendar()
	def getReminderData(self):
		return {
			'useDefault': False,
			'overrides': 
			[{'method': 'email', 'minutes': mins} for mins in self.emailNotifMinuteList] +
			[{'method': 'popup', 'minutes': mins} for mins in self.popupNotifMinuteList]
		}
	def getCalendarData(self):
		timezone = 'Asia/Singapore'
		calendar = {
			'summary': self.name,
			'location': self.location.address,
			'description': '',
			'start': {
				'dateTime': str(self.startDate), 
				'timeZone': timezone,
			},
			'end': {
				'dateTime': str(self.endDate),
				'timeZone': timezone,
			},
			'reminders': self.getReminderData(),
			"attendees": [ { "email": a.email, 'self' : a.isSelf} for a in self.attendees],
			"creator": { "email": self.owner.email, 'self': self.owner.isSelf}, 
			"organizer": { "email": self.organiser.email, 'self': self.organiser.isSelf} 
		}
		return calendar

	def addToCalendar(self):
		# if self.startDate.year > 2050 or self.endDate.year > 2050:
		# 	raise Exception("Event later than 2050 can't be created")
			
		calendar = self.getCalendarData()
		data = self.api.events().insert(calendarId='primary',body=calendar).execute()
		print (f'Event created: {data.get("htmlLink")}')
		self.id = data['id']
		return data

	def deleteFromCalendar(self):
		try:
			isOrganiser = Attendee.checkIsOrganiser(self.getCalendarData())
			if not isOrganiser:
				raise Exception("Only organisers are allowed to update the event details")
			currentTime = dt.datetime.now()
			if(not currentTime>=self.endDate.getTime()):
				raise Exception("Can't delete future events!")
			
			self.api.events().delete(calendarId='primary', eventId=self.id).execute() 
			print("Event successfully deleted")
			return True
		except Exception as e:
			print(e)
			print("Event not successfully deleted")
			return False

	def setEventAddress(self,address):
		try:
			isOrganiser = Attendee.checkIsOrganiser(self.getCalendarData())
			if not isOrganiser:
				raise Exception("Only organisers are allowed to update the event details")
			self.location = Location(address)
			patchData = {'location' : self.location.address}
			self.api.events().patch(calendarId='primary', eventId=self.id,body=patchData,sendUpdates="all").execute()
			return True
		except AssertionError as e:
			print(e)
			return False
		except Exception as e:
			print(e)
			return False
		

	def cancelEvent(self):
		try:
			isOrganiser = Attendee.checkIsOrganiser(self.getCalendarData())
			if not isOrganiser:
				raise Exception("Only organisers are allowed to update the event details")

			patchData = {'status' : 'cancelled'}
			currentTime = dt.datetime.now()

			if(currentTime<=self.startDate.getTime()):
				self.api.events().patch(calendarId='primary', eventId=self.id,body=patchData).execute()
				print("Event was successfully canceled!")
				return True 
				
			raise Exception("Can't cancel past events")
		except Exception as e:
			print(e)
			return False

	def restoreEvent(self):
		try:
			isOrganiser = Attendee.checkIsOrganiser(self.getCalendarData())
			if not isOrganiser:
				raise Exception("Only organisers are allowed to update the event details")

			currentTime = dt.datetime.now()
			if(currentTime<=self.startDate.getTime()):
				patchData = {'status' : 'confirmed'}
				self.api.events().patch(calendarId='primary', eventId=self.id,body=patchData).execute()
				print("Event was successfully restored!")
				return True
			raise Exception("Can't restore past events")
		except Exception as e:
			print(e)
			return False
	
	def addEmailReminder(self,minutesBeforeStartDate):
		try:
			if(minutesBeforeStartDate<0 or minutesBeforeStartDate>40320):
				raise AssertionError("minutes out of bounds") 
			self.emailNotifMinuteList.append(minutesBeforeStartDate)
			patchData = {'reminders': self.getReminderData()}
			self.api.events().patch(calendarId='primary', eventId=self.id,body=patchData).execute()
			print("Email reminder added.")
		except:
			print ("Email reminder not added.")


	def addPopupReminder(self,minutesBeforeStartDate):
		try:
			if(minutesBeforeStartDate<0 or minutesBeforeStartDate>40320):
				raise AssertionError("minutes out of bounds") 
			self.popupNotifMinuteList.append(minutesBeforeStartDate)
			patchData = {'reminders': self.getReminderData()}
			self.api.events().patch(calendarId='primary', eventId=self.id,body=patchData).execute()
			print("Notification reminder added.")
		except:
			print ("Notification reminder not added.")

	@staticmethod
	def fromData(api,data):
		id = data['id']
		name = data['summary']
		if('location' in list(data.keys())):
			location = Location(data['location'])
		else:
			# location = Location(None) 
			raise Exception("Event without location is invalid for us.")

		attendees = [Attendee(attendee['email']) for attendee in data['attendees']]
		organiser = Attendee(data['organizer']['email'],data['organizer']['self'] if 'self' in list(data['organizer'].keys()) else False)
		owner = Attendee(data['creator']['email'],data['creator']['self'] if 'self' in list(data['creator'].keys()) else False)
		tSplit = str(data['start']['dateTime']).split("T")
		startDate = tSplit[0]
		startHour = tSplit[1].split(":")[0]
		startMinute = tSplit[1].split(":")[1]
		tSplit = str(data['end']['dateTime']).split("T")
		endDate = tSplit[0]
		endHour = tSplit[1].split(":")[0]
		endMinute = tSplit[1].split(":")[1]
		status = data['status']
		emailNotifMinuteList = []
		popupNotifMinuteList = []
		if('overrides' in list(data['reminders'].keys())):
			for reminder in data['reminders']['overrides']:
				if(reminder['method']=="email"):
					emailNotifMinuteList.append(reminder['minutes']) 
				else:
					popupNotifMinuteList.append(reminder['minutes'])   
		event = Event(api,name,location,attendees,organiser,owner,Date(startDate,"%s:%s" % (startHour,startMinute)),Date(endDate,"%s:%s" % (endHour,endMinute)),status=status,uploadEvent=False,emailNotifMinuteList=emailNotifMinuteList,popupNotifMinuteList=popupNotifMinuteList)
		event.id = id 
		return event 

class Location:
	def __init__(self,address="ONLINE"): #,streetNumber,streetName, country,zipCode
		# try:
		self.address = address 
		self.isPhysical = address.upper()!="ONLINE"
		self.validateSelf()
	
	@staticmethod
	def isLocationValid(address):
		addressHasStreet = False 
		for streetStr in streetStrVariantList: #A2
			if(streetStr in address): 
				addressHasStreet = True 
				break
		if(not addressHasStreet):
			return False 
		splitAddress = address.split(" ") 
		australian = False 
		american = False 
		if(len(splitAddress)>=2): #AA0
			stateCode = splitAddress[-2]
			postalCode = splitAddress[-1]
			if(stateCode==stateCode.upper() and stateCode.isalpha()): #AAA0
				if(len(stateCode)==3): #AAAA0
					australian = True 
				elif(len(stateCode)==2): #AAAB0
					american = True 
				else: #AAAC0
					return False
			else: #AAB0
				return False
			if(postalCode.isnumeric()):  #AAC0
				if(australian and len(postalCode)==4): #AACA0
					pass 
				elif(american and len(postalCode)==5): #AACB0
					pass 
				else: #AACC0
					return False
			else: #AAD0
				return False
		else: #AB0
			return False
		return True

	def validateSelf(self): #0
		if(self.address.upper()!="ONLINE"): #A0
			if(Location.isLocationValid(self.address)):
				pass 
			else:
				raise AssertionError("invalid address")
		else: #B
			if(self.isPhysical==True):
				raise AssertionError("An event location with no address cannot be physical") # 34

class Attendee:
	def __init__(self,email,isSelf=True):
		try:
			self.email = email
			self.isSelf=isSelf
		#self.isOwner = isOwner
		except Exception as e:
			print(e)
	
	@staticmethod
	def isEmailValid(email):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		return re.fullmatch(regex,email)

	# Check whether user is an attendee of a certain event
	def checkIsAttendee(event):
		if 'attendees' in event:
			for attendee in event['attendees']:
				if 'self' in attendee and attendee['self']:
					return True
		else: # no attendee list
			return False

	@staticmethod
	def checkIsOrganiser(event):
		organiserInfo = event['organizer']
		if 'self' not in organiserInfo or (not organiserInfo['self']):
			return False
		elif 'self' in organiserInfo and organiserInfo['self']:
			return True
		else:
			return False
	
class Date:
	def __init__(self,dateStr,timeStr="00:00"):
		if(Date.isDateValid(dateStr)):
			self.year, self.month, self.day = self.extractDateFromDateStr(dateStr)
		else:
			raise AssertionError("Invalid date string")
		if(Date.isTimeValid(timeStr)):
			self.hour, self.minute =  self.extractTimeFromTimeStr(timeStr)
		else:
			raise AssertionError("Invalid time string")
		

		assert self.year >=50 and self.year <=2050, "Year exceeded 2050"

	def extractDateFromDateStr(self,dateStr):
		splitDate = dateStr.split("-")
		year = 0; month = 0; day = 0;
		if(splitDate[1].isnumeric()):
			month = int(splitDate[1])
			year = int(splitDate[0])
			day = int(splitDate[2])
		else: 
			month = monthStrDict[splitDate[1]]
			year = int(splitDate[2])
			if(year<=50):
				year += 2000
			else:
				year += 1900
			day = int(splitDate[0])
		return year, month, day

	def extractTimeFromTimeStr(self,timeStr):
		if Date.isTimeValid(timeStr):
			hour,minute = timeStr.split(":") 
			hour,minute = int(hour),int(minute)
			return hour,minute
		else:
			raise AssertionError("Please enter correct details for time")
		
	@staticmethod
	def isTimeValid(time):
		try:
			hour,minute = time.split(':')
			if not (hour.isnumeric() and len(hour) == 2 and (int(hour)>=0 and int(hour)<=23)):
				print("Time must be given in HH:MM format where HH is a 2 digit number and within 0-23")
				return False
			if not (minute.isnumeric() and len(minute) == 2 and (int(minute)>=0 and int(minute)<=59)):
				print("Time must be given in HH:MM format where MM is a 2 digit number and within 0-59")
				return False
			return True
		except:
			print("Time must be given in HH:MM format")
			return False

	@staticmethod
	def isDateValid(date,viewing=False):
		try:
			part1,month,part3 = date.split('-')
			monthIsNumeric = month.isnumeric()
			if(monthIsNumeric): 
				year = part1 
				day = part3
			else:
				year = part3
				day = part1
			if viewing:

				if not (monthIsNumeric and year.isnumeric() and len(year) == 4 and (viewYYYYLowerBound <= int(year) <= viewYYYYUpperBound)) and not (not monthIsNumeric and year.isnumeric() and len(year) == 2 and (viewYYLowerBound <= int(year) <= viewYYUpperBound)):
					print("Date should be in either YYYY-MM-DD or DD-MON-YY format")
					print(f"Year can only be between {viewYYYYLowerBound} and {viewYYYYUpperBound} for viewing")
					return False
			else:
			
				if not (monthIsNumeric and year.isnumeric() and len(year) == 4 and (int(year)>=0 and int(year)<=2050)) and not (not monthIsNumeric and year.isnumeric() and len(year) == 2 and (int(year)>=0 and int(year)<=99)):
					print("Date should be in either YYYY-MM-DD or DD-MON-YY format")
					print(f"Year can't be later than 2050 for creating or editing event")
					return False

			if not (month.isnumeric() and len(month) == 2 and (int(month)>=1 and int(month)<=12)) and not (month in list(monthStrDict.keys())):
				print("Date should be in either YYYY-MM-DDor DD-MON-YY format")
				print("Month must be within 1-12")
				return False
			if not (day.isnumeric() and len(day) == 2 and (int(day)>=1 and int(day)<=31)):
				print("Date should be in either YYYY-MM-DD or DD-MON-YY format")
				print("Day must be within 1-31")
				return False
			return True
		except:
			print("Date should be in either YYYY-MM-DD or DD-MON-YY format")
			return False

	@staticmethod
	def isStartDateTimeBeforeEndDateTime(startDate,startTime,endDate,endTime):
		'''
		By the time we reach here, our dates and times should already be in correct format.
		Do check.
		'''
		start = Date(startDate,startTime)
		end = Date(endDate,endTime)

		if start.year == end.year and start.month == end.month and start.day==end.day:
			if start.hour == end.hour: 
				return start.minute <= end.minute # If same year,month,day,hour but start min > end min
			else:
				return start.hour < end.hour       # If same year,month,day, but start hour < end hour or start hour > end hour

		elif start.year == end.year and start.month == end.month:
			return start.day < end.day              # If same year,month, but start day < end day or start day > end day

		elif start.year == end.year:
			return start.month < end.month          # If same year, but start month < end month or start month > end month
		
		else:
			return start.year < end.year            # start.year < end.year or start.year > end.year
	
	def __str__(self):
		return "%s-%s-%sT%s:%s:00+08:00" % (str(self.year).rjust(4, "0"),str(self.month).rjust(2, "0"),str(self.day).rjust(2, "0"),str(self.hour).rjust(2, "0"),str(self.minute).rjust(2, "0"))
	def getTime(self):
		return dt.datetime(self.year,self.month,self.day,self.hour,self.minute)

if __name__ == "__main__":
	print(str(Date("0950-01-01","05:09")))
	print(Date.isDateValid("2027-11-31",True))