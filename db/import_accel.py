#!/usr/bin/env python3

from datetime import datetime
from os import listdir
from os.path import isfile,join
import psycopg2
import re

romans={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12 }

conn = psycopg2.connect(dbname="lapalma", user="qwatcher", password="111111111", host="192.168.0.1")
cur = conn.cursor()

file_filter='acelerogramasComunSV'
extension_filter='csv'

mypath='./Accel'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for filename in files:
    if file_filter in filename and extension_filter in filename:
        f = open(mypath+'/'+filename, "r")
        for l in f:
            if 'Evento' not in l:
                if '.IL' in l:
                    ort='C'
                    s=l.rstrip()
                    ar=re.split(r';',s)
                    loc=ar[8]
                    loc=re.split(r'\.',loc)
                    orient=re.split(r'\s',loc[0])
                    ar[8]=' '.join(orient[1:])
                    ort=orient[0]
                    date_str=f"{ar[1]} {ar[2]} UTC+0000"
                    if ar[5]=='': ar[5]=0
                    else: ar[5]=-1*int(ar[5])
                    if ar[6]=='': ar[6]='NULL'
                    tstamp=datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S %Z%z")
#                    print(f"'{ar[0]}','{tstamp}',ST_GeographyFromText('SRID=4326;POINTZM({ar[4]} {ar[3]} {ar[5]} {ar[7]})'),'{ar[6]}','{ar[8]}','{ort}','{ar[9]}',{ar[10]},{ar[11]},{ar[12]},{ar[13]}")
                    cur.execute(f"INSERT INTO acceleration (event,tstamp,coors,intensity,location,direction,station,distance,accel_ns,accel_v,accel_ew) VALUES \
                    ('{ar[0]}','{tstamp}',ST_GeographyFromText('SRID=4326;POINTZM({ar[4]} {ar[3]} {ar[5]} {ar[7]})'),'{ar[6]}','{ar[8]}','{ort}','{ar[9]}',{ar[10]},{ar[11]},{ar[12]},{ar[13]}) \
                    ON CONFLICT (event) DO UPDATE SET tstamp='{tstamp}',coors=ST_GeographyFromText('SRID=4326;POINTZM({ar[4]} {ar[3]} {ar[5]} {ar[7]})'),intensity='{ar[6]}',location='{ar[8]}',direction='{ort}', \
                    station='{ar[9]}',distance={ar[10]},accel_ns={ar[11]},accel_v={ar[12]},accel_ew={ar[13]}")
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
#                        print(f"'{ar[0]}',{int_min},{int_max}")
                        cur.execute(f"INSERT INTO intensities_accel (event,min,max) VALUES ('{ar[0]}',{int_min},{int_max}) ON CONFLICT (event) DO UPDATE SET min={int_min},max={int_max}")
                        conn.commit()
        f.close()
cur.close()
conn.close()


'''
Evento;     Fecha;     Hora;    Latitud;Longitud;Prof. (Km);Inten.;Mag.;Epicentro           ;Estación                            ;Dist.epic.(km)            ;Aceleración máxima(mg) N-S;Aceleración máxima(mg) V;Aceleración máxima(mg) E-W
es2021vnoyo;03/11/2021;04:59:54;28.5652;-17.7929;36        ;III   ;4.0 ;SW VILLA DE MAZO.ILP;Barros. Los (SANTA CRUZ DE TENERIFE);15.8                      ;4.02                      ;3.10                    ;5.27


CREATE TABLE IF NOT EXISTS acceleration (
    event character varying(16) primary key,
    tstamp timestamp with time zone,
    coors geography(PointZM,4326),
    intensity character varying(16),
    type int,
    location character varying(32),
    direction character varying(2),
    station  character varying(50),
    distance real,
    accel_ns real,
    accel_v real,
    accel_ew real
);

CREATE TABLE IF NOT EXISTS intensities_accel (
    event character varying(16) primary key,
    min int,
    max int
);

'''
