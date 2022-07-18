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
        return None

@db_con
def add_plant(cur,name):
    lis_plant=cr_name_plant(name)
    permi=find_id_plant()
    if permi==None:
        sql_plant="""INSERT INTO plants (name,variety) VALUES(%s,%s)"""
        cur.execute(sql_plant,lis_plant)
    else:
        print('This plant is already here')

@db_con
def add_set(cur,list_settings):
    list_settings[-1]=find_id_plant(list_settings[-1])
    sql_light="""INSERT INTO light (stage,led,value,plant_id) VALUES(%s,%s,%s,%s)"""
    cur.execute(sql_light,list_settings)
