from flask import Flask, render_template, request, url_for, redirect,session
import db,string,random,os
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))
UPLOAD_FOLDER = 'C:/Users/riki/github-classroom/morijyobi/python_flask_web_final_exercise_2023-Ragamn/python-project/static/images'


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
    quiz_list = db.quiz_list()
     
    return render_template('quiz_list.html',quizzes=quiz_list,name='images/')
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
  answer1 = request.form.get('answer1')
  answer2 = request.form.get('answer2')
  answer3 = request.form.get('answer3')
  answer4 = request.form.get('answer4')
  answer = request.form.get('answer')
   # アップロードされたファイルをrequestから取得
  file = request.files['file']
   # ../../a.jpgみたいな名前のファイルへの対策(ディレクトリトラバーサル攻撃)
  # 不要な文字列を削除します。(なお、日本語も削除されちゃいます....)
  # ファイルを保存
  name = secure_filename(file.filename)
  file.save(os.path.join(UPLOAD_FOLDER, name))
  
  count = db.insert_quiz(name,answer1,answer2,answer3,answer4,answer)
  
  if count == 1:
    return redirect(url_for('admin_menu'))
  else:
    error = '登録に失敗しました'
    return render_template('register_quiz_form.html', error=error)

# @app.route('/list')
# def list():
#   quiz_list = db.quiz_list()
  
#   return render_template('quiz_list.html',quizzes=quiz_list,name='images/')

@app.route('/edit',methods=['POST'])
def edit():
  id = request.form.get('id')
  quiz = db.select_quiz(id)
  return render_template('quiz_edit.html',quiz=quiz) 
  
@app.route('/update_quiz',methods=['POST'])
def update_quiz():
  id = request.form.get('id')
  answer1 = request.form.get('answer1')
  answer2 = request.form.get('answer2')
  answer3 = request.form.get('answer3')
  answer4 = request.form.get('answer4')
  answer = request.form.get('answer')
   # アップロードされたファイルをrequestから取得
  file = request.files['file']
   # ../../a.jpgみたいな名前のファイルへの対策(ディレクトリトラバーサル攻撃)
  # 不要な文字列を削除します。(なお、日本語も削除されちゃいます....)
  # ファイルを保存
  name = secure_filename(file.filename)
  file.save(os.path.join(UPLOAD_FOLDER, name))
  db.update_quiz(id,name,answer1,answer2,answer3,answer4,answer)
  return render_template('quiz_list.html')

@app.route('/delete_quiz',methods=['POST'])
def delete_quiz():
  id = request.form.get('id')
  db.delete_quiz(id)
  return render_template('quiz_list.html')

@app.route('/quiz_answer',methods=['get'])
def quiz_answer():
  num = int(request.args.get('question_num'))
  random_num = db.count_id()
  criterion = 0
  session['id'] = []
  session['answer'] = []
  i = []
  while criterion < num  and len(session['id']) <= num:
    q_id = random.randrange(0,random_num[0]) + 1
    quiz=(db.select_quiz_answer(q_id))
    if not q_id in session['id'] and quiz != None:
      session['id'].append(q_id)
      session['answer'].append(quiz)
      quiz = None
      i.append(criterion)
      criterion += 1
  return render_template('quiz_answer_form.html',name='images/',num=num,i=i)

@app.route('/answer_check',methods=['post'])
def answer_check():
  session['u_answer'] = []
  session['result'] = []
  num = int(request.form.get('num'))
  criterion = []
  i = 0
  count = 0
  while i < num:
    session['u_answer'].append(request.form.get('u_answer'+str(i)))
    if session['answer'][i][5] == session['u_answer'][i]:
      session['result'].append('〇正解')
      count +=1 
    else:
      session['result'].append('✕不正解あなたの答えは'+session['u_answer'][i])
    criterion.append(i)
    i +=1
    
  return render_template('check.html',criterion=criterion,name='images/',count=count,num=num)

@app.route('/back')
def 完了():
  session.pop('id', None) # session の破棄
  session.pop('answer', None) # session の破棄
  session.pop('u_answer', None) # session の破棄
  session.pop('result', None) # session の破棄
  return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)