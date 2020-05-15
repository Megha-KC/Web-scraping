from bs4 import BeautifulSoup
import requests
from csv import writer

url = 'https://www.meetup.com/find/?allMeetups=true&keywords=React&radius=25&userFreeform=New+York%2C+New+York%2C+USA&eventFilter=all'
response = requests.get(url)
data = response.text

soup = BeautifulSoup(data, 'html.parser')
events = soup.find_all('a', {'class':'display-none'})
with open('events.csv', 'w') as csv_file:
	csv_writer = writer(csv_file)
	headers = ['Title', 'Link', 'Description', 'Date & Time', 'Cost', 'Location']
	csv_writer.writerow(headers)

	for event in events:
		link = event.get('href')
		event_response = requests.get(link)
		event_data = event_response.text
		event_soup = BeautifulSoup(event_data, 'html.parser')
		members = event_soup.find('a',{'class':'groupHomeHeaderInfo-memberLink'}).text
		mem_int = int(''.join(unicode.strip(members).split(' ')[0].split(',')))
		# print 'Members: ',mem_int

		if mem_int > 500:
			# 1. Title of the event
			title = event.text
			print 'Title: ',title

			# 2. Link to the event		
			print 'Link: ',link

			# 3. Description of the event
			event_para = event_soup.find('p', {'class':'group-description'})
			event_description = event_para.findNext('p').text
			print 'Event description: ', event_description

			# 4. Time and date of the event
			time_exist = event_soup.find('time')
			time = time_exist.text if time_exist else 'Not specified'
			print 'Date & time: ',time

			# 5. Cost of the event
			cost_exist = event_soup.find(attrs={'data-e2e': 'event-footer--price-label'})
			cost = cost.contents[0].text if cost_exist else 'FREE'
			print 'Cost:', cost
			# 6. Location of the event
			location = event_soup.find('ul',{'class':'organizer-city'}).text
			print 'Location: ',location
			csv_writer.writerow([title.encode("utf-8"), link.encode("utf-8"), event_description.encode("utf-8"), time.encode("utf-8"), cost.encode("utf-8"), location.encode("utf-8")])
			print '\n----------------------------------------------------'





