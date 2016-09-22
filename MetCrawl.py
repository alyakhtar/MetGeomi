#Importing the required Modules
import psycopg2
import sys
from sys import argv

con = None

#Connecting with the Database
def create_connection(database , user):
    cur_db = database
    cur_usr = user 
    con = psycopg2.connect(database = cur_db , user = cur_usr) 
    return con


#Creating Tables
def create_tables(con):
    cur = con.cursor()

    cur.execute("CREATE TABLE student(Stu_ID INTEGER PRIMARY KEY, Name VARCHAR(40), Address VARCHAR(10) , Sex VARCHAR(5))")
    cur.execute("CREATE TABLE department(Dep_Code INTEGER PRIMARY KEY, Dep_Name VARCHAR(40))")
    cur.execute("CREATE TABLE course(Cour_No INTEGER PRIMARY KEY , Cour_Name VARCHAR(20))")
    cur.execute("CREATE TABLE section(Sec_No INTEGER PRIMARY KEY, Sem VARCHAR(10) ,Year INTEGER)")
    cur.execute("CREATE TABLE grade_report(Letter_Grade VARCHAR(2), Num_Grade INTEGER)")
    cur.execute("CREATE TABLE log(S_ID INTEGER)")
    cur.execute("CREATE TABLE company(ID INTEGER NOT NULL UNIQUE , Name VARCHAR(10) NOT NULL)")     
    con.commit()


#Insering sample data
def insert_data(con):
    cur = con.cursor()

    cur.execute("INSERT INTO student VALUES(3 , 'Gama' , 'Delhi' , 'Male')")
    cur.execute("INSERT INTO student VALUES(2 , 'Beta' , 'Mumbai' , 'Male')")
    cur.execute("INSERT INTO department VALUES(305 , 'Computer Engineering')")
    cur.execute("INSERT INTO course VALUES(101 , 'Operating System' )")

    con.commit()


#Print data
def show_tables(con):
    cur = con.cursor()

    cur.execute("SELECT * FROM student")
    resp = cur.fetchall()

    for row in resp:
        print row


#Creating Functions
def create_function(con):
    cur = con.cursor()

    psql_command = '''CREATE OR REPLACE FUNCTION show_rec_name (rec_id INTEGER , sample CHAR(10))
                      RETURNS char(20) AS $rec_name$
                      declare
                      rec_name char(20);
                      BEGIN
                      SELECT name into rec_name FROM student WHERE stu_id = rec_id;
                      RETURN rec_name;
                      END;
                      $rec_name$ LANGUAGE plpgsql;'''

    cur.execute(psql_command)

    con.commit()


#Testing fucntion with sample input
def func_test():
    cur = con.cursor()

    cur.execute("select show_rec_name(2)")
    resp=cur.fetchone()
    print resp[0]
    
    con.commit()


#Creating Views
def create_view(con):
    cur = con.cursor()

    psql_command = '''CREATE VIEW student_view2 AS
              SELECT student.Stu_Id, student.Name, course.Cour_No 
              FROM  student,course;'''

    cur.execute(psql_command)
    con.commit()



#Creating Triggers
def create_trigger(con):
    cur = con.cursor()

    psql_command = '''CREATE OR REPLACE FUNCTION log_add_entry()
            RETURNS trigger AS $stu$

              BEGIN
            INSERT INTO log VALUES(new.Stu_ID); 
            RETURN NEW;
              END;
                      $stu$ LANGUAGE plpgsql;'''
    
    cur.execute(psql_command)   
    
    psql_command = '''CREATE TRIGGER test_trig AFTER INSERT ON student
              FOR EACH ROW EXECUTE PROCEDURE log_add_entry();'''

    cur.execute(psql_command)

    con.commit()


#Creating TablesForIndexes
def create_indexes(con):
    cur = con.cursor()

    cur.execute("CREATE TABLE test (a int, b int, c int, constraint pk_test primary key(a, b))")
    cur.execute("CREATE TABLE test2 (a int, b int, c int, constraint uk_test2 unique (b, c))")
    cur.execute("CREATE TABLE test3 (a int, b int, c int, constraint uk_test3b unique (b), constraint uk_test3c unique (c),constraint uk_test3ab unique (a, b))")   
      
    con.commit()

#Extracting the Tables Info from database
def meta_crawl_tables(con):
    cur = con.cursor()

    tables=[]
    cur.execute("SELECT table_name FROM information_schema.tables "
                "WHERE table_schema='public' "
                "AND table_type='BASE TABLE'");
    resp = cur.fetchall()
    
    for row in resp:
        tables.append(row[0])

    
    return tables   
        

