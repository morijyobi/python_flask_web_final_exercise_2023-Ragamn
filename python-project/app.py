from flask import Flask, render_template, request, url_for, redirect,session
import db
from datetime import timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/admin_menu', methods=['GET'])
def admin_menu():
  # session にキー：'user' があるか判定
  if 'user' in session:
    return render_template('admin_menu.html') # session があればmypage.html を表示
  else :
    return redirect(url_for('index')) # session がなければログイン画面にリダイレクト

@app.route('/login_form')
def login_form():
  return render_template('login.html')

@app.route('/login')
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
    return render_template('index.html',error=error,data=input_data)

@app.route('/logout')
def logout():
  session.pop('user', None) # session の破棄
  return redirect(url_for('index')) # ログイン画面にリダイレクト

if __name__ == '__main__':
    app.run(debug=True)