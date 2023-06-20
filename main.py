from flask import Flask,render_template,session,request,redirect,url_for
from flask_socketio import SocketIO,send
from time import strftime

app = Flask(__name__)
app.secret_key="once upon a time there lived a gost"
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def msg(message):
	try:
		l=message.split(":")
		t=strftime('%H:%M')
		s=f'''<div class="card bg-dark text-light" style="width:20rem;">
	          <div class='card-body'>
	            <h4 class='card-title' style="display:inline;">{l[0]}</h4>
	            <h6 class='card-title' style="display:inline;">,{t}</h6>
	            <p class="card-text">{l[1]}</p>
	          </div><br>'''
		if message=='user connected':
			print('new user connected')
		else:
			send(s,broadcast=True)
			print(t+' log : '+l[0]+" : "+l[1])
	except:
		pass
	
@app.route('/',methods=['GET','POST'])
def index():
	if request.method=="POST":
		session['name']=request.form['name']
		return redirect(url_for('chat'))
	return render_template('index.html')

@app.route('/chat',methods=['GET','POST'])
def chat():
	return render_template('chatroom.html',name=session['name'])

if __name__=='__main__':
	socketio.run(app,debug=True,host="0.0.0.0",port=8000)