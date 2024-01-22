from MyEventManager import *
class App():
	def __init__(self,api):
		self.started = False
		self.api = api
		self.loadEventList()
		self.eventsChanged = False 

	def loadEventList(self):
		self.eventList = get_all_events(self.api)

	def start(self):
		print("Welcome to the MyEventManager App!")
		exited = False 
		while(not exited):
			self.loadEventList()
			self.checkForNotifs(eventList)
			self.printMainMenu()
			inp = input("Please select a menu option by entering its index (1-6): ").upper()
			if(inp=="1"): 
				self.viewEvents()
			elif(inp=="2"):
				self.createEvent()
			elif(inp=="3"): 
				self.importEvent()
			elif(inp=="4"): 
				self.searchEventByNameKeyWord()
			elif(inp=="5"): 
				self.searchEventByDate()
			elif(inp=="6"): 
				self.navigateEvents()
			elif(inp=="M"):
				self.printMainMenu()
			elif(inp=="E"):
				exited = True 
			else:
				print("Invalid input! Please try again.")
				self.printMainMenu()
		print("Thank you for using this application!")
		
	def printMainMenu(self):
		print("-----MAIN MENU-----")
		print("1| View all events")
		print("2| Create an event")
		print("3| Import an event")
		print("4| Search event by name/keyword")
		print("5| Search event by date")
		print("6| Navigate events through year,month or day")
		print("M| Show menu")
		print("E| Exit application")
		print("-"*20)
	
	def checkForNotifs(self, eventArr):
		notifiableEventList = checkForEventNotifications(eventArr) 
		if(len(notifiableEventList)>0):
			print("-----REMINDERS-----")
			i = 1
			for event in notifiableEventList:
				print(f"{i}| Event {event.name} starting soon on {event.startDate.getTime()}")
				i += 1

	def viewEvents(self):
		self.listEvents(self.eventList,True)
	
	def viewCancelledEvents(self):
		self.listEvents(self.cancelledEventList,True)
	
	def createEvent(self):
		try:
			print("1| Create own event")
			print("2| Create event on behalf of others")
			choice = input("Enter choice (1/2): ")

			if choice  == "1":
				name = input("Event name: ") 
				address = input("Event address (NONE if virtual): ")
				if(address.upper()=="NONE"):
					address = "Online"
				location = Location(address)
				attendees = []
				while(True):
					print("Please enter attendee details; enter QUIT to stop")
					attEmail = input("attendee email: ")
					if(attEmail.upper()=="QUIT"): break 
					attendees.append(Attendee(attEmail))
					print("Attendee added!")

				isAttending = input("Are you attending? (Y/N): ") 

				if isAttending == "Y":
					isAttending = True
				elif isAttending == "N":
					isAttending = False
				else:
					raise AssertionError("Enter Y or N for is attending.")

				userEmail = input("Enter your email: ") 
				organiser = Attendee(userEmail)
				owner = Attendee(userEmail)

				startDateStr = input("Event start date (YYYY-MM-DD or DD-MON-YY): ")
				startDateHours = input("Event start date hour (HH): ")
				startDateMinutes = input("Event start date minutes (MM): ")
				startDate = Date(startDateStr,"%s:%s" % (startDateHours,startDateMinutes))
				endDateStr = input("Event end date (YYYY-MM-DD or DD-MON-YY): ")
				endDateHours = input("Event end date hour (HH): ")
				endDateMinutes = input("Event end date minutes (MM): ")
				endDate = Date(endDateStr,"%s:%s" % (endDateHours,endDateMinutes))
				event = Event(self.api,name,location,attendees,organiser,owner,startDate,endDate,isAttending=isAttending)
				self.eventsChanged = True
			
			elif choice == "2":
				name = input("Event name: ") 
				address = input("Event address (NONE if virtual): ")
				if(address.upper()=="NONE"):
					address = "Online"
				location = Location(address)
				attendees = []
				while(True):
					print("Please enter attendee details; enter QUIT to stop")
					attEmail = input("attendee email: ")
					if(attEmail.upper()=="QUIT"): break 
					attendees.append(Attendee(attEmail))
					print("Attendee added!")

				isAttending = input("Are you attending? (Y/N): ") 
				if isAttending == "Y":
					isAttending = True
				elif isAttending == "N":
					isAttending = False
				else:
					raise AssertionError("Enter Y or N for is attending.")

				orgEmail = input("Enter the organiser's email: ") 
				owner = Attendee(orgEmail)
				attendees.append(owner)

				userEmail = input("Enter your email: ") 
				user = Attendee(userEmail)

				startDateStr = input("Event start date (YYYY-MM-DD or DD-MON-YY): ")
				startDateHours = input("Event start date hour (HH): ")
				startDateMinutes = input("Event start date minutes (MM): ")
				startDate = Date(startDateStr,"%s:%s" % (startDateHours,startDateMinutes))
				endDateStr = input("Event end date (YYYY-MM-DD or DD-MON-YY): ")
				endDateHours = input("Event end date hour (HH): ")
				endDateMinutes = input("Event end date minutes (MM): ")
				endDate = Date(endDateStr,"%s:%s" % (endDateHours,endDateMinutes))
				eventId = Event(self.api,name,location,attendees,user,owner,startDate,endDate,isAttending=isAttending).id
				self.eventsChanged = True
				changeOrganiser(self.api,eventId,orgEmail)
			else:
				print("Invalid input! Please try again.")

		except AssertionError as e:
			print(e)
			print("Event creation failed!") 
	
	def deleteEvent(self):
		index = input("please enter an index of an event to delete (0-%d): " % (len(self.eventList)-1))
		if(index.isnumeric()):
			index = int(index)
			if(index>=0 and index<len(self.eventList)):
				result = self.eventList[index].deleteFromCalendar ()
				if(result):
					self.eventsChanged = True
					print("Event deleted!")
				else:
					print("Event failed to delete!")
			else:
				print("No event with that index exists!")
		else:
			print("Index needs to be numeric!") 
		
	def cancelEvent(self):
		index = input("please enter an index of an event to cancel (0-%d): " % (len(self.eventList)-1)) 
		if(index.isnumeric()):
			index = int(index)
			if(index>=0 and index<len(self.eventList)):
				result = self.eventList[index].cancelEvent()
				if(result):
					self.eventsChanged = True
					print("event cancelled!")
				else:
					print("event failed to be cancelled!")
			else:
				print("No event with that index exists!")
		else:
			print("index needs to be numeric!") 
	
	def restoreEvent(self):
		self.viewCancelledEvents() 
		if(len(self.cancelledEventList)==0):
			print("there are no cancelled events!")
			return 
		index = input("please enter an index of a cancelled event to restore (0-%d): " % (len(self.cancelledEventList)-1)) 
		if(index.isnumeric()):
			index = int(index)
			if(index>=0 and index<len(self.cancelledEventList)):
				self.cancelledEventList[index].restoreEvent()
				self.eventsChanged = True
			else:
				print("No event with that index exists!")
		else:
			print("index needs to be numeric!") 

	def importEvent(self):
		file = input("File path to event JSON file (use / as delimiter): ")
		result = importEventFromJSON(self.api,file)
		if result != True:
			print(result)
		else:
			self.eventsChanged = True

	def searchEventByNameKeyWord(self):
		keyword = input("Enter event keyword: ")
		events = searchEvent_by_name_keyword(self.api,keyword)
		self.listEvents(events)

	def searchEventByDate(self):
		eventDate = input("Enter event date (YYYY-MM-DD or DD-MON-YY): ")
		events = searchEvent_by_date(self.api,eventDate)
		self.listEvents(events)

	def navigateEvents(self):
		self.exitNavigation = False
		while (not self.exitNavigation):
			print("Please choose the navigation method: \n"
			"Y: Navigate by year \n"
			"M: Navigate by month \n"
			"D: Navigate by day \n"
			"X: Back to main menu"
			)
			ymd_inp = str(input("Enter choice: ")).upper()
			if ymd_inp == 'Y':
				year_input = str(input("Input Year (YYYY): "))
				self.handleEventsNavigation(year=year_input)
			
			elif ymd_inp == 'M':
				year_input = str(input("Input Year (YYYY): "))
				month_input = str(input("Input Month of the respective year (MM): "))
				self.handleEventsNavigation(year=year_input,month=month_input)

			elif ymd_inp == 'D':
				year_input = str(input("Input Year (YYYY): "))
				month_input = str(input("Input Month of the respective year (MM): "))
				day_input = str(input("Input Day of the respective month (DD): "))
				self.handleEventsNavigation(year=year_input,month=month_input,day=day_input)

			elif ymd_inp == 'X':
				self.exitNavigation = True
			
			else:
				print("Invalid input! Please try again.")

	def handleEventsNavigation(self,year="",month="",day=""):
		exit = False
		currYear = year
		currMonth = month
		currDay = day
		while not exit:
			if currYear and not currMonth and not currDay:
				events = getNavigatedEvents(self.api, year = currYear, month= currMonth,day=currDay)
				if events != False:
					print("-"*20)
					print(f"Events on year {currYear}")
					self.listEvents(events)
					print("-"*20)
					print("N| Next year")
					print("P| Previous year")
					print("E| Exit navigation")
					print("-"*20)
					navChoice = input("Enter choice: ").upper()
					if navChoice == "N":
						currYear,currMonth,currDay = navigateForward(currYear,currMonth,currDay)
					elif navChoice == "P":
						currYear,currMonth,currDay = navigateBackward(currYear,currMonth,currDay)
					elif navChoice == "E":
						exit = True
						self.exitNavigation = True
					else:
						print("Invalid input! Please try again.")
				else:
					print("Please enter year in YY format")
					exit = True
			
			elif currYear and currMonth and not currDay:
				events = getNavigatedEvents(self.api, year = currYear, month= currMonth,day=currDay)
				if events != False:
					print("-"*20)
					print(f"Events on month {currMonth} {currYear}")
					self.listEvents(events)
					print("-"*20)
					print("N| Next month")
					print("P| Previous month")
					print("E| Exit navigation")
					print("-"*20)
					navChoice = input("Enter choice: ").upper()
					if navChoice == "N":
						currYear,currMonth,currDay = navigateForward(currYear,currMonth,currDay)
					elif navChoice == "P":
						currYear,currMonth,currDay = navigateBackward(currYear,currMonth,currDay)
					elif navChoice == "E":
						exit = True
						self.exitNavigation = True
					else:
						print("Invalid input! Please try again.")
				else:
					print("Please enter year and month in YY and MM format respectively")
					exit = True

			elif currYear and currMonth and currDay:
				events = getNavigatedEvents(self.api, year = currYear, month= currMonth,day=currDay)
				if events != False:
					print("-"*20)
					print(f"Events on day {currDay} of month {currMonth} {currYear}")
					self.listEvents(events)
					print("-"*20)
					print("N| Next day")
					print("P| Previous day")
					print("E| Exit navigation")
					print("-"*20)
					navChoice = input("Enter choice: ").upper()
					if navChoice == "N":
						currYear,currMonth,currDay = navigateForward(currYear,currMonth,currDay)
					elif navChoice == "P":
						currYear,currMonth,currDay = navigateBackward(currYear,currMonth,currDay)
					elif navChoice == "E":
						exit = True
						self.exitNavigation = True
					else:
						print("Invalid input! Please try again.")
				else:
					print("Please enter year and month and day in YY and MM and DD format respectively")
					exit = True
			
			else:
				print("Please enter year, month or day in correct format and sequence")
				exit=True

	def listEvents(self,events,isEventObject=False):
		exitView = False
		eventArr = []
		while not exitView:
			i = 1
			print("-"*20)
			for event in events:
				try:
					if not isEventObject:
						eventObj = Event.fromData(self.api,event)
					else:
						eventObj = event
					if eventObj.status == "cancelled":
						currentTime = dt.datetime.now()
						futureEvent = currentTime <= eventObj.startDate.getTime()
						if futureEvent:
							print("%d| %d-%d-%d %s %s" % (i,eventObj.startDate.year,eventObj.startDate.month,eventObj.startDate.day,eventObj.name,"(CANCELED)"))
							eventArr.append(eventObj)
							i += 1
					else:
						print("%d| %d-%d-%d %s" % (i,eventObj.startDate.year,eventObj.startDate.month,eventObj.startDate.day,eventObj.name))
						eventArr.append(eventObj)
						i += 1 
				except:
					pass

			if len(eventArr) >= 1:
				print("-"*20)
				print("I| Interact with event")
				print("O| Exit viewing events")
				choice = input("Enter choice (I/O): ").upper()
				print("-"*20)
				if choice == "I":
					try:
						eventIdx = int(input("Enter the event number according to the list shown: "))
						if 1 <= eventIdx <= len(eventArr):
							self.interactWithEvents(eventArr,eventIdx)
						else:
							print("Event number needs to be within the range of available events")
					except Exception as e:
						print(e)
						print("Event number should be numeric!")
				elif choice == "O":
					exitView = True
				else:
					print("Invalid input! Please try again.")
			else:
				exitView = True

	def interactWithEvents(self,eventArr,eventIdx):
		# every event in eventArr is an event obj
		currEvent = eventArr[eventIdx-1]
		currEventId = currEvent.id
		self.exitInteraction = False
		while (not self.exitInteraction):
			print("-"*20)
			print(f"Please choose your possible interactions with Event {eventIdx}: ")
			print("-"*20)
			print(
			"T: View event details \n"
			"A: Change title \n"
			"S: Change address \n"
			"D: Change description \n"
			"F: Delete event \n"
			"G: Cancel event \n"
			"H: Restore event \n"
			"J: Change event date \n"
			"K: Change organiser \n"
			"L: Add attendee \n"
			"Z: Remove attendee \n"
			"X: Add email reminder \n"
			"C: Add notification reminder \n"
			"V: Export event \n"
			"B: Accept invitation \n"
			"N: Reject invitation \n"
			"M: Back"
			)
			print("-"*20)
			choice = str(input("Enter choice: ")).upper()
			print("-"*20)
			if choice == 'T':
				details = self.getEventDetails(currEvent)
				back = False
				while not back:
					isBack = str(input(details)).upper()
					if isBack == "M":
						back = True
					else:
						print("Enter M to go back. Try again.")
			
			elif choice == 'A':
				newTitle = str(input("Enter new event tile: "))
				changeEventTitle(self.api,currEventId,newTitle)

			elif choice == 'S':
				newAddress = str(input("Enter new event address: "))
				currEvent.setEventAddress(newAddress)

			elif choice == 'D':
				newDescription = str(input("Enter new event description: "))
				changeEventDescription(self.api,currEventId,newDescription)
			
			elif choice == 'F':
				successfulDelete = currEvent.deleteFromCalendar()
				if successfulDelete:
					self.exitInteraction = True
			
			elif choice == 'G':
				currEvent.cancelEvent()
				currEvent.status = "cancelled"
			
			elif choice == 'H':
				currEvent.restoreEvent()
				currEvent.status = "confirmed"
			
			elif choice == 'J':
				newStartDate = str(input("Enter new start date (YYYY-MM-DD or DD-MM-YY): "))
				newStartTime = str(input("Enter new start time (HH:MM): "))
				newEndDate = str(input("Enter new end date (YYYY-MM-DD or DD-MM-YY): "))
				newEndTime = str(input("Enter new end time (HH:MM): "))
				changeEventDate(self.api,currEventId,newStartDate,newStartTime,newEndDate,newEndTime)
			
			elif choice == 'K':
				newOrganiserEmail = str(input("Enter new organiser's email: "))
				changeOrganiser(self.api,currEventId,newOrganiserEmail)
				
			elif choice == 'L':
				newAttendeeEmail = str(input("Enter new attendee's email: "))
				addAttendee(self.api,currEventId,newAttendeeEmail)
			
			elif choice == 'Z':
				targetAttendeeEmail = str(input("Enter the to be removed attendee's email: "))
				removeAttendee(self.api,currEventId,targetAttendeeEmail)
			
			elif choice == 'X':
				try:
					reminderMinutes = int(input("Enter the minutes for email reminder before event starts (0-40320): "))
					currEvent.addEmailReminder(reminderMinutes)
				except:
					print("Minutes must be numeric and between 0 and 40320")
			
			elif choice == 'C':
				try:
					notificationMinutes = int(input("Enter the minutes for notification reminder before event starts (0-40320): "))
					currEvent.addPopupReminder(notificationMinutes)
				except Exception as e:
					print(e)
					print("Minutes must be numeric and between 0 and 40320")

			elif choice == 'V':
				filePath = input("Enter file path to export to (NONE for current directory): ")
				if filePath == "NONE":
					exportEventToJSON(self.api,currEventId)
				else:
					exportEventToJSON(self.api,currEventId,filePath)
			
			elif choice == 'B':
				acceptEventInvite(self.api,currEventId)
			elif choice == 'N':
				rejectEventInvite(self.api,currEventId)
	
			elif choice == 'M':
				self.exitInteraction = True
			else:
				print("Invalid input! Please try again.")

	def getEventDetails(self,currEvent):
		attendees = "\n"
		for i,attendee in enumerate(currEvent.attendees):
			attendees += f"Attendee {i+1}: {attendee.email} \n"
		attendees = "none" if attendees == "\n" else attendees

		emailReminderStr = "\n"
		for j,emailReminderMinutes in enumerate(currEvent.emailNotifMinuteList):
			emailReminderStr += f"Email reminder {j+1}: {emailReminderMinutes} minutes before \n"
		emailReminderStr = "none" if emailReminderStr == "\n" else emailReminderStr

		notificationReminderStr = "\n"
		for k,notificationReminderMinutes in enumerate(currEvent.popupNotifMinuteList):
			notificationReminderStr += f"Notification reminder {k+1}: {notificationReminderMinutes} minutes before \n"
		notificationReminderStr = "none" if notificationReminderStr == "\n" else notificationReminderStr

		details = ""
		details += f"Event name: {currEvent.name}\n"
		details += f"Event location: {currEvent.location.address}\n"
		details += f"Event start date: {str(currEvent.startDate)}\n"
		details += f"Event end date: {str(currEvent.endDate)}\n"
		details += f"Event organiser: {currEvent.organiser.email}\n"
		details += f"Event status: {currEvent.status}\n"
		details += f"Event attendees: {attendees}"
		details += f"Event email reminders: {emailReminderStr}\n"
		details += f"Event notification reminders: {notificationReminderStr}\n"
		details += f"Press M to go back: "
		return details

if __name__ == "__main__":
    try:
        console = App(get_calendar_api())
        console.start()
    except FileNotFoundError as e:
        print(e)




