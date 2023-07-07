from flask import Flask, render_template, request, url_for, redirect,session
import db,string,random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/')
def index():
  msg = request.args.get('msg')
  
  if msg == None:
    return render_template('index.html')
  else:
    return render_template('index.html',msg=msg)
  
#クイズ選択画面
@app.route('/form')
def form():
    return render_template('form.html')

#管理者メニュー
@app.route('/admin_menu', methods=['GET'])
def admin_menu():
  # session にキー：'user' があるか判定
  if 'user' in session:
    return render_template('admin_menu.html')
  else :
    return redirect(url_for('login_form'))

#ログイン画面
@app.route('/login_form')
def login_form():
  return render_template('login.html')

#ログイン動作
@app.route('/login', methods=['POST'])
def login():
  user_name = request.form.get('username')
  password = request.form.get('password')
  
  # ログイン判定
  if db.login(user_name, password):
    session['user'] = True # session にキー：'user', バリュー:True を追加
    session.permanent = True # session の有効期限を有効化
    app.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を5 分に設定
    return redirect(url_for('admin_menu'))
  else :
    error = 'ログインに失敗しました。'
    # dictで返すことでフォームの入力量が増えても可読性が下がらない。
    input_data = {
      'user_name':user_name,
      'password':password
      }
    return render_template('login.html',error=error,data=input_data)

#ログアウト
@app.route('/logout')
def logout():
  session.pop('user', None) # session の破棄
  return redirect(url_for('index')) # ログイン画面にリダイレクト

#管理者登録画面
@app.route('/register')
def register_form():
    return render_template('register.html')

#管理者登録
@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('register.html', error=error)

@app.route('/register_quiz_form')
def register_quiz_form():
  if 'user' in session:
    return render_template('register_quiz_form.html')
  else :
    return redirect(url_for('login_form'))
  
@app.route('/register_quiz' , methods=['POST'])
def register_quiz():
  quiz_name = request.form.get('quiz_name')
  answer = request.form.get('answer')
  
  count = db.insert_quiz(quiz_name,answer)
  
  if count == 1:
    return redirect(url_for('admin_menu'))
  else:
    error = '登録に失敗しました'
    return render_template('register_quiz_form.html', error=error)

@app.route('/list')
def list():
  quiz_list = db.quiz_list()
  return render_template('quiz_list.html',quizzes=quiz_list)

if __name__ == '__main__':
    app.run(debug=True)