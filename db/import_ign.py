#!/usr/bin/env python3

from datetime import datetime
from os import listdir
from os.path import isfile,join
import psycopg2
import re

romans={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12 }

conn = psycopg2.connect(dbname="lapalma", user="qwatcher", password="11111111", host="192.168.0.1")
cur = conn.cursor()

file_filter='catalogoComunSV'
extension_filter='csv'

mypath='./Quakes'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for filename in files:
    if file_filter in filename and extension_filter in filename:
        f = open(mypath+'/'+filename, "r")
        for l in f:
            if 'Evento' not in l:
                if 'PALMA.IL' in l or '.ILP' in l or 'Isla de La Palma' in l:
                    ort='C'
                    s=l.rstrip()
                    ar=re.split(r';\s*',s)
                    ar[0]=ar[0].lstrip()
                    loc=ar[-1]
                    if ',' in loc:
                        loc=re.split(r'\,',loc)[0]
                        ar[-1]=loc
                    if '.' in  loc:
                        loc=re.split(r'\.',loc)
                        orient=re.split(r'\s',loc[0])
                        if len(orient[0])<3:
                            ar[-1]=' '.join(orient[1:])
                            ort=orient[0]
                        else: ar[-1]=loc[0]
                    if ar[5]=='': ar[5]=0
                    else: ar[5]=-1*int(ar[5])
                    if ar[6]=='': ar[6]='NULL'
                    if ar[7]=='': ar[7]=-1
                    if ar[8]=='': ar[8]=-1
                    date_str=f"{ar[1]} {ar[2]} UTC+0000"
                    tstamp=datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S %Z%z")
                    cur.execute(f"INSERT INTO quakes (event,tstamp,coors,intensity,type,location,direction) VALUES \
                    ('{ar[0]}','{tstamp}',ST_GeographyFromText('SRID=4326;POINTZM({ar[4]} {ar[3]} {ar[5]} {ar[7]})'),'{ar[6]}',{ar[8]},'{ar[9]}','{ort}') \
                    ON CONFLICT (event) DO UPDATE SET tstamp='{tstamp}',coors=ST_GeographyFromText('SRID=4326;POINTZM({ar[4]} {ar[3]} {ar[5]} {ar[7]})'),intensity='{ar[6]}',type={ar[8]},location='{ar[9]}',direction='{ort}'")
                    conn.commit()

                    if ar[6]!='NULL':
                        if ar[6]=='-1' or ar[6]=='-1.0':
                            int_min=0
                            int_max=0
                        else:
                            if '-' in ar[6]:
                                ints=re.split(r'-',ar[6])
                                int_min=romans[ints[0]]
                                int_max=romans[ints[1]]
                            else:
                                int_min=romans[ar[6]]
                                int_max=romans[ar[6]]
                        cur.execute(f"INSERT INTO intensities (event,min,max) VALUES ('{ar[0]}',{int_min},{int_max}) ON CONFLICT (event) DO UPDATE SET min={int_min},max={int_max}")
                        conn.commit()
        f.close()
cur.close()
conn.close()


'''

CREATE TABLE IF NOT EXISTS quakes (
    event character varying(16) primary key,
    tstamp timestamp with time zone,
    coors geography(PointZM,4326),
    intensity character varying(16),
    type int,
    location character varying(32),
    direction character varying(2)
);

CREATE TABLE IF NOT EXISTS intensities (
    event character varying(16) primary key,
    min int,
    max int
);

'''
