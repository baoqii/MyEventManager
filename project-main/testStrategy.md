<h1><b> Test Strategy</b></h1>
Due to the high number of different functionalities that MyEventManager has, we decided to split our test suites in a way for each functionality, we would have a test suite. We would also have additional test suites to test the important arguments such as DateTest,TimeTest, EmailTest, LocationTest, as these fields require great amount of validation in MyEventManager. Thus test suites are created to test them comprehensively.
<br><br>

# Test Suite 1: GetAllEventsTest
This test suite tests the get_all_events function in MyEventManager.py which allows the user to view all events that are within 5 years in the past and 5 years in the future. The function is made so that the organizer and attendee can only view events within these 10 years. It takes in an argument which is Google Calendar API.

Basic **line coverage** was used as the test strategy to test this function since it does not contain any conditions. Mocking is used to simulate an API call to Google Calendar, where the mocked object is used to retrieve the event within the 10 years according to the user’s current time. Whether the process of viewing all events is successful will be checked by the test cases before checking if the list of events returned is equal to what is expected. 
<br><br>

# Test Suite 2: GetCancelledEventsTest
This test suite tests the extraction of events that are cancelled from the calendar. In order to ensure that the functionality works correctly, the test data that is provided includes cancelled events, deleted events, and non-cancelled events. This ensures that the test case confirms that only cancelled events are included. Only a single test case is necessary for this test suite as the inputs into the singular test case allows all the possibilities within the event extraction loop to function, thus ensuring **branch coverage**.
# Test Suite 3: LocationTest
This test suite makes use of **branch coverage** in order to affirm that only valid locations can be created without triggering an error. Branch testing ensures that every condition is properly checked and confirmed to work properly. The test suite furthermore confirms whether changing the location of the event works. It does this by checking a valid location change, along with various inputs that could cause problems. It however treats invalid addresses as a single test case in order to avoid redundancy with the previous test cases. 
# Test Suite 4: ImportEventFromAPITest
This test suite ensures that creating the Event class based on the data provided by the google calendar API works appropriately. It makes use of **line coverage** as the process of creating an event from the data is mostly linear, meaning that branch coverage is unlikely to be relevant. 
# Test Suite 5: DeleteEventTest
This test suite tests for deletion to check whether deleting an event works correctly through **branch testing**, which ensures that the conditions that could lead to a successful or unsuccesful delete are conducted correctly. It is necessary to patch the datetime module for this test suite in order to ensure that the current time according to the test suite is constant regardless of the actual current time. Furthermore as only past events can be deleted, boundary value analysis is used to check whether the this condition works correctly.

# Test Suite 6: CancelAndRestoreEventTest
This test suite checks whether the functionality for cancelling and restoring an event works correctly. It uses **branch testing** in order to ensure that conditions for succeeding and failing in cancelling and restoring an event works correctly. Similarly to the deletion test suite, this test suite makes use of patching to ensure that the current time is always the same. Furthermore as only future events can be cancelled, boundary value analysis is used to check whether the this condition works correctly.

# Test Suite 7: DateTest
For testing the validity of date, we created a static method called isDateValid() under Date class. This method basically checks if the inputted time is in the correct format of 'YYYY-MM-DD' or 'DD-MON-YY'. isDateValid() also takes in a optional 'viewing' argument, which is False by default. When viewing is False, dates within year 2050 are valid. When viewing is True, dates that are 5 years from now and 5 years before now, are valid.

In this test suite, we would apply <b>condition/decision coverage</b> on isDateValid() and test the validity of date comprehensively. By using condition/decision coverage, we ensure that each branch is evaluated to both true and false at least once, and each condition in each branch is evaluated to both true and false at least once. By performing condition/decision coverage, we would also achieve maximum <b>line coverage</b>, <b>branch coverage</b> and <b>condition coverage</b> based on the structure of our code. All lines would be executed, each branch and condition would also be tested. We also applied <b>boundary value analysis</b> when deriving our test cases. 
<br><br>

