# -*- coding: UTF-8 -*-

import pymysql
import json
import time
import datetime
from dateutil.parser import parse
import calendar

def datetime_timestamp(dt):
    dt = dt.replace(u'年','-')
    dt = dt.replace(u'月','-')
    dt = dt.replace(u'日','-')
    dt = parse(dt) # 解析日期时间
    timeArray = dt.timetuple ()
    timeStamp = int(time.mktime(timeArray))
    # 转换为时间戳
    return timeStamp


class SQLEngine:
    def __init__(self):
        try:
            self.db = pymysql.connect("localhost","root","1234qwer","LinkedIn_data")
            self.cur = self.db.cursor()
        except pymysql.Error,e:
            print "connection failed, error%d: %s" % (e.args[0],e.args[1])

    def insertData(self,table,my_dict, f_id=0):
        print "insert:%s" % table
        try:
            #sql = "SELECT"
            if True:#self.db.insert_id() == 0:
                sql = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
                self.cur.execute(sql)
                self.db.commit()
            self.db.set_charset("utf8")
            cols = ', '.join(my_dict.keys())
            values = '","'.join(my_dict.values())

            if f_id == 0:
                sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
            else:
                sql = "INSERT INTO %s (%s , p_id) VALUES (%s, %d)" % (table, cols, '"'+values+'"', f_id)
            try:
                result = self.cur.execute(sql)
                insert_id = self.cur.lastrowid
                self.db.commit()
                if result:
                    #print insert_id
                    return insert_id
                else:
                    return 0
            except pymysql.Error,e:
                print e
                self.db.rollback()
                return 0
        except pymysql.Error,e:
            print e

    def __del__(self):
        self.db.close()


testdict = json.load(open("supply%20chain%20manager"))

engine = SQLEngine()
for item in testdict:
    for entity in testdict[item]:
        profile_key = ["Name","Occupation","LinkedIn","Summary","Location","Connection_Num"]
        #print entity
        p_id = engine.insertData("`Profile`",my_dict={key:value for key,value in entity.items() if key in profile_key})

        print p_id

        if p_id==0:
            continue

        multi_key = ["WorkingExperience","Education","Volunteer","Skills","Project","Publication","Honor","Patent","Organization"]

        for sub_key in multi_key:
            if sub_key in entity:
                for sub_entity in entity[sub_key]:
                    if "Start_Date" in sub_entity:
                        print sub_entity["Start_Date"]
                        try:
                            datelist = sub_entity["Start_Date"].split(".")
                            if len(datelist)==1:
                                sub_entity["Start_Date"]= str(datetime.date(int(datelist[0]),1,1))
                            if len(datelist)==2:
                                sub_entity["Start_Date"] = str(datetime.date(int(datelist[0]), int(datelist[1]), 1))
                        except Exception,e:
                            print e
                        print sub_entity["Start_Date"]
                    if "End_Date" in sub_entity:
                        print sub_entity["End_Date"]
                        try:
                            try:
                                datelist = sub_entity["End_Date"].split(".")
                                if len(datelist) == 1:
                                    firstDayWeekDay, monthRange = calendar.monthrange(int(datelist[0]), 12)
                                    sub_entity["End_Date"] = str(datetime.date(int(datelist[0]), 12, monthRange))
                                if len(datelist) == 2:
                                    firstDayWeekDay, monthRange = calendar.monthrange(int(datelist[0]), int(datelist[1]))
                                    sub_entity["End_Date"] = str(datetime.date(int(datelist[0]), int(datelist[1]), monthRange))
                            except:
                                sub_entity["End_Date"] = str(datetime.date.today())
                        except Exception, e:
                            print e
                        print sub_entity["End_Date"]
                    if "Patent_Time" in sub_entity:
                        sub_entity["Patent_Time"] = sub_entity["Patent_Time"].split(":")[1]

                    engine.insertData(sub_key,my_dict={key:unicode(value) for key,value in sub_entity.items()},f_id=p_id)

        #if "Working_Experience" in entity:#entity["Working_Experience"]:
        #    for we_entity in entity["Working_Experience"]:
                ##To do !!! date
                #if isinstance(we_entity["End_Date"],(str,unicode)):
                #    we_entity["End_Date"] = datetime.date.today()
                #print we_entity
                #engine.insertData("WorkingExperience",my_dict={key:unicode(value) for key,value in we_entity.items()},f_id=p_id)

#engine.insertData("T1",my_dict=testdict)