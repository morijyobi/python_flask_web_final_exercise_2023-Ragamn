import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset,k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password  = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1000).hex()
    return hashed_password

def login(user_name,password):
  sql = 'SELECT hashed_password,salt FROM quiz_admin WHERE name = %s'
  flg = False
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(user_name,))
    user = cursor.fetchone()
    if user != None:
      # SQLの結果からソルトを取得
      salt = user[1]
      
      # DBから取得したソルト+ 入力したパスワードからハッシュ値を取得
      hashed_password = get_hash(password, salt)
      
      # 生成したハッシュ値とDBから取得したハッシュ値を比較する
      if hashed_password == user[0]:
        flg = True
  except psycopg2.DatabaseError :
    flg = False
  finally :
    cursor.close()
    connection.close()
  return flg

def insert_user(user_name,password):
    sql = 'INSERT INTO quiz_admin VALUES(default, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password,salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count
  
def insert_quiz(picture,answer1,answer2,answer3,answer4,answer):
    sql = 'INSERT INTO quiz VALUES(default,%s, %s,%s,%s,%s,%s,default)'
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (picture, answer1,answer2,answer3,answer4,answer))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count

def quiz_list():
  sql = 'SELECT * FROM quiz WHERE delete_flg = FALSE ORDER BY id ASC'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    
  finally :
    cursor.close()
    connection.close()
  return list

def select_quiz(id):
  sql = 'SELECT * FROM quiz WHERE id = %s'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(id,))
    quiz = cursor.fetchone()
      
  finally :
    cursor.close()
    connection.close()
    
  return quiz

def update_quiz(id,picture,answer1,answer2,answer3,answer4,answer):
  sql = 'UPDATE quiz SET picture_path = %s,answer1 = %s,answer2 = %s,answer3 = %s,answer4 = %s,answer = %s WHERE id = %s'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(picture, answer1,answer2,answer3,answer4,answer,id))
    count = cursor.rowcount #更新件数取得
    connection.commit()
    
  except psycopg2.DatabaseError :
    count = 0
    
  finally :
    cursor.close()
    connection.close()
    
  return count

def delete_quiz(id):
  sql = 'UPDATE quiz SET delete_flg = TRUE WHERE id = %s'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(id,))
    count = cursor.rowcount #更新件数取得
    connection.commit()
    
  except psycopg2.DatabaseError :
    count = 0
    
  finally :
    cursor.close()
    connection.close()
    
  return count

def count_id():
  sql = 'SELECT count(id) FROM quiz'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    count_num = cursor.fetchone()
      
  finally :
    cursor.close()
    connection.close()
    
  return count_num

def select_quiz_answer(id):
  sql = 'SELECT picture_path,answer1,answer2,answer3,answer4,answer FROM quiz WHERE id = %s AND delete_flg = FALSE'
  
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(id,))
    quiz = cursor.fetchone()
      
  finally :
    cursor.close()
    connection.close()
    
  return quiz