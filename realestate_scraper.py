#--------------------------------------
#Importing modules
import requests
from bs4 import BeautifulSoup
import time
import xlsxwriter
import pandas as pd
#--------------------------------------


#--------------------------------------
#Scraping functions
def url_creator(pages_amount):
    for x in range(1,(pages_amount+1)):
        urls.append(p_url.format(x))

def page_scraping(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    persons = soup.find_all('div',class_="rui-row")
    number = (urls.index(url)*10)
    for item in persons:
        number +=1
        name = item.find('h3').text
        phone_parrent = item.find('div',class_ = "ao-info-c1")
        phone = phone_parrent.find('div',class_ = "ao-phone", id="ao-phone").text
        person = (name,phone,number)
        results.append(person)
#--------------------------------------


#--------------------------------------
#Saving function
def saving_xlsx(check):
    workbook = xlsxwriter.Workbook('records.xlsx') 
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', "Full Name")
    worksheet.write('B1', "Phone Number")
    count = 0  
    n = 2   
    for record in records:
        worksheet.write(f'A{n}', record[0])
        worksheet.write(f'B{n}', record[1])
        n += 1
        count += 1

    workbook.close()
    if check == "check":
        print("EXCEL FILE")
        df = pd.read_excel("records.xlsx")
        pd.set_option('max_rows',5000)
        print(df)
#--------------------------------------


#--------------------------------------
#Sort functions
def sort_function(x):
        return int(x[2])

def sort_function_parrent():
    results.sort(key=sort_function)
    for item in results:
        record = (item[0],item[1])
        records.append(record)
#--------------------------------------


#--------------------------------------
def main_function(pages = 0, check = "check"):
    start = time.time()
    
    #Declaring variables
    global urls
    global results
    global records
    global p_url
    urls = []
    results = []
    records = []
    p_url = "https://realestate.sabor.com/AgentSearch/Results.aspx?SearchType=agent&FirstName=&LastName=&OfficeName=&Address=&City=&State=&Country=-32768&Zip=&Languages=&Titles=&Specialties=&Accreditations=&Areas=&rpp=10&page={}&SortOrder="

    #Creating urls for each page
    url_creator(pages)

    #Scraping
    print("Scraping")
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(page_scraping,urls)

    #Sorting and saving
    sort_function_parrent()
    saving_xlsx(check)

    end = time.time()
    total = time.gmtime(end-start)
    total_time = time.strftime("%M:%S",total) 
    print("Total: ",total_time)
#--------------------------------------


main_function(pages = 1600, check = "check")


#------INSTRUCTIONS-------
#Chose amount of pages to scrap(10 results per page) first. 
#You can set a little more pages than you need,there will be no copies of the results.
#Set "check = None" if you dont want to check results.
#Should look like: main_function(pages = 1405, check = None)

#P.S the program will take ~ 6 minutes to complete for 1500 pages.



