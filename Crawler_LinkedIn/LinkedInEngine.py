# -*- coding:utf-8 -*-
import sys
import copy
import json
import time
from urllib import unquote
import requests
from urllib import quote
import re
from lxml import etree
import unicodecsv as csv
import urllib2
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import ssl



reload(sys)
sys.setdefaultencoding('utf8')


def login(laccount, lpassword):

    s = requests.Session()
    #adapter = requests.adapters.HTTPAdapter(max_retries=20)
    #s.mount('https://www.linkedin.com', adapter)
    r = s.get('https://www.linkedin.com/uas/login')

    tree = etree.HTML(r.content)
    loginCsrfParam = ''.join(tree.xpath('//input[@id="loginCsrfParam-login"]/@value'))
    csrfToken = ''.join(tree.xpath('//input[@id="csrfToken-login"]/@value'))
    sourceAlias = ''.join(tree.xpath('//input[@id="sourceAlias-login"]/@value'))
    isJsEnabled = ''.join(tree.xpath('//input[@name="isJsEnabled"]/@value'))
    source_app = ''.join(tree.xpath('//input[@name="source_app"]/@value'))
    tryCount = ''.join(tree.xpath('//input[@id="tryCount"]/@value'))
    clickedSuggestion = ''.join(tree.xpath('//input[@id="clickedSuggestion"]/@value'))
    signin = ''.join(tree.xpath('//input[@name="signin"]/@value'))
    session_redirect = ''.join(tree.xpath('//input[@name="session_redirect"]/@value'))
    trk = ''.join(tree.xpath('//input[@name="trk"]/@value'))
    fromEmail = ''.join(tree.xpath('//input[@name="fromEmail"]/@value'))

    payload = {
        'isJsEnabled': isJsEnabled,
        'source_app': source_app,
        'tryCount': tryCount,
        'clickedSuggestion': clickedSuggestion,
        'session_key': laccount,
        'session_password': lpassword,
        'signin': signin,
        'session_redirect': session_redirect,
        'trk': trk,
        'loginCsrfParam': loginCsrfParam,
        'fromEmail': fromEmail,
        'csrfToken': csrfToken,
        'sourceAlias': sourceAlias
    }
    s.post('https://www.linkedin.com/uas/login-submit', data=payload)
    return s

def createDictCSV(fileName="", dataDict={}): #output stream to csv
    path = '/Users/nero/Desktop/PycharmProjects/untitled/data'+'/'+fileName
    dict = {fileName:dataDict}
    with open(path, "wb") as file:
        #csvWriter = csv.writer(csvFile)
        #csvWriter.writerow(dataDict)
        #csvFile.close()
        file.write(json.dumps(dict))
        file.close()

