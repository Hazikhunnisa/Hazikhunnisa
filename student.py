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
        CREATE TABLE IF NOT EXISTS student_db(
             student_id SERIAL PRIMARY KEY,
             studentname TEXT NOT NULL,
             coursename TEXT NOT NULL,
             coursecode TEXT NOT NULL,
             rollno TEXT NOT NULL,
             email TEXT NOT NULL      
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_tb_if_not_exist()

@app.route("/student_register",methods=['POST'])
def student_register():
    studentname=request.json['studentname']
    coursename=request.json['coursename']
    coursecode=request.json['coursecode']
    rollno=request.json['rollno']
    email=request.json['email']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        INSERT INTO student_db(studentname,coursename,coursecode,rollno,email)
        VALUES(%s,%s,%s,%s,%s)
    """,(studentname,coursename,coursecode,rollno,email))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"student registered successfully"}),200

@app.route("/get_student",methods=['GET'])
def get_student():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
          SELECT*FROM student_db;
                   
""")
    student_db = cursor.fetchall()
    cursor.close()
    connection.close()
    result=[
         {"student_id":student[0],
          "studentname":student[1],"coursename":student[2],"coursecode":student[3],"rollno":student[4],"email":student[5]}for student in student_db
    ]
    return jsonify(result),200

@app.route("/student_update",methods=['PUT'])
def student_update():
    student_id=request.args['student_id']
    studentname=request.json['studentname']
    coursename=request.json['coursename']
    coursecode=request.json['coursecode']
    rollno=request.json['rollno']
    email=request.json['email']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute(""" 
        UPDATE student_db
                 SET studentname=%s, coursename =%s, coursecode=%s, rollno=%s, email=%s where student_id=%s;
""",(studentname,coursename,coursecode,rollno,email,student_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"student update successfully"}), 201

@app.route('/delete_student',methods=['DELETE'])
def delete_student():
    student_id=request.args.get('student_id')
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        DELETE FROM student_db WHERE student_id=%s;
   """,(student_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"student deleted successfully"}),200

if __name__=='__main__':
    app.run(debug=True)

