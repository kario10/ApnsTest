import pymysql.cursors
from apscheduler.schedulers.blocking import BlockingScheduler
import pushNotification
import time
#I use the apscheduler to do schedule job, to prevent use too much system resource
current_rowcount_result = {}

first_check = True


#This is the connection of database
#This whole documentation could be found in https://pymysql.readthedocs.io

sched = BlockingScheduler()

def checkUpdate():
    try:
        global current_rowcount_result
        global first_check
        coon = pymysql.connect(
            host='',
            user='',
            password='',
            db='',
            charset='',
            cursorclass=pymysql.cursors.DictCursor
        )
        with coon.cursor() as cursor:
            #read a single record,check everything in the database
            sql = "SELECT * FROM  ``"
            cursor.execute(sql)
            result = cursor.fetchall()
            #if there is no defferent, it will not call the APNs to push notification.
            #if the result is not the same, it will print out the data and call APNs to push this notificaiton.
            print(first_check)
            if first_check == False :
                if result != current_rowcount_result :
                    annoucementOrigenal = getAnnouncement(current_rowcount_result)
                    annoucementNow = getAnnouncement(result)
                    retD = list(set(annoucementNow).difference(set(annoucementOrigenal)))
                    print("There seems some one post a new announcement")
                    print(retD)
                    print(retD[0])
                    pushNotification.pushNotification(retD[0])
            current_rowcount_result = result
            first_check = False
            print(current_rowcount_result)
            print(result)
    finally:
        coon.close()
        print("finish checking School App DataBase")


def getAnnouncement(dict):
    a = []
    for i in dict:
        print(i)
        a.append(i["Announcement"])
    return a

if __name__ == '__main__' :
    sched.add_job(checkUpdate,
                  "interval",
                  seconds = 5,
                  misfire_grace_time=10,
                  coalesce=True,
                  max_instances=1)
    sched.start()