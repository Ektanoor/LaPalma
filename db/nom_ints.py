#!/usr/bin/env python3

from geopy.geocoders import Nominatim
from datetime import datetime
from os import listdir
from os.path import isfile,join
import psycopg2
import re
import time

reconstruct=0


romans={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12 }

nom=Nominatim(domain='192.168.0.6/nominatim', scheme='http')

conn = psycopg2.connect(dbname="lapalma", user="qwatcher", password="11111111", host="192.168.0.1")
cur = conn.cursor()

if reconstruct:
    cur.execute("DROP  TABLE IF EXISTS intensity_maps");
    cur.execute("DROP  TABLE IF EXISTS intensity_coors");
    time.sleep(2)
    cur.execute("""CREATE TABLE IF NOT EXISTS intensity_maps (
                event character varying(16),
                min int,
                max int,
                location character varying(150),
                province character varying(10),
                checking character varying(3),
                primary key (event,location,min,max)
                )"""
    )

    cur.execute("CREATE INDEX event_maps_idx ON intensity_maps (event)")

    cur.execute("""CREATE TABLE IF NOT EXISTS intensity_coors (
                event character varying(16),
                coors geography(Point,4326),
                min int,
                max int,
                primary key (event,coors,min,max)
                )"""
    )

    cur.execute("CREATE INDEX event_coors_idx ON intensity_coors (event)")

extension_filter='txt'

mypath='./Intensities'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for filename in files:
    if extension_filter in filename:
        event=re.split(r'\.',filename)[0]
        f = open(mypath+'/'+filename, "r")
        oth=0
        for l in f:
            l=l.rstrip()
            int_min=0
            int_max=0
            region=''
            locality=''
            province=''
            checking=''
            if 'AUT ' in l or 'MAN' in l:
                oth=0
                if '.' in l:
                    loc=re.split(r'\.',l)
                    province=loc[1]
                    l=loc[0]
                else: province=''
                row=re.split(r'\s',l)

                checking=row[0]

                if '-' in row[1]:
                    ints=re.split(r'-',row[1])
                    int_min=romans[ints[0]]
                    int_max=romans[ints[1]]
                else:
                    int_min=romans[row[1]]
                    int_max=romans[row[1]]
                location=' '.join(row[2:])
                cur.execute(f"INSERT INTO intensity_maps (event,min,max,location,province,checking) VALUES ('{event}',{int_min},{int_max},'{location}','{province}','{checking}') ON CONFLICT DO NOTHING")
                conn.commit()
                print(location)
                coors=nom.geocode(location,exactly_one=True,addressdetails=False)
                print(coors)
                if not coors: continue
                cur.execute(f"INSERT INTO intensity_coors (event,coors,min,max) VALUES ('{event}',ST_GeographyFromText('SRID=4326;POINT({coors.longitude} {coors.latitude})'),{int_min},{int_max}) ON CONFLICT DO NOTHING")
                conn.commit()
        if oth: print(filename)
        f.close()

cur.close()
conn.close()


'''



'''