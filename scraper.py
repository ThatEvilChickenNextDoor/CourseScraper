from bs4 import BeautifulSoup

with open('csciCoursePage.html') as page:
    soup = BeautifulSoup(page, 'lxml')
    
table = soup.table
table_rows = table.find_all('tr')

'''
courses = list()
for row in table_rows:
    contents = row.find_all('td')
    course = [i.text.strip() for i in contents]
    if len(course) > 0:
        courses.append(course)
'''

courses = [[i.text.strip() for i in row.find_all('td')] for row in table_rows][1:]

for course in courses:
    print(course)
