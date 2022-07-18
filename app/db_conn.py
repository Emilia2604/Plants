import psycopg2
import db_log

def db_con(func):
    def connect(*args, **kwargs):
        con=db_log.conn
        cur=db_log.curr
        func(cur,*args, **kwargs)
        con.commit()
        cur.close()
        con.close()
    return connect

def cr_name_plant(name_plant):
    name_plant=name_plant+' -'
    cut=name_plant.split()
    return cut[0:2]

@db_con
def plant_list(cur):
    plants=[]
    sql_plant_list="""SELECT name,variety FROM public.plants"""
    cur.execute(sql_plant_list)
    records=cur.fetchall()
    result = [row[0]+' '+row[1] for row in records]
    return result

@db_con
def find_spectrum(cur,stage,plant):
    data_set=[find_id_plant(plant),stage]
    sql_find_set="""SELECT value, led FROM public.light WHERE plant_id=%s AND stage=%s ORDER BY led ASC"""
    cur.execute(sql_find_set,data_set)
    records=cur.fetchall()
    value=[row[0] for row in records]
    led = [row[1] for row in records]
    result=dict(zip(led,value))
    return result

@db_con
def find_id_plant(cur,plant):
    name_plant=cr_name_plant(plant)
    sql_find_id="""SELECT id FROM public.plants WHERE name=%s AND variety=%s"""
    cur.execute(sql_find_id,name_plant)
    records=cur.fetchall()
    for row in records:
        id_plant=row
    try:
        return(id_plant[0])
    except:
        print('This plant is not here yet')

@db_con
def add_plant(cur,name):
    lis_plant=cr_name_plant(name)
    try:
        permi=find_id_plant(lis_plant)
    except:
        sql_plant="""INSERT INTO plants (name,variety) VALUES(%s,%s)"""
        cur.execute(sql_plant,lis_plant)
    finally:
        print('This plant is already here')

@db_con
def add_set(cur,list_settings):
    try:
        list_settings[-1]=find_id_plant(list_settings[-1])
    except:
        add_plant(list_settings[-1])
        list_settings[-1]=find_id_plant(list_settings[-1])
    sql_light="""INSERT INTO light (stage,led,value,plant_id) VALUES(%s,%s,%s,%s)"""
    cur.execute(sql_light,list_settings)