def parse(content, url, person_propile, s):
    list_edu = []
    list_WEP = []
    list_Pub = []
    list_Hor = []
    list_Org = []
    list_Pat = []
    list_Pro = []
    list_Vol = []
    content = unquote(content).replace('&quot;', '"')
    profile_txt = ' '.join(re.findall('(\{[^\{]*?profile\.Profile"[^\}]*?\})', content))
    #print profile_txt
    firstname = re.findall('"firstName":"(.*?)"', profile_txt)
    lastname = re.findall('"lastName":"(.*?)"', profile_txt)
    if firstname and lastname:
        print 'Name: %s%s    Linkedin: %s' % (lastname[0], firstname[0], url)
        person_propile['Name'] = lastname[0]+firstname[0]
        person_propile['LinkedIn'] = url

        summary = re.findall('"summary":"(.*?)"', profile_txt)
        if summary:
            print 'Brief_Intro: %s' % summary[0]
            person_propile['Summary'] = summary[0]

        occupation = re.findall('"headline":"(.*?)"', profile_txt)
        if occupation:
            print 'Identity/Ocupation: %s' % occupation[0]
            person_propile['Occupation'] = occupation[0]

        locationName = re.findall('"locationName":"(.*?)"', profile_txt)
        if locationName:
            print 'Location: %s' % locationName[0]
            person_propile['Location'] = locationName[0]


        networkInfo_txt = ' '.join(re.findall('(\{[^\{]*?profile\.ProfileNetworkInfo"[^\}]*?\})', content))
        connectionsCount = re.findall('"connectionsCount":(\d+)', networkInfo_txt)
        if connectionsCount:
            print 'Friend_Num: %s' % connectionsCount[0]
            person_propile['Connection_Num'] = connectionsCount[0]


        website_txt = ' '.join(re.findall('("included":.*?profile\.StandardWebsite",.*?\})', content))
        website = re.findall('"url":"(.*?)"', website_txt)
        if website:
            print 'Personal_Website: %s' % website[0]
            person_propile['Website'] = website[0]

        educations = re.findall('(\{[^\{]*?profile\.Education"[^\}]*?\})', content)
        if educations:
            print 'Education_Experience:'
        for one in educations:
            dic_edu = {}
            schoolName = re.findall('"schoolName":"(.*?)"', one)
            fieldOfStudy = re.findall('"fieldOfStudy":"(.*?)"', one)
            degreeName = re.findall('"degreeName":"(.*?)"', one)
            timePeriod = re.findall('"timePeriod":"(.*?)"', one)
            schoolTime = ''
            if timePeriod:
                startdate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                enddate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                start_year = re.findall('"year":(\d+)', startdate_txt)
                start_month = re.findall('"month":(\d+)', startdate_txt)
                end_year = re.findall('"year":(\d+)', enddate_txt)
                end_month = re.findall('"month":(\d+)', enddate_txt)
                startdate = ''
                if start_year:
                    startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                enddate = ''
                if end_year:
                    enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                if len(startdate) > 0 and len(enddate) == 0:
                    enddate = 'Now'
                schoolTime += '   %s ~ %s' % (startdate, enddate)
            if schoolName:
                fieldOfStudy = '   %s' % fieldOfStudy[0] if fieldOfStudy else ''
                degreeName = '   %s' % degreeName[0] if degreeName else ''
                print '    %s %s %s %s' % (schoolName[0], schoolTime, fieldOfStudy, degreeName)
                #---------------------------#
                dic_edu['School_Name'] = schoolName[0]
                dic_edu['Field_Study'] = fieldOfStudy
                dic_edu['Degree_Name'] = degreeName
                dic_edu['Start_Date'] = startdate
                dic_edu['End_Date'] = enddate
                list_edu.append(dic_edu)
                #---------------------------#
        person_propile['Education'] = list_edu

        position = re.findall('(\{[^\{]*?profile\.Position"[^\}]*?\})', content)
        if position:
            print 'Working_Experience:'
        for one in position:
            dic_WEP = {}
            companyName = re.findall('"companyName":"(.*?)"', one)
            description = re.findall('"description":"(.*?)"', one)
            title = re.findall('"title":"(.*?)"', one)
            locationName = re.findall('"locationName":"(.*?)"', one)
            timePeriod = re.findall('"timePeriod":"(.*?)"', one)
            positionTime = ''
            if timePeriod:
                startdate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                enddate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                start_year = re.findall('"year":(\d+)', startdate_txt)
                start_month = re.findall('"month":(\d+)', startdate_txt)
                end_year = re.findall('"year":(\d+)', enddate_txt)
                end_month = re.findall('"month":(\d+)', enddate_txt)
                startdate = ''
                if start_year:
                    startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                enddate = ''
                if end_year:
                    enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                if len(startdate) > 0 and len(enddate) == 0:
                    enddate = 'Now'
                positionTime += '   %s ~ %s' % (startdate, enddate)
            if companyName:
                title = '   %s' % title[0] if title else ''
                locationName = '   %s' % locationName[0] if locationName else ''
                description = '   %s' % description[0] if description else ''
                print '    %s %s %s %s %s' % (companyName[0], positionTime, title, locationName, description)
                #-------------------------------#
                dic_WEP['Company_Name'] = companyName[0]
                dic_WEP['Title'] = title
                dic_WEP['Location'] = locationName
                dic_WEP['Description'] = description
                dic_WEP['Start_Date'] = startdate
                dic_WEP['End_Date'] = enddate
                list_WEP.append(dic_WEP)
                #-------------------------------#
        person_propile['WorkingExperience'] = list_WEP

        publication = re.findall('(\{[^\{]*?profile\.Publication"[^\}]*?\})', content)
        if publication:
            print 'Publication_work:'
        for one in publication:
            dic_Pub = {}
            name = re.findall('"name":"(.*?)"', one)
            publisher = re.findall('"publisher":"(.*?)"', one)
            if name:
                print '    %s %s' % (name[0], '   Publisher: %s' % publisher[0] if publisher else '')
                #------------------------------------------#
                dic_Pub['Pub_Name'] = name[0]
                dic_Pub['Publisher'] = publisher[0] if publisher else ''
                list_Pub.append(dic_Pub)
                #------------------------------------------#
                #dic_Pub[name[0]] = publisher[0] if publisher else ''
        person_propile['Publication'] = list_Pub

        honor = re.findall('(\{[^\{]*?profile\.Honor"[^\}]*?\})', content)
        if honor:
            print 'Honor:'
        for one in honor:
            dic_Hor = {}
            title = re.findall('"title":"(.*?)"', one)
            issuer = re.findall('"issuer":"(.*?)"', one)
            issueDate = re.findall('"issueDate":"(.*?)"', one)
            issueTime = ''
            if issueDate:
                issueDate_txt = ' '.join(
                    re.findall('(\{[^\{]*?"\$id":"%s"[^\}]*?\})' % issueDate[0].replace('(', '\(').replace(')', '\)'),
                               content))
                year = re.findall('"year":(\d+)', issueDate_txt)
                month = re.findall('"month":(\d+)', issueDate_txt)
                if year:
                    issueTime += '   Issue_time: %s' % year[0]
                    if month:
                        issueTime += '.%s' % month[0]
            if title:
                print '    %s %s %s' % (title[0], '   Publisher: %s' % issuer[0] if issuer else '', issueTime)
                #--------------------------------------#
                dic_Hor['Honor_Title'] = title[0]
                dic_Hor['Issuer'] = issuer[0] if issuer else ''
                dic_Hor['Issue_Date'] = issueTime
                list_Hor.append(dic_Hor)
                #--------------------------------------#
                #dic_Hor[title[0]] = issuer[0] if issuer else ''+' '+issueTime
        person_propile['Hornor'] = list_Hor

        organization = re.findall('(\{[^\{]*?profile\.Organization"[^\}]*?\})', content)
        if organization:
            print 'Organization:'
        for one in organization:
            dic_Org = {}
            name = re.findall('"name":"(.*?)"', one)
            timePeriod = re.findall('"timePeriod":"(.*?)"', one)
            organizationTime = ''
            if timePeriod:
                startdate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                enddate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                start_year = re.findall('"year":(\d+)', startdate_txt)
                start_month = re.findall('"month":(\d+)', startdate_txt)
                end_year = re.findall('"year":(\d+)', enddate_txt)
                end_month = re.findall('"month":(\d+)', enddate_txt)
                startdate = ''
                if start_year:
                    startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                enddate = ''
                if end_year:
                    enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                if len(startdate) > 0 and len(enddate) == 0:
                    enddate = 'Now'
                organizationTime += '   %s ~ %s' % (startdate, enddate)
            if name:
                print '    %s %s' % (name[0], organizationTime)
                #-----------------------------------------#
                dic_Org['Org_Name'] = name[0]
                dic_Org['Start_Date'] = startdate
                dic_Org['End_Date'] = enddate
                list_Org.append(dic_Org)
                #-----------------------------------------#
                #dic_Org[name[0]] = organizationTime
        person_propile['Organization'] = list_Org

        patent = re.findall('(\{[^\{]*?profile\.Patent"[^\}]*?\})', content)
        if patent:
            print 'Patent/Invention:'
        for one in patent:
            dic_Pat = {}
            title = re.findall('"title":"(.*?)"', one)
            issuer = re.findall('"issuer":"(.*?)"', one)
            url = re.findall('"url":"(http.*?)"', one)
            number = re.findall('"number":"(.*?)"', one)
            localizedIssuerCountryName = re.findall('"localizedIssuerCountryName":"(.*?)"', one)
            issueDate = re.findall('"issueDate":"(.*?)"', one)
            patentTime = ''
            if issueDate:
                issueDate_txt = ' '.join(
                    re.findall('(\{[^\{]*?"\$id":"%s"[^\}]*?\})' % issueDate[0].replace('(', '\(').replace(')', '\)'),
                               content))
                year = re.findall('"year":(\d+)', issueDate_txt)
                month = re.findall('"month":(\d+)', issueDate_txt)
                day = re.findall('"day":(\d+)', issueDate_txt)
                if year:
                    patentTime += '   Issue_Time: %s' % year[0]
                    if month:
                        patentTime += '.%s' % month[0]
                        if day:
                            patentTime += '.%s' % day[0]
            if title:
                print '    %s %s %s %s %s %s' % (
                title[0], '   Publisher: %s' % issuer[0] if issuer else '', '   Patent_Num: %s' % number[0] if number else '',
                '   Nation: %s' % localizedIssuerCountryName[0] if localizedIssuerCountryName else '', patentTime,
                '   Patent_Details: %s' % url[0] if url else '')
                #---------------------------------------------------#
                dic_Pat['Title'] = title[0]
                dic_Pat['Issuer'] = issuer[0] if issuer else ''
                dic_Pat['Patent_Number'] = number[0] if number else ''
                dic_Pat['Country'] = localizedIssuerCountryName[0] if localizedIssuerCountryName else ''
                dic_Pat['Patent_Time'] = patentTime
                dic_Pat['Patent_Detail'] = url[0] if url else ''
                list_Pat.append(dic_Pat)
                #---------------------------------------------------#
                #dic_Pat[title[0]] ='Publisher: '+ issuer[0] if issuer else ''+ '   Patent_Num: '+ number[0] if number else ''+ '   Country: '+ localizedIssuerCountryName[0] if localizedIssuerCountryName else ''+patentTime+'   Patent_Details: '+ url[0] if url else ''
        person_propile['Patent'] = list_Pat

        project = re.findall('(\{[^\{]*?profile\.Project"[^\}]*?\})', content)
        if project:
            print 'Project:'
        for one in project:
            dic_Pro = {}
            title = re.findall('"title":"(.*?)"', one)
            description = re.findall('"description":"(.*?)"', one)
            timePeriod = re.findall('"timePeriod":"(.*?)"', one)
            projectTime = ''
            if timePeriod:
                startdate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                enddate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                start_year = re.findall('"year":(\d+)', startdate_txt)
                start_month = re.findall('"month":(\d+)', startdate_txt)
                end_year = re.findall('"year":(\d+)', enddate_txt)
                end_month = re.findall('"month":(\d+)', enddate_txt)
                startdate = ''
                if start_year:
                    startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                enddate = ''
                if end_year:
                    enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                if len(startdate) > 0 and len(enddate) == 0:
                    enddate = 'Now'
                projectTime += '   Time: %s ~ %s' % (startdate, enddate)
            if title:
                print '    %s %s %s' % (title[0], projectTime, '   Project_Description: %s' % description[0] if description else '')
                #---------------------------------------#
                dic_Pro['Title'] = title[0]
                dic_Pro['Description'] = description[0] if description else ''
                dic_Pro['Start_Date'] = startdate
                dic_Pro['End_Date'] = enddate
                list_Pro.append(dic_Pro)
                #---------------------------------------#
                #dic_Pro[title[0]] = projectTime+' '+'Project_Description: '+ description[0] if description else ''
        person_propile['Project'] = list_Pro

        volunteer = re.findall('(\{[^\{]*?profile\.VolunteerExperience"[^\}]*?\})', content)
        if volunteer:
            print 'Volunteer_Experience:'
        for one in volunteer:
            dic_Vol = {}
            companyName = re.findall('"companyName":"(.*?)"', one)
            role = re.findall('"role":"(.*?)"', one)
            timePeriod = re.findall('"timePeriod":"(.*?)"', one)
            volunteerTime = ''
            if timePeriod:
                startdate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                enddate_txt = ' '.join(re.findall(
                    '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' % timePeriod[0].replace('(', '\(').replace(')', '\)'),
                    content))
                start_year = re.findall('"year":(\d+)', startdate_txt)
                start_month = re.findall('"month":(\d+)', startdate_txt)
                end_year = re.findall('"year":(\d+)', enddate_txt)
                end_month = re.findall('"month":(\d+)', enddate_txt)
                startdate = ''
                if start_year:
                    startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                enddate = ''
                if end_year:
                    enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                if len(startdate) > 0 and len(enddate) == 0:
                    enddate = 'Now'
                volunteerTime += '   Time: %s ~ %s' % (startdate, enddate)
            if companyName:
                print '    %s %s %s' % (companyName[0], volunteerTime, '   Role: %s' % role[0] if role else '')
                #--------------------------------------#
                dic_Vol['Company_Name'] = companyName[0]
                dic_Vol['Role'] = role[0] if role else ''
                dic_Vol['Start_Date'] = startdate
                dic_Vol['End_Date'] = enddate
                list_Vol.append(dic_Vol)
                #--------------------------------------#
                #dic_Vol[companyName[0]] = volunteerTime+' Role: '+ role[0] if role else ''
        person_propile['Volunteer'] = list_Vol

        skills = re.findall('(\{[^\{]*?profile\.Skill"[^\}]*?\})', content)
        skill_list = []
        skill_dict = {}
        skill_Flist = []
        if skills:
            print 'Skills:'
            link = url + '/detail/skills/'
            skill_r = copy.deepcopy(s).get(link, allow_redirects=False)
            soup_skill = BeautifulSoup(skill_r.content, 'lxml')
            item = soup_skill.find_all('code')
            for item in soup_skill.find_all('code'):
                Skill_name = re.findall('(fs_skill:(?:(?!").|\n)*?","name":".*?")', item.text)
                Skill_endorsement = re.findall('(fs_skill:(?:(?!").|\n)*?","endorsementCount":\d{1,})', item.text)
                if Skill_name:
                    for ee in Skill_name:
                        skill_dict[re.findall('fs_skill:(.*?)"', ee)[0]] = re.findall('"name":"(.*?)"', ee)
                if Skill_endorsement:
                    for jj in Skill_endorsement:
                        skill_dict[re.findall('fs_skill:(.*?)"', jj)[0]].append(
                            re.findall('"endorsementCount":(\d{1,})', jj)[0])
            skill_list = skill_dict.values()
            for i in range(0, len(skill_list) - 1):
                for j in range(i + 1, len(skill_list)):
                    if int(skill_list[i][1]) <= int(skill_list[j][1]):
                        v_temp = skill_list[i]
                        skill_list[i] = skill_list[j]
                        skill_list[j] = v_temp
            for item in skill_list:
                dic_temp = {}
                dic_temp['Skill_Name'] = item[0]
                dic_temp['Endorsement'] = int(item[1])
                skill_Flist.append(dic_temp)

        person_propile['Skills'] = skill_Flist
        print skill_Flist
    print '\n\n'

