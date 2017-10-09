# -*- coding:utf-8 -*-
import sys
import copy
import time
from urllib import unquote
import requests
from urllib import quote
import re
from lxml import etree
import unicodecsv as csv
import urllib2
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

LINKS_FINISHED = []

def company_500(url): #from web to crawl world top 500 company names
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    temp_name = soup.table.contents[1].contents
    name_list = []
    for item in temp_name:
        a = item.text.split()[1]
        name_list.append(a)
    return name_list


def createDictCSV(fileName="", dataDict={}): #output stream to csv
    path = '/Users/nero/Desktop/PycharmProjects/untitled/data'+'/'+fileName
    with open(path, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(dataDict)
        csvFile.close()

def login(laccount, lpassword):

    s = requests.Session()
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


def get_linkedin_url(url, s):

    try:
        r = s.get(url, allow_redirects=False)
        if r.status_code == 302 and 'Location' in r.headers.keys() and 'linkedin.com/in/' in r.headers['Location']:
            return r.headers['Location']
    except Exception, e:
        print 'get linkedin url failed: %s' % url
    return ''

def parse(content, url, person_propile):
    """ 解析一个员工的Linkedin主页 """
    dic_edu = {}
    dic_WEP = {}
    dic_Pub = {}
    dic_Hor = {}
    dic_Org = {}
    dic_Pat = {}
    dic_Pro = {}
    dic_Vol = {}
    content = unquote(content).replace('&quot;', '"')
    profile_txt = ' '.join(re.findall('(\{[^\{]*?profile\.Profile"[^\}]*?\})', content))
    #print profile_txt
    firstname = re.findall('"firstName":"(.*?)"', profile_txt)
    lastname = re.findall('"lastName":"(.*?)"', profile_txt)
    if firstname and lastname:
        print 'Name: %s%s    Linkedin: %s' % (lastname[0], firstname[0], url)
        person_propile['Name'] = lastname[0]+firstname[0]
        person_propile['Linkedin'] = url

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
            person_propile['LocationName'] = locationName[0]


        networkInfo_txt = ' '.join(re.findall('(\{[^\{]*?profile\.ProfileNetworkInfo"[^\}]*?\})', content))
        connectionsCount = re.findall('"connectionsCount":(\d+)', networkInfo_txt)
        if connectionsCount:
            print 'Friend_Num: %s' % connectionsCount[0]
            person_propile['Connections Num'] = connectionsCount[0]


        website_txt = ' '.join(re.findall('("included":.*?profile\.StandardWebsite",.*?\})', content))
        website = re.findall('"url":"(.*?)"', website_txt)
        if website:
            print 'Personal_Website: %s' % website[0]
            person_propile['Website'] = website[0]

        educations = re.findall('(\{[^\{]*?profile\.Education"[^\}]*?\})', content)
        if educations:
            print 'Education_Experience:'
        for one in educations:

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
                dic_edu[schoolName[0]] = schoolTime +' '+fieldOfStudy+' '+ degreeName
        person_propile['Education'] = dic_edu

        position = re.findall('(\{[^\{]*?profile\.Position"[^\}]*?\})', content)
        if position:
            print 'Working_Experience:'
        for one in position:
            companyName = re.findall('"companyName":"(.*?)"', one)
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
                print '    %s %s %s %s' % (companyName[0], positionTime, title, locationName)
                dic_WEP[companyName[0]] = positionTime+' '+title+' '+locationName
        person_propile['Working_Experience'] = dic_WEP

        publication = re.findall('(\{[^\{]*?profile\.Publication"[^\}]*?\})', content)
        if publication:
            print 'Publication_work:'
        for one in publication:
            name = re.findall('"name":"(.*?)"', one)
            publisher = re.findall('"publisher":"(.*?)"', one)
            if name:
                print '    %s %s' % (name[0], '   Publisher: %s' % publisher[0] if publisher else '')
                dic_Pub[name[0]] = publisher[0] if publisher else ''
        person_propile['Publication'] = dic_Pub

        honor = re.findall('(\{[^\{]*?profile\.Honor"[^\}]*?\})', content)
        if honor:
            print 'Honor:'
        for one in honor:
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
                dic_Hor[title[0]] = issuer[0] if issuer else ''+' '+issueTime
        person_propile['Hornor'] = dic_Hor

        organization = re.findall('(\{[^\{]*?profile\.Organization"[^\}]*?\})', content)
        if organization:
            print 'Organization:'
        for one in organization:
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
                dic_Org[name[0]] = organizationTime
        person_propile['Organization'] = dic_Org

        patent = re.findall('(\{[^\{]*?profile\.Patent"[^\}]*?\})', content)
        if patent:
            print 'Patent/Invention:'
        for one in patent:
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
                dic_Pat[title[0]] ='Publisher: '+ issuer[0] if issuer else ''+ '   Patent_Num: '+ number[0] if number else ''+ '   Country: '+ localizedIssuerCountryName[0] if localizedIssuerCountryName else ''+patentTime+'   Patent_Details: '+ url[0] if url else ''
        person_propile['Patent'] = dic_Pat

        project = re.findall('(\{[^\{]*?profile\.Project"[^\}]*?\})', content)
        if project:
            print 'Project:'
        for one in project:
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
                dic_Pro[title[0]] = projectTime+' '+'Project_Description: '+ description[0] if description else ''
        person_propile['Project'] = dic_Pro

        volunteer = re.findall('(\{[^\{]*?profile\.VolunteerExperience"[^\}]*?\})', content)
        if volunteer:
            print 'Volunteer_Experience:'
        for one in volunteer:
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
                dic_Vol[companyName[0]] = volunteerTime+' Role: '+ role[0] if role else ''
        person_propile['Volunteer'] = dic_Vol

        skills = re.findall('(\{[^\{]*?profile\.Skill"[^\}]*?\})', content)
        skill_list = []
        if skills:
            print 'Skills:'
        for one in skills:
            Skill_name = re.findall('"name":"(.*?)"', one)
            skill_list.append(Skill_name[0])
        print skill_list
        person_propile['Skills'] = skill_list
    print '\n\n'


def crawl(url, s, person_propile):

    try:
        url = get_linkedin_url(url, copy.deepcopy(s)).replace('cn.linkedin.com',
                                                              'www.linkedin.com')
        #print url
        if len(url) > 0 and url not in LINKS_FINISHED:
            LINKS_FINISHED.append(url)

            failure = 0
            while failure < 10:
                try:
                    r = s.get(url, timeout=10)
                    #print r.content
                except Exception, e:
                    failure += 1
                    continue
                if r.status_code == 200:
                    parse(r.content, url, person_propile)

                    break
                else:
                    print '%s %s' % (r.status_code, url)
                    failure += 2
            if failure >= 10:
                print 'Failed: %s' % url
    except Exception, e:
        pass

if __name__ == '__main__':
    s = login(laccount=‘XXX’, lpassword=‘XXX’)
    url_company_500 = "http://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites"
    company_list = ['P&G']
    #print company_list
    for it in company_list:
        company_name = it
        maxpage = 76
        result = []
        url = 'http://www.baidu.com/s?ie=UTF-8&wd=%20%7C%20领英%20' + quote(company_name) + '%20site%3Alinkedin.com'
        results = []
        failure = 0
        while len(url) > 0 and failure < 10:
            try:
                r = requests.get(url, timeout=10)
            except Exception, e:
                failure += 1
                continue
            if r.status_code == 200:
                hrefs = list(set(re.findall('"(http://www\.baidu\.com/link\?url=.*?)"', r.content)))  # 一页有10个搜索结果
                for href in hrefs:
                    person_propile = {}
                    crawl(href, copy.deepcopy(s), person_propile)
                    if person_propile != {}:
                        result.append(person_propile)
                createDictCSV(company_name, result)
                results += hrefs
                tree = etree.HTML(r.content)
                nextpage_txt = tree.xpath(
                    '//div[@id="page"]/a[@class="n" and contains(text(), "下一页")]/@href'.decode('utf8'))
                url = 'http://www.baidu.com' + nextpage_txt[0].strip() if nextpage_txt else ''
                failure = 0
                maxpage -= 1
                if maxpage <= 0:
                    break
            else:
                failure += 2
                print 'search failed: %s' % r.status_code
        if failure >= 10:
            print 'search failed: %s' % url
