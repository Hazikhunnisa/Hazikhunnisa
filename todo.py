from flask import Flask,request,jsonify
import psycopg2
from psycopg2 import sql

app=Flask(__name__)



#database configuration
DB_HOST='localhost'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='2057'


def get_db_connection():
    connection=psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD

    )
    return connection


def create_tb_if_not_exist():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todo_db(
             task_id SERIAL PRIMARY KEY,
             titlename TEXT NOT NULL,
             description TEXT NOT NULL,
             duedate TEXT NOT NULL,
             priority text not null,
             status TEXT DEFAULT 'pending'
                   
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_tb_if_not_exist()

@app.route("/todo_register",methods=['post'])
def todo_register():
    titlename=request.json['titlename']
    description=request.json['description']
    duedate=request.json['duedate']
    priority=request.json['priority']
    status=request.json['status']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        INSERT INTO todo_db(titlename,description,duedate,priority,status)
        VALUES(%s,%s,%s,%s,%s)
    """,(titlename,description,duedate,priority,status))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"task done successfully"}),200

@app.route("/get_todo",methods=['GET'])
def get_todo():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
          SELECT*FROM todo_db;
                   
""")
    todo_db = cursor.fetchall()
    cursor.close()
    connection.close()
    result=[
         {"task_id":user[0],
          "titlename":user[1],"desciption":user[2],"duedate":user[3],"priority":user[4],"status":user[5]}for user in todo_db
    ]
    return jsonify(result),200

@app.route("/todo_update",methods=['PUT'])
def todo_update():
    task_id=request.args['task_id']
    titlename=request.json['titlename']
    description=request.json['description']
    duedate=request.json['duedate']
    priority=request.json['priority']
    status=request.json['status']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute(""" 
        UPDATE todo_db
                 SET titlename=%s, description =%s,duedate =%s,priority =%s, status=%s where task_id=%s;
""",(titlename,description,duedate,priority,status,task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"Information update successfully"}), 201

@app.route('/delete_todo',methods=['DELETE'])
def delete_todo():
    task_id=request.args.get('task_id')
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        DELETE FROM todo_db WHERE task_id=%s;
   """,(task_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"task deleted successfully"}),200

if __name__=='__main__':
    app.run(debug=True)