def crawl(url, s, person_propile):
    try:
            failure = 0
            while failure < 10:
                try:
                    r = s.get(url, timeout=10)
                    #print r.content
                except Exception, e:
                    failure += 1
                    continue
                if r.status_code == 200:
                    parse(r.content, url, person_propile, s)

                    break
                else:
                    print '%s %s' % (r.status_code, url)
                    failure += 2
            if failure >= 10:
                print 'Failed: %s' % url
    except Exception, e:
        pass

def crawl_LinkedIn(people_name, max_page, craw_list, s):
    base = "https://www.linkedin.com/in/"
    for i in range(0, max_page):
        url = 'https://www.linkedin.com/search/results/index/?keywords=' + people_name + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(i)
        try:
            r = copy.deepcopy(s).get(url, allow_redirects=False)
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
        if r.status_code == 200:
            time.sleep(3)
            soup = BeautifulSoup(r.content, 'lxml')
            temp = soup.find_all('code')
            for box in temp:
                if ("metadata" in box.text.encode('utf-8')):
                    identifier = re.findall('"publicIdentifier":"(.*?)"', box.text)
                    for ele in identifier:
                        if ele != 'UNKNOWN':
                            craw_list.append(base + ele.encode('utf-8'))

def create_RTF(search_name):
    s = login(laccount='735422760@qq.com', lpassword='1234qwer')
    Final_list = []
    result = []
    Max_Page = 90
    crawl_LinkedIn(search_name, Max_Page, Final_list, s)
    Final_list = list(set(Final_list))
    for href in Final_list:
        person_propile = {}
        crawl(href, copy.deepcopy(s), person_propile)
        if person_propile != {}:
            result.append(person_propile)
    createDictCSV(search_name, result)
    print len(Final_list)




if __name__ == '__main__':
    search_key = ['Department of Computer Science and Engineering']
    for item in search_key:
        create_RTF(item.replace(' ','%20').replace('&','%26'))