#Extracting the Columns Info from database
def meta_crawl_columns(con):
    cur = con.cursor()
    to_d_col=[]
    tables = meta_crawl_tables(con)
    for table in tables:
        cur.execute("SELECT column_name,data_type,character_maximum_length "
                "FROM information_schema.columns "
                "WHERE table_name = '" + table + "'");
        resp = cur.fetchall()
        #to_d_col=[]
        for row in resp:
            columns=[]
            columns.append(table)
            columns.append(row[0])
            columns.append(row[1])
            columns.append(row[2])
            to_d_col.append(columns)
    print to_d_col        


#DataTypeID to DataTypeName Mapping
def typeid_to_typename(con , id):
    cur = con.cursor()

    cur.execute("SELECT typname from pg_type WHERE oid = " + str(id))
    resp = cur.fetchone()
    return resp[0]

        
#Extracting the Functions Info from database
def meta_crawl_functions(con):
    cur = con.cursor()
    to_d_func=[]
    user_func=[]
    cur.execute("SELECT routine_name FROM information_schema.routines WHERE specific_schema = 'public'")    
    resp=cur.fetchall()
    for row in resp:
        user_func.append(row[0])

    
    cur.execute("SELECT proname, prorettype, pronargs, proargnames , proargtypes from pg_proc WHERE proname IN " + str(tuple(user_func)))
    resp = cur.fetchall()
    for row in resp:
        functions=[]
        ret_type_list=[]
        functions.append(row[0])
        functions.append(typeid_to_typename(con , row[1]))
        functions.append(row[2])
        functions.append(row[3])
        ret_arg = row[4].split()
        for item in ret_arg:
            ret_type_list.append(typeid_to_typename(con , item))
        functions.append(ret_type_list)
        to_d_func.append(functions)

    print to_d_func    
                 

#Extracting the Triggers Info from database
def meta_crawl_triggers(con):
    cur = con.cursor()
    to_d_trig=[]
    
    cur.execute("SELECT trigger_name, action_timing, event_manipulation, event_object_table FROM information_schema.triggers")    
    resp=cur.fetchall()
    for row in resp:
        trig=[]
        trig.append(row[0])
        trig.append(row[2])
        trig.append(row[2])
        trig.append(row[3])
        to_d_trig.append(trig) 

    print to_d_trig      
 
#Extracting the Views Info from database
def meta_crawl_views(con):
    cur = con.cursor()
    cur.execute("SELECT table_name FROM information_schema.views WHERE table_schema = 'public'")    
    resp=cur.fetchall()
    to_d_view=[]
    for row in resp:
        view=[]
        view.append(row[0])
        tb=[]
        cur.execute("SELECT table_name FROM information_schema.view_table_usage WHERE view_name = '"+ str(row[0]) +"'")
        sub_resp = cur.fetchall()
        for item in sub_resp:
            tb.append(item[0])   
            col=[]
        cur.execute("SELECT column_name FROM information_schema.view_column_usage WHERE view_name = '"+ str(row[0]) +"'")
        sub_resp = cur.fetchall()
        for item in sub_resp:
            col.append(item[0])
        
        view.append(tb)
        view.append(col)
        to_d_view.append(view)      

    print to_d_view    

#Extracting the Constraints Info from database
def meta_crawl_constraints(con):
    cur = con.cursor()
    cons=[]
    to_d_cons=[]
    
    cur.execute("SELECT constraint_name, column_name, table_name "
                "FROM information_schema.constraint_column_usage")
    resp = cur.fetchall()

    for row in resp:
       cons=[]
       cons.append(row[0])
       cons.append(row[1])
       cons.append(row[2])
       to_d_cons.append(cons)
    
    print to_d_cons
    

#Extracting the Indexes Info from database
def meta_crawl_indexes(con):
    cur = con.cursor();    
    ind=[]
    to_d_ind=[]
    cur.execute("SELECT i.relname,t.relname,array_to_string(array_agg(a.attname), ', ') "
                "FROM pg_class t, pg_class i, pg_index ix, pg_attribute a "
                "WHERE t.oid = ix.indrelid and i.oid = ix.indexrelid and a.attrelid = t.oid and a.attnum = ANY(ix.indkey) and t.relkind = 'r' and t.relname like 'test%' "
                "GROUP BY t.relname, i.relname "
                "ORDER BY t.relname, i.relname")
    resp = cur.fetchall()

    for row in resp:
      ind=[]
      ind.append(row[0])
      ind.append(row[1])
      ind.append(row[2])
      to_d_ind.append(ind)

    print to_d_ind       


#Main
if __name__ == "__main__":
    script , database , user = argv
    con = create_connection(database, user)
    create_tables(con)        
    # insert_data(con)
    #show_tables(con)
    #table_name = meta_crawl_tables(con)
    #print table_name
    #meta_crawl_columns(con)
    # create_function(con)
    #func_test()
    #meta_crawl_functions(con)
    # create_trigger(con)
    #meta_crawl_triggers(con)
    # create_view(con)
    meta_crawl_views(con)
    #meta_crawl_constraints(con)
    # create_indexes(con)
    # meta_crawl_indexes(con)
    