import requests
import MySQLdb
from bs4 import BeautifulSoup

import config as cfg

#db connections
HOST = cfg.database['host']
USERNAME = cfg.database['username']
PASSWORD = cfg.database['password']
DATABASE = cfg.database['database']

print(HOST)
print(USERNAME)
print(PASSWORD)
print(DATABASE)

scraped_url = "https://howpcrules.com/sample-page-for-web-scraping/"

#load html data
html_text = requests.get(scraped_url)

#parse data
soup = BeautifulSoup(html_text.text, "html.parser")

name_of_class = soup.h3.text.strip()

#FOR TABLE 1
basic_table_data = soup.find("table", {"summary": "Basic data for the event"})
basic_data_cells = basic_table_data.findAll('td')

# print(basic_data_cells)

#getting data from different table values
type_of_course = basic_data_cells[0].text.strip()
lecturer = basic_data_cells[1].text.strip()
number_id = basic_data_cells[2].text.strip()
short_text = basic_data_cells[3].text.strip()
choice_term = basic_data_cells[4].text.strip()
hours_per_week_in_term = basic_data_cells[5].text.strip()
expected_num_of_participants = basic_data_cells[6].text.strip()
maximum_participants = basic_data_cells[7].text.strip()
assignment = basic_data_cells[8].text.strip()
lecture_id = basic_data_cells[9].text.strip()
credit_points = basic_data_cells[10].text.strip()
hyperlink = basic_data_cells[11].text.strip()
language = basic_data_cells[12].text.strip()

db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "INSERT INTO classes(name_of_class, type_of_course, lecturer, number, short_text, choice_term, hours_per_week_in_term, expected_num_of_participants, maximum_participants, assignment, lecture_id, credit_points, hyperlink, language, created_at) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(name_of_class, type_of_course, lecturer, number_id, short_text, choice_term, hours_per_week_in_term, expected_num_of_participants, maximum_participants, assignment, lecture_id, credit_points, hyperlink, language, 'NOW()')

try:
 # Execute the SQL command
 cursor.execute(sql)
 # Commit your changes in the database
 db.commit()
except:
 # Rollback in case there is any error
 db.rollback()
 #get the just inserted class id
sql = "SELECT LAST_INSERT_ID()"
try:
 # Execute the SQL command
 cursor.execute(sql)
 # Get the result
 result = cursor.fetchone()
 # Set the class id to the just inserted class
 class_id = result[0]
except:
 # Rollback in case there is any error
 db.rollback()
 # disconnect from server
 db.close()
 # on error set the class_id to -1
 class_id = -1

#FOR TABLE 2
dates_tables = soup.findAll("table", {"summary": "Overview of all event dates"})


for table in dates_tables:
	for rows in table.select('tr'):
		cells = rows.findAll('td')
		if len(cells) > 0:
			duration = cells[0].text.split("to")
			start_date = duration[0]
			end_date = duration[1].strip()
			day = cells[1].text.strip()
			time = cells[2].text.split("to")
			start_time = time[0].strip()
			end_time = time[1].strip()
			frequency = cells[3].text.strip()
			room = cells[4].text.strip()
			lecturer_for_date = cells[5].text.strip()
			status = cells[6].text.strip()
			remarks = cells[7].text.strip()
			cancelled_on = cells[8].text.strip()
			max_participants = cells[9].text.strip()

			#Save event data to database
			# Open database connection
			db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
			# prepare a cursor object using cursor() method
			cursor = db.cursor()
			# Prepare SQL query to INSERT a record into the database.
			sql = "INSERT INTO events(class_id, start_date, end_date, day, start_time, end_time, frequency, room, lecturer_for_date, status, remarks, cancelled_on, max_participants, created_at) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(class_id, start_date, end_date, day, start_time, end_time, frequency, room, lecturer_for_date, status, remarks, cancelled_on, max_participants, 'NOW()')
			try:
			 cursor.execute(sql)
			 db.commit()
			except:
			 db.rollback()
			 db.close()