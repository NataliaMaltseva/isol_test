import psycopg2
from config import config

import time
from datetime import datetime, timezone

# write to bd bbox, video frame time and detect execution time
def add_to_bd(bbox, dt_st, time_ex):
    sql = "insert into detect_video(x_top_left,y_top_left,width,height,id_obj,time_stp,time_ex) values (%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    x,y,w,h,id_obj=bbox
    try:
        # # read database configuration
        params = config()
        # # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql,(x,y,w,h,int(id_obj),dt_st,time_ex))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# connect()
# st=time.time()
# dt = datetime.now(timezone.utc)
# end=time.time()
# ex=end-st
# add_to_bd((10,10,150,150,1), dt, ex)