# Test Suite 8: TimeTest
For testing the validity of time, we created a static method called isTimeValid() under Date class. This method basically checks if the inputted time is in the correct format of 'HH:MM'. In this test suite, we would apply <b>condition coverage</b> on isTimeValid() and test the validity of time comprehensively. By performing condition coverage, we would also achieve <b>line coverage</b> and <b>branch coverage</b> based on the structure of our code. Following condition coverage, each three conditions in the two branches of isTimeValid() are made to evaluate to true and false at least once, and thus we were able to create the following test cases:<br><br>
TC1: Time = 23:59" (All conditions true and time in valid HH:MM format)<br>
TC2: Time = "6:00" (Hour's length is not 2 and is not in HH format)<br>
TC3: Time = "24:00" (Hour is not between 0 and 23)<br>
TC4: Time = "gg:00" (Hour is not numeric)<br>
TC5: Time = "06:5" (Minutes' length is not 2 and is not in MM format)<br>
TC6: Time = "06:60" (Minute is not between 0 and 59)<br>
TC7: Time = "16:hi" (Minute is not numeric)<br>
TC8: Time = "23-31" (HH and MM is not separated with colon, :)<br>
TC9: Time = "" (Time is empty and not in HH:MM)<br><br>
By having these test cases, we would achieve <b>maximum line coverage</b>, <b>branch coverage</b> and also <b>condition coverage</b> for testing time. All lines would be executed, each branch and condition would also be tested. In the midst of choosing the values for the test cases, boundary value analysis was also applied to test the edge cases of the time validity.
<br><br>

# Test Suite 9: EmailTest
For testing the validity of email, we created a static method called isEmailValid() under Attendee class. This method basically checks if the inputted email is in the correct format of starting with email initials, followed by a "@" and some email domain, in the end the email would look something like "{emailInitials}@{emailDomain}". As we are using regular expressions for this function, there are no apparent branches, however we can treat the whole regex as one single branch, and each matching regular expression clause as a condition. Thus, in this test suite, we would apply <b>condition coverage</b> on isEmailValid() and test the validity of email comprehensively. By performing condition coverage, we would also achieve <b>line coverage</b> and <b>branch coverage</b> based on the structure of our code. Following condition coverage, each condition is made to evaluate to true and false at least once, and thus we were able to create the following test cases:<br>

TC1: Email = georgetan615@gmail.com" (All conditions true and email in valid format)<br>
TC2: Email = "georgetangmail.com" (Email is missing a '@')<br>
TC3: Email = "georgetan615@" (Email is missing email domain)<br>
TC4: Email = "@gmail.com" (Email is missing email initials)<br>
TC5: Email = "" (Email is empty)<br>

By having these test cases, we would achieve <b>maximum line coverage</b>, <b>branch coverage</b> and also <b>condition coverage</b> for testing email.  All lines would be executed, each branch and condition would also be tested. 
<br>

# Test Suite 10: NotifTest 
This test suite is intended to confirm whether notifications for an event are added appropriately to ensure that the notifications are stored within the class, and that the code to check whether an event should be notified works correctly. This is done through **branch testing** as it would affirm that conditions are met correctly, thus reducing the likelihood of any unexpected bugs. Another check that is conducted is checking that the minutes before the notifications are bounded correctly, thus **boundary value analysis** is used to check for this.

# Test Suite 11: StartDateTimeBeforeEndDateTimeTest
For testing if a given startDate and startTime is before a given endDate and endTime, we created a static method called isStartDateTimeBeforeEndDateTime() under Date class. This method basically checks if the inputted startDate and startTime are before the end date and end time. The dates and times inputted into this function are also assumed to be valid already. In this test suite, we would apply <b>condition coverage</b> on isStartDateTimeBeforeEndDateTime() and test comprehensively if start date and time are before end date and time. By performing condition coverage, we would also achieve <b>line coverage</b> and <b>branch coverage</b> based on the structure of our code. Following condition coverage, each conditions in the four branches of isStartDateTimeBeforeEndDateTime() are made to evaluate to true and false at least once and thus we were able to create the following test cases:<br><br>


TC1: StartDate="2022-11-12" StartTime="11:12" EndDate="2022-11-12" EndTime="11:12" (both start and end's year,month,day,hour are same, and startMinute is before endMinute)<br>
TC2: StartDate="2022-11-12" StartTime="11:13" EndDate="2022-11-12" EndTime="11:12" (both start and end's year,month,day,hour are same, but startMinute is after endMinute)<br>
TC3: StartDate="2022-11-12" StartTime="11:13" EndDate="2022-11-12" EndTime="12:12" (both start and end's year,month,day are same, but startHour is before endHour)<br>
TC4: StartDate="2022-11-12" StartTime="13:13" EndDate="2022-11-12" EndTime="12:12" (both start and end's year,month,day are same, but startHour is after endHour)<br>
TC5: StartDate="2022-11-13" StartTime="05:12" EndDate="2022-11-14" EndTime="08:32" (both start and end's year,month are same, but startDay is before endDay)<br>
TC6: StartDate="2022-11-15" StartTime="05:12" EndDate="2022-11-14" EndTime="08:32" (both start and end's year,month are same, but startDay is after endDay)<br>
TC7: StartDate="2022-11-13" StartTime="05:12" EndDate="2022-12-14" EndTime="08:32" (both start and end's year are same, but startMonth is before endMonth)<br>
TC8: StartDate="2022-11-15" StartTime="05:12" EndDate="2022-10-14" EndTime="08:32" (both start and end's year are same, but startMonth is after endMonth)<br>
TC9: StartDate="2022-11-13" StartTime="05:12" EndDate="2023-11-14" EndTime="08:32" (start year is before end year)<br>
TC10: StartDate="2022-11-13" StartTime="05:12" EndDate="2021-11-14" EndTime="08:32" (start year is after end year)<br><br>

By having these test cases, we would achieve <b>maximum line coverage</b>, <b>branch coverage</b> and also <b>condition coverage</b> for testing if start date and time are before end date and time. All lines would be executed, each branch and condition would also be tested. In the midst of choosing the values for the test cases, <b>boundary value analysis</b> was also applied to test the edge cases.
<br><br>

# Test Suite 12: ChangeEventDateTest 
This test suite is designed to check whether the event date can be changed correctly using **branch coverage**. The tested code checks whether the user is allowed to modify the event's date, along with whether the date is valid, so the test cases accordingly checks if the validations work correctly.
# Test Suite 13: ChangeOrganiserTest
In this test suite, we will be testing for the changeOrganiser() function in MyEventManager.py, which allows organisers to change the organiser to another person. The changeOrganiser() function takes in the google calendar API object, the new organiser's email and also the eventId of the event that would be updated. The input eventId would allow us to directly access and update that event's organiser as specified in the Google Calendar API reference document.
<br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. Our two branches involved checking if the current user is an organiser and also checking if the input new organiser email is of a valid format. These checks are done using the static methods checkIsOrganiser() and isEmailValid(), which basically returns a boolean that signifies the validity of that arguement. By performing branch and condition coverage, we are also able to achieve maximum <b>line coverage</b>. Mocking is also used to mock the API object, where the mocked API object would be used to change the organiser of the event after the checkIsOrganiser() and isEmailValid() checks. If the organiser was not successfuly changed, any errors or Exceptions would also be caught, thus leading the changeOrganiser() function return False. Our test cases would just check if the change organiser process was successful or not depending on our input.
<br><br>

# Test Suite 14: RemoveAttendeeTest
In this test suite, we will be testing for the removeAttendee() function in MyEventManager.py, which allows organisers to remove a certain attendee. The removeAttendee() function takes in the google calendar API object, the to be removed attendee's email and also the eventId of the event that would be updated. The input eventId would allow us to directly access and remove the attendee in that event as specified in the Google Calendar API reference document.
<br><br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. Our branches involved checking if the current user is an organiser, checking if the input attendee email is of a valid format, and also checking if the number of attendees changed upon removing the attendee from that event. These checks are involved using the static methods checkIsOrganiser() and isEmailValid(), which basically returns a boolean that signifies the validity of that arguement. By achieving maximum branch and condition coverage, we also achieve maximum <b>line coverage</b>. Mocking is also used to mock the API object, where the mocked API object would be used to remove the attendee of the event after the checkIsOrganiser() and isEmailValid() checks. After the removal of attendee, we would also check if the number of attendees did decrement by 1. If the attendee was not successfully removed, any errors or Exceptions would also be caught, thus leading the removeAttendee() function return False. Our test cases would just check if the remove attendee process was successful and also did the number of attendees change. For cases where the number of attendees did not change after removal, this means that the given email user is not an attendee in the event, thus the removeAttendee() function would also return False.
<br><br>

# Test Suite 15: AddAttendeeTest 
In this test suite, we will be testing for the addAttendee() function in MyEventManager.py, which allows organisers to add a certain attendee. The addAttendee() function takes in the google calendar API object, the to be added attendee's email and also the eventId of the event that would be updated. The input eventId would allow us to directly access and add the attendee in that event as specified in the Google Calendar API reference document.
<br><br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. Our branches involved checking if the current user is an organiser, checking if the input attendee email is of a valid format, checking if the number of attendees in the event has already reached our maximum capacity (20 attendees) and also checking if the number of attendees changed upon adding the attendee from that event. These checks are involve using the static methods checkIsOrganiser() and isEmailValid(), which basically returns a boolean that signifies the validity of that arguement. <b>Boundary value analysis</b> was also applied when testing the boundaries of the maximum capacity of attendees in an event. By achieving maximum branch and condition coverage, we also achieve maximum <b>line coverage</b>. Mocking is also used to mock the API object, where the mocked API object would be used to add the attendee of the event after the checkIsOrganiser() and isEmailValid() checks and also if the event has not yet reached maximum capacity. After the addition of attendee, we would also check if the number of attendees did increment by 1. If the attendee was not successfully added, any errors or Exceptions would also be caught, thus leading the addAttendee() function return False. Our test cases would just check if the add attendee process was successful and also did the number of attendees change. For cases where the number of attendees did not change after addition, this means that the given email user is already an attendee in the event, thus the addAttendee() function would also return False.
<br><br>

# Test Suite 16: EventCreationAttendeeTest    
This test suite ensures that the maximum attendee limit is respected using **branch coverage** and **boundary value analysis** to check the boundary of 20 attendees. The test suite tests the on-point and the off-point, so only 2 tests are required for this test suite.
# Test Suite 17: ImportJSONEventTest
In this test suite, we will be testing for the importEventFromJSON() function in MyEventManager.py, which allows users to create/import events from a file with JSON syntax. The importEventFromJSON() function takes in the Google calendar API object, and the filepath of the JSON syntax file that contains the event details that would be used to import the event. Besides, we mention json syntax because as long as the file's contents is in JSON syntax, then the event can be imported, it does not matter if the file type is Python or JSON file.<br>

<b>Condition and branch coverage</b> were used to make sure each condition and branch are tested. In our case, the branches are exception catches such as catching FileNotFoundError (when user give invalid file paths), JSONDecodeError (when the file specified by user is not in proper json syntax) and HttpError (when the file's contents are not in valid format to create the event). By using condition and branch coverage, we ensure that each above catches would be executed at least once and when none of them executes, we successfully imported the event. Mocking is also used to mock the API object, where the mocked API object would be used to create the event using the file's contents. Our test cases would just check if the import of event process was successful and upon a successful event creation, the event link would also be generated. By achieving maximum branch coverage, we also achieve maximum <b>line coverage</b> in our case.
<br><br>

# Test Suite 18: ExportEventJSONTest 
In this test suite, we will be testing for the exportEventToJSON() function in MyEventManager.py, which allows users to export an event from Google Calendar to a JSON file. The exportEventToJSON() function takes in the Google calendar API object, eventId, and the location/file path of where the event by the specified by the eventId should be exported to. 
<br><br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. In our case, the branches are the exception catch for FileNotFoundError (when user gives a file path that does not exist) and also checks for if the user has inputted a file path or not, if the user did not input a file path, the event would be exported to the current directory. By using condition and branch coverage, we ensure that both of the branch's decision would be executed at least once, and to do this each condition would need to be evaluated to true and false at least once. Mocking is also used to mock the API object, where the mocked API object would be used to get the event using the eventId specified. Our test cases would just check if the export of event process was successful and upon a successful event creation, the test case would check if the exported event file exists at the directory specified. By achieving maximum branch coverage, we also achieve maximum <b>line coverage</b> in our case.
<br><br>

# Test Suite 19: ChangeEventTitleTest
In this test suite, we will be testing for the changeEventTitle() function in MyEventManager.py, which allows users to change an event's title. The changeEventTitle() function takes in the Google calendar API object, eventId, and the new title of the event that should be changed into. 
<br><br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. In our case, the branches are just checking if the user is organiser and if the new title is empty. By using condition and branch coverage, we ensure that both of the branch's decision would be executed at least once, and to do this each condition would need to be evaluated to true and false at least once. Mocking is also used to mock the API object, where the mocked API object would be used to get the event using the eventId specified. Our test cases would just check if the change of event title process was successful and upon a successful event title update, the test case would check if the updated event's title is equal to the input new title. By achieving maximum branch coverage, we also achieve maximum <b>line coverage</b> in our case.
<br><br>

# Test Suite 20: ChangeEventDescriptionTest 
In this test suite, we will be testing for the changeEventDescription() function in MyEventManager.py, which allows users to change an event's description. The changeEventDescription() function takes in the Google calendar API object, eventId, and the new description of the event that should be changed into. 
<br><br>
<b>Branch coverage</b> was used to make sure each branch is tested. In our case, each decision node also only has one condition, thus <b>condition coverage</b> would also be applied as each condition in those decision nodes would be true or false at least once. In our case, the branches are just checking if the user is organiser and if the new description is empty. By using condition and branch coverage, we ensure that both of the branch's decision would be executed at least once, and to do this each condition would need to be evaluated to true and false at least once. Mocking is also used to mock the API object, where the mocked API object would be used to get the event using the eventId specified. Our test cases would just check if the change of event description process was successful and upon a successful event description update, the test case would check if the updated event's description is equal to the input new description. By achieving maximum branch coverage, we also achieve maximum <b>line coverage</b> in our case.
<br><br>

# Test Suite 21: TestGetNavigatedEvents 
In this test suite, we will be testing for the getNavigatedEvents() function in MyEventManager.py, which allows users to get a list of events on a specific,year,month,day, depending on the combination of year month day the user has input. This function is needed for us to make the navigation feature in our MyEventManagerApp work. The getNavigatedEvents() function takes in the Google calendar API object, and the year,month,or day. If the user wants to view all events on a certain year, then the user only has to specify the input year. If the user wants to view all events on a certain year's month, then the user only has to specify the input year and month. If the user wants to view all events on a certain year's month's day, then the user only has to specify the input year, month and day. Any other combinations of inputs between year month and day would be rejected. The unspecified arguments would be kept as an empty string.
<br><br>
<b>Condition/Decision coverage</b> was used to make sure each condition in a branch is made to evaluate to both true and false at least once. Each branch is also made to evaluate to both true and false at least once. This strategy was chosen as we have multiple conditions in a single branch to test the different combinations of input year, month, day. By using condition/decision coverage, 
we also can achieve maximum <b>line coverage</b> and <b>branch coverage</b> for our case. Mocking is also used to mock the API object, where the mocked API object would be used to get the event using the eventId specified. Our test cases would just check if the process of getting the navigated events was successful and upon the successful process, the test case would check if the list of events obtained is what is expected. <br><br>
By using decision/condition coverage along with <b>boundary value analysis</b>, we are able to derive the below test cases with the selected values:<br>

<b>First branch (Evaluate to True)</b><br>
TC1: Year = "2023", Month = "", Day = "" (All conditions evaluate to True, valid year format, successful getNavigatedEvents)<br>
TC2: Year = "202", Month = "", Day = "" (All conditions evaluate to True, invalid year format, unsuccessful getNavigatedEvents)<br>

<b>First branch (FALSE)</b><br>
TC3: Year = "", Month = "11", Day = "12" (All conditions evaluate to False)<br>

<b>Second branch (TRUE)</b><br>
TC4: Year = "2023", Month = "11", Day = "" (All conditions evaluate to True, valid year and month format, successful getNavigatedEvents)<br>
TC5: Year = "2021", Month = "13", Day = "" (All conditions evaluate to True, month not between 1 and 12, unsuccessful getNavigatedEvents )<br>

<b>Second branch (FALSE)</b><br>
TC6: Year = "", Month = "", Day = "12" (All conditions evaluate to False)<br>


<b>Third branch (TRUE)</b><br>
TC7: Year = "2023", Month = "12", Day = "31" (All conditions evaluate to True, valid year, month and day format, successful getNavigatedEvents)<br>
TC8: Year = "2021", Month = "11", Day = "32" (All conditions evaluate to True, day not between 1 and 31, unsuccessful getNavigatedEvents )<br>

<b>Third branch (FALSE)</b><br>
TC9: Year = "", Month = "", Day = "" (All conditions evaluate to False)<br>

<br><br>


# Test Suite 22: TestNavigateForward 
This test suite tests the navigateForward function in MyEventManager.py which allows the user to navigate to the next year or month or day depending on the combination of year, month, day the user has provided. The function takes year, month and day as arguments and if no arguments are given it will return False. If only year is given it will return the next year. If both year and month are given it will return the next month. If all three are given it will return the next day. These return arguments will be passed to function getNavigatedEvents to retrieve the list of events.

In order for each condition in a branch to evaluate to both true and false at least one, **condition/decision coverage** was used. This is because the different conditions of input year, month, and day can be tested with the multiple conditions in a single branch. Therefore, maximum **line coverage and branch coverage** can be achieved. The output of the function will be checked by the test case to see if the correct date of the next year or month or day is shown as specified. It will also check whether the date is similar to what is expected. 

The test cases can be derived with the selected values using **condition/decision coverage** along with **boundary value analysis**.<br>

<b>First branch (TRUE)</b><br>
TC1: Year = "2022", Month = "", Day = "" (All conditions evaluated to True, navigated to Year 2023, successful navigateForward)<br>

<b>First branch (FALSE)</b><br>
TC2: Year = "", Month = "11", Day = "12" (All conditions evaluated to False)

<b>Second branch (TRUE)</b><br>
TC3: Year = "2022", Month = "11", Day = "" (All conditions evaluated to True, navigated to December of 2022, successful navigateForward)<br>

TC4: Year = "2022", Month = "13", Day = "" (All conditions evaluated to True, month is greater than 12, navigated to January of 2023, successful navigateForward)<br>

<b>Second branch (FALSE)</b><br>
TC5: Year = "", Month = "", Day = "12" (All conditions evaluated to False)

<b>Third branch (TRUE)</b><br>
TC6: Year = "2022", Month = "11", Day = "12" (All conditions evaluated to True, day is not less than 31, navigated to 13th of November of 2022, successful navigateForward)<br>

TC7: Year = "2022", Month = "11", Day = "32" (All conditions evaluated to True, day is greater than 31, month is not December, navigated to december 1st of 2022, successful navigateForward)<br>

TC8: Year = "2022", Month = "12", Day = "32" (All conditions evaluated to True, day is greater than 31, month is December, navigated to january 1st of 2023, successful navigateForward)<br>

<b>Third branch (FALSE)</b><br>
TC9: Year = "", Month = "", Day = "" (All conditions evaluated to False)
<br><br>

# Test Suite 23: TestNavigateBackward 
Similar to TestNavigateForward, this test suite tests the navigateBackward function in MyEventManager.py, though it allows the user to navigate to the previous year or month or day depending on the combination of year, month, day the user has provided. The function takes year, month and day as arguments and if no arguments are given it will return False. If only year is given it will return the previous year. If both year and month are given it will return the previous month. If all three are given it will return the previous day. These return arguments will be passed to function getNavigatedEvents to retrieve the list of events. <br><br>

In order for each condition in a branch to evaluate to both true and false at least one, **condition/decision coverage** was used. This is because the different conditions of input year, month, and day can be tested with the multiple conditions in a single branch. Therefore, maximum **line coverage and branch coverage** can be achieved. The output of the function will be checked by the test case to see if the correct date of the previous year or month or day is shown as specified. It will also check whether the date is similar to what is expected. 
<br><br>

The test cases can be derived with the selected values using **condition/decision coverage** along with **boundary value analysis**.

First branch (Evaluate to True)
TC1: Year = "2022", Month = "", Day = "" (All conditions evaluated to True, navigate to Year 2021, successful navigateBackward)

<b>Second branch (TRUE)</b><br>

TC3: Year = "2022", Month = "2", Day = "" (All conditions evaluated to True, navigated to January of 2022, successful navigateBackward)<br>

TC4: Year = "2022", Month = "0", Day = "" (All conditions evaluated to True, month is lesser than 1, navigated to January of 2021, successful navigateBackward)<br>

<b>Second branch (FALSE)</b><br>
TC5: Year = "", Month = "", Day = "13" (All conditions evaluated to False)<br>

<b>Third branch (TRUE)</b><br>
TC6: Year = "2022", Month = "2", Day = "13" (All conditions evaluated to True, day is not less than 1, navigated to 12th of February of 2022, successful navigateBackward)<br>

TC7: Year = "2022", Month = "2", Day = "0" (All conditions evaluated to True, day is lesser than 1, month is not January, navigated to January 31st of 2022, successful navigateBackward)<br>

TC8: Year = "2022", Month = "1", Day = "0" (All conditions evaluated to True, day is lesser than 1, month is January, navigated to December 31st of 2021, successful navigateBackward)<br>

<b>Third branch (FALSE)</b><br>
TC9: Year = "", Month = "", Day = "" (All conditions evaluated to False)<br>
<br><br>

# Test Suite 24: AcceptEventInviteTest 
This test suite tests the acceptEventInvite function in MyEventManager.py which allows the user to accept the invitation to the event. This action is only allowed for attendees of the specified event. This function returns an updatedEvent. The acceptEventInvite() function takes in the Google Calendar API object and EventId.

By using **branch coverage**, it is ensured that each branch is tested. As each decision node in our case only has one condition, **condition coverage** is applied as each condition would be true or false at least once. In this case, the branches are checking whether the user is an attendee. If it is an attendee, the email of the attendee will be obtained and the responseStatus of that attendee will be changed to ‘accepted’. Both of the branches’ decisions would be executed at least once by using **condition and branch coverage**, and each condition would need to be evaluated to true and false at least once. Mocking is used to simulate an API call to Google Calendar, where the mocked object is used to get the event using the eventId specified. The test case would check if the change of responseStatus to ‘accepted’ was successful and if successful, the test case would check if the updated event are the same as  what is expected. 
<br><br>

# Test Suite 25: RejectEventInviteTest 
Similar to acceptEventInviteTest, this test suite tests the rejectEventInvite function in MyEventManager.py, though it allows the user to reject the invitation to the event. This action is only allowed for attendees of the specified event. This function returns an updatedEvent. The rejectEventInvite() function takes in the Google Calendar API object and EventId.

By using **branch coverage**, it is ensured that each branch is tested. As each decision node in our case only has one condition, **condition coverage** would also be applied as each condition would be true or false at least once. In this case, the branches are checking whether the user is an attendee. If it is an attendee, the email of the attendee will be obtained and the responseStatus of that attendee will be changed to ‘rejected’.

Both of the branches’ decisions would be executed at least once by using **condition and branch coverage**, and each condition would need to be evaluated to true and false at least once. Mocking is used to simulate an API call to Google Calendar, where the mocked object is used to get the event using the eventId specified. The test case would check if the change of responseStatus to ‘rejected’ was successful and if successful, the test case would check if the updated event are the same as what is expected. 
<br><br>

# Test Suite 26: SearchEventByDateTest 
This test suite tests the searchEvent_by_date function in MyEventManager.py which allows the user to search for events in the user's primary calendar that matches the event date specified and returns them by making use of the 'timeMin' and 'timeMax' parameter. This function takes in Google Calendar API, and event_date which is a string representing the date the user wants to search for in YYYY-MM-DD or DD-MON-YY format. The specified event_date is passed into isDateValid() function from Date Class to check whether it is indeed a valid date before searching for events according to this event_date. It returns a list of events that match the specified date, if there are no matching events an empty list will be returned.

To make sure that each branch is tested, **branch coverage** was used. In this case, each decision node only has a condition, hence **condition coverage** would be applied as each condition in those decision nodes would be true or false at least once.
For this test suite, the branches are just checking if the date provided is valid and invalid. By using **condition and branch coverage**, this branch's decision will be executed at least once, in order to do so each condition should be evaluated at least once. Mocking is used to simulate an API call to Google Calendar, where the mocked object is used to search the event with the event_date specified. Whether the process of obtaining the searched events is successful will be checked by the test cases before checking if the list of events returned is equal to what is expected.

There are 2 test cases in this test suite where:
TC1: event_date = “”<br>
Test whether the function returns False given an invalid date<br>

TC2: event_date = “2022-12-21”<br>
Test whether the function returns list of events that match the valid date<br>
<br><br>

# Test Suite 27: SearchEventByNameKeywordTest
This test suite tests the searchEvent_by_name_keyword function in MyEventManager.py which allows the user to search for events in the user's primary calendar that matches event name or contains a keyword and returns them by making use of the 'q' parameter. This function takes in Google Calendar API, and a query which is a string representing the event name or keyword the user wants to search for. It returns a list of events that match the query, if there are no matching events an empty list will be returned.

Basic **line coverage** was used as the test strategy to test this function since it does not contain any conditions. Mocking is used to simulate an API call to Google Calendar, where the mocked object is used to search the event with the query specified. Whether the process of obtaining the searched events is successful will be checked by the test cases before checking if the list of events returned is equal to what is expected. 
<br><br>

There are 3 test cases in this test suite where:<br>
TC1: query = "UPPERCASE"<br>
Test whether the function returns events even if the input query is **uppercase** letters<br>

TC2: query = "Add title"<br>
Tests whether the function returns events that matches the **event name** given a query<br>

TC3: query = "keyword"<br>
Tests whether the function returns events that matches the **event keyword** given a query 
<br><br>

