import requests 
from bs4 import BeautifulSoup 
import csv
from itertools import zip_longest

# Start global Variables
jobTitlesList = []
companyNamesList = []
companyLocationsList = []
jobSkillsList = []
postedList = []
links = []
salaries=[]
jobRequeirments = []
pageNumber = 0
jobRequeirmentcounter = 1
# End global Variables


while (1) :
    myUrl = f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={pageNumber}" #setting the page number as a varible to access all pages automaticly using while loop
    try:
        result = requests.get(myUrl) #get the page from the server (it depends on the connection speed & the server response time)
    except: 
        print("server side problem occured")
    src = result.content #get the entire HTML code from the page 
    soup = BeautifulSoup(src , "lxml") #convert the HTML code into (BeautifulSoup) obj
    jobTitles = soup.find_all("h2" , {"class" : "css-m604qf"}) #getting the Jobs Title by tags and its classes (python code)
    companyNames = soup.find_all("a" , {"class" : "css-17s97q8"})
    companyLocations = soup.find_all("span" , {"class" : "css-5wys0k"})
    jobSkills = soup.select('.css-y4udm8 > div:nth-child(2)') #getting the Jobs Skills by tags and its classes (css code) 
    jobsfound = int (soup.find ('strong').text)
    Posted = soup.select ('.css-d7j1kk > div:first-of-type')
    link = soup.select('.css-m604qf>a') # getting the link for every job 
    for i in link :
        temptext = "https://wuzzuf.net"+ i['href'] #normalizing the URL to be valid
        links.append(temptext) #groubing all links in a list

    print (f"Getting the Jobs From page number {pageNumber + 1}") #for console monitoring
    pageNumber+=1

    for i in range(len(jobTitles)): #converting all HTML codes saved above into meaningful texts
        jobTitlesList.append(jobTitles[i].text)
        companyNamesList.append(companyNames[i].text)
        jobSkillsList.append(jobSkills[i].text)
        companyLocationsList.append(companyLocations[i].text)
        postedList.append(Posted[i].text)

    if(pageNumber > jobsfound // 15): #evry page has 15 jobs inside (limit "depends on the number of pages" to break the infinite while loop)
        print("All Jobs have been collected")
        break

print(f"{jobsfound} jobs Founded") #for console monitoring
print("getting all Requeirments for each Job has been started ... ")
for lnk in links : #after we collected the main info about each job .. it's time to click on each job link's to get the full discription (like : job Requeirments , salaries , features)
    try:
        result = requests.get(lnk)
    except: 
        print("server side problem occured")
    src = result.content
    soup = BeautifulSoup(src , "lxml")
    jobRequeirmentLI = soup.select('.css-1t5f0fr > ul > li')
    temp = ""
    for i in jobRequeirmentLI:
        temp += i.text + " | "
    jobRequeirments.append(temp[:-2])
    print ("Loading Requeirments for job number : " , jobRequeirmentcounter)
    jobRequeirmentcounter+=1

FileList = [jobTitlesList , postedList ,companyNamesList , companyLocationsList , jobSkillsList ,jobRequeirments, links] #two dimension array which is not ready to be written on csv file
transposed = zip_longest(*FileList) # normalizing the array (example : pairing each first element form the nested arrays togather and save it into array . the first array(row on csv file) will be ["python developer" , "2 days ago" , "microsoft" , "united stats" ....] )
with open('scraping.csv','w',encoding='utf-8') as myfile: #some texts are not supported by the current encoding so i used (encoding='utf-8') to avoid raising an error if there was arabic words or any unsupported texts
    wr=csv.writer(myfile)
    wr.writerow(["Job Title", "Date", "Company Name","Company Location","Job Skills " ,"Job Requeirments", "links"]) # set the heading 
    try :
        wr.writerows(transposed) # write the final data (normalized two dimentional arr) int the csv file
    except:
        print ("error ocurred while writing the data on csv File")