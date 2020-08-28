from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
import pyodbc
from datetime import datetime
import sqlcheck
from decimal import Decimal



with open('C:/Users/chris/OneDrive/Running/Running/mens.txt') as f:#read file with athlete name
    lines = f.read().splitlines()
driver = webdriver.Firefox(executable_path='C:/Users/chris/OneDrive/Running/Running/geckodriver.exe')#load driver
for name in lines:                                                  #loop thru athlete name
    athleteid=sqlcheck.insertathlete(name)
    driver.get("https://www.worldathletics.org/athletes")           #get to main page
    for x in range(211):                                            #get right country code
        driver.find_element_by_name("countryCode").send_keys(Keys.ARROW_DOWN)#country code
    for x in range(1):                                              #get right gender
        athid=driver.find_element_by_name("gender").send_keys(Keys.ARROW_DOWN)#gender
    driver.find_element_by_name("query").send_keys(name)            #enter name
    driver.find_element_by_class_name("btn-lg").click()             #click enter
    time.sleep(2)
    athlete= driver.find_element_by_class_name("records-table").find_element_by_tag_name('tbody').find_elements_by_tag_name("tr")#get each row in result table
    for ath in athlete:#loop thru each row
        years = True
        count=0
        if ath.find_element_by_css_selector('td').text==name:   #check if the first column  match   
            ath.find_element_by_css_selector('td').find_element_by_tag_name("a").click()#click on name
            time.sleep(1)
            for x in driver.find_element_by_class_name('outer-container').find_element_by_class_name('site-container').find_element_by_css_selector("div[class='container ctx-bound']").find_element_by_css_selector("ul").find_elements_by_css_selector("li"):#loop thru header
                if x.text=="Results":#check if header is result
                    x.click()#click result header
                    driver.find_element_by_class_name('outer-container').find_element_by_class_name('site-container').find_element_by_css_selector("div[class='container ctx-bound']").find_element_by_class_name('col-md-9').find_element_by_class_name('tab-content').find_element_by_id('results').find_element_by_name('resultsByYearOrderBy').send_keys(Keys.ARROW_DOWN)#get result order by year
                    while years==True:
                        time.sleep(2)
                        count=count+1
                        for y in driver.find_element_by_class_name('outer-container').find_element_by_class_name('site-container').find_element_by_css_selector("div[class='container ctx-bound']").find_element_by_class_name('col-md-9').find_element_by_class_name('tab-content').find_element_by_id('results').find_element_by_class_name('profile__results').find_element_by_css_selector("div[class='results-data ctx-bound']").find_element_by_class_name('results-data__inner').find_element_by_css_selector("div[class='results-wrapper results-by-date-wrapper']").find_element_by_css_selector("div[class='results__item table-wrapper']").find_element_by_css_selector("table[class='athletes-results-table records-table']").find_element_by_tag_name('tbody').find_elements_by_tag_name("tr"):#loop thru each result
                            date=None #default variables
                            competition=None
                            event=None
                            cnt=None
                            cat=None
                            race=None
                            pl=None
                            result=None
                            for z in y.find_elements_by_tag_name('td'):#loop thru in data field in a row
                                if z.get_attribute('data-th')=='Date':
                                    date=z.text
                                if z.get_attribute('data-th')=='Competition':
                                    competition=z.text
                                if z.get_attribute('data-th')=='Event':
                                    event=z.text
                                if z.get_attribute('data-th')=='Cnt.':
                                    cnt=z.text
                                if z.get_attribute('data-th')=='Cat':
                                    cat=z.text
                                if z.get_attribute('data-th')=='Race':
                                    race=z.text
                                if z.get_attribute('data-th')=='Pl.':
                                    pl=z.text.replace('.','')
                                if z.get_attribute('data-th')=='Result':
                                    result=z.text.replace('h','')
                            date=datetime.strptime(date, '%d %b %Y').date()
                            resulttype=''
                            if result!='DNF' and result!='' and result!='DQ' and result!='DNS' and result!='-':
                                racetime=''
                                timesplit=result.split(':')
                                countsplit=0
                                for x in timesplit: 
                                    decsplit=x.split('.')
                                    if countsplit==len(timesplit)-1:
                                        if len(decsplit)==2:
                                            if countsplit==0:
                                                racetime=decsplit[0].zfill(2)+'.'+decsplit[1].zfill(2)
                                            else:
                                                racetime=racetime+':'+decsplit[0].zfill(2)+'.'+decsplit[1].zfill(2)
                                        else:
                                            if countsplit==0:
                                                racetime=decsplit[0].zfill(2)+'.00'
                                            else:
                                                racetime=racetime+':'+decsplit[0].zfill(2)+'.00'
                                    else: 
                                        if countsplit==0:
                                            racetime=decsplit[0].zfill(2)
                                        else:
                                            racetime=racetime+':'+decsplit[0].zfill(2)
                                    countsplit=countsplit+1
                                if len(timesplit)==2:
                                    racetime='00:'+racetime
                                if len(timesplit)==1: 
                                    floatrace=Decimal(racetime)-60
                                    if floatrace>=0:
                                        floatsplit=str(floatrace).split('.')
                                        racetime='00:01:'+floatsplit[0].zfill(2)+'.'+floatsplit[1].zfill(2) 
                                    else:
                                        racetime='00:00:'+racetime    
                            else:
                                resulttype=result
                                racetime='00:00:00.00'

                            sqlcheck.insertresult(athleteid,competition,event,date,cnt,cat,pl,racetime,resulttype)
                            #print((name,date,competition,event,cnt,cat,race,pl,racetime,resulttype))#print tuple out           
                        if count<len(driver.find_element_by_class_name('outer-container').find_element_by_class_name('site-container').find_element_by_css_selector("div[class='container ctx-bound']").find_element_by_class_name('col-md-9').find_element_by_class_name('tab-content').find_element_by_id('results').find_element_by_name('resultsByYear').find_elements_by_tag_name('option')):
                            driver.find_element_by_class_name('outer-container').find_element_by_class_name('site-container').find_element_by_css_selector("div[class='container ctx-bound']").find_element_by_class_name('col-md-9').find_element_by_class_name('tab-content').find_element_by_id('results').find_element_by_name('resultsByYear').send_keys(Keys.ARROW_DOWN)#get result order by year
                        else:
                            years=False
                    break#break out of loop because title match
            break#break out of loop because name match







