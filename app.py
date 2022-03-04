from flask import Flask, render_template, request
import numpy as np
import cv2
from keras.models import load_model
import webbrowser

language =''
prediction=''

english_happy={'song1':'Blinding Lights','link1':'https://youtu.be/fHI8X4OXluQ',
'song2':'Uptown Funk','link2':'https://youtu.be/CeYuFSBkkVw ',
'song3':'Lean On (feat. MØ)','link3':'https://youtu.be/rn9AQoI7mYU',
'song4':'Sia - Cheap Thrills','link4':'https://youtu.be/MBYfs0y5r-c ',
'song5':'Doja Cat ','link5':'https://youtu.be/F9wklh1vwWk'}

tamil_happy={'song1':'Arabic Kuthu','link1':'https://youtu.be/8FAUEv_E_xQ ',
'song2':'Vedalam - Aaluma Doluma ','link2':'https://youtu.be/2ogKpj5QuSY',
'song3':'Oo Solriya..Oo Oo Solriy','link3':'https://youtu.be/3Tnf9AxEtnc',
'song4':'jingila mani','link4':'https://youtu.be/fAcmG2NKx2E',
'song5':'Pokkiri','link5':'https://youtu.be/CKRCyEy_DIA '}

hindi_happy={'song1':'Dilli Wali Girlfriend','link1':'https://youtu.be/yTRNFrUBu58',
'song2':'Badtameez Dil  ','link2':'https://youtu.be/II2EO3Nw4m0 ',
'song3':'Queen: London Thumakda','link3':'https://youtu.be/udra3Mfw2oo ',
'song4':'Kamariya ','link4':'https://youtu.be/i0_m90T04uw',
'song5':'Laila Main Laila','link5':'https://youtu.be/jE4-tKSYScQ'}

malayalam_happy={'song1':'Love Action Drama','link1':'https://youtu.be/1KpTXAsNpaM ',
'song2':'Velmuruka Harohara','link2':'https://youtu.be/Ppo3oPo4NYw',
'song3':'Pathinalam Ravinte','link3':'https://youtu.be/eZkVkknmnyk ',
'song4':'PUTHIYA MUGAM ','link4':'https://youtu.be/B-MJralHWU8 ',
'song5':'Moha Mundiri','link5':'https://youtu.be/usk3Yt0j14A '}

english_sad={'song1':' Easy On Me','link1':'https://youtu.be/OT2YRfvOHAk ',
'song2':'Wrecked','link2':'https://youtu.be/CqKZM9JMJls',
'song3':'Faith Healer','link3':'https://youtu.be/Zm3fwahQiO8 ',
'song4':' Meaningless ','link4':'https://youtu.be/m84nAryISmo',
'song5':' Medicine','link5':'https://youtu.be/NpgLo5xUesA '}

tamil_sad={'song1':'Po Nee Po','link1':'https://youtu.be/DnyA_qEbTpw',
'song2':'Unna Nenachu_Pyscho','link2':'https://youtu.be/uuooYJoC6gk',
'song3':' Maruvaarthai ','link3':'https://youtu.be/N8vIvL0JV7g ',
'song4':'Ennodu Nee Irundhaal','link4':'https://youtu.be/EhhiY11Z9-U',
'song5':'Pona Poagattum ','link5':'https://youtu.be/zJOGWMiLqys'}

hindi_sad={'song1':'Allah Waariya','link1':'https://youtu.be/Jcr9afnpbQg',
'song2':'Mann Bharryaa','link2':'https://youtu.be/1poXN3jF3Bw',
'song3':'Tum Hi Ho Aashiqui 2','link3':'https://youtu.be/IJq0yyWug1k',
'song4':'AGAR TUM SAATH HO','link4':'https://youtu.be/xRb8hxwN5zc',
'song5':'Kun Faya Kun','link5':'https://youtu.be/T94PHkuydcw '}

malayalam_sad={'song1':'Mizhiyoram','link1':'https://youtu.be/acAMgv0ZOy4',
'song2':'Arike Ninna','link2':'https://youtu.be/yCxwpUdgFsM',
'song3':'Big B','link3':'https://youtu.be/-luwCHXknxw ',
'song4':' Uyire  ','link4':'https://youtu.be/Fd7-FybJlbs ',
'song5':'Akashamayavale','link5':'https://youtu.be/Ri_0ow-JOFY '}


english_fear={'song1':'Everything At Once ','link1':'https://youtu.be/VIetJT4QY6A ',
'song2':'Killing Me ','link2':'https://youtu.be/qZ-yYiaNjWw',
'song3':'Only Reason','link3':'https://youtu.be/j6lNI-aAJBw ',
'song4':'Ye ','link4':'https://youtu.be/vPtAjfyXvEo',
'song5':'Real Life','link5':'https://youtu.be/f0V3th5Rttk'}

tamil_fear={'song1':'Ra Ra','link1':'https://youtu.be/z1BpwFb0YLo',
'song2':'Party With The Pei','link2':'https://youtu.be/mLaVG3hf5Wg',
'song3':' Kodiavanin Kathaya  ','link3':'https://youtu.be/AKz8TUrUZN8 ',
'song4':'Poochandi','link4':'https://youtu.be/6DxBhGv3rFY',
'song5':'Mirutha Mirutha','link5':'https://youtu.be/pNCk142fq0A'}

hindi_fear={'song1':'Lag Jaa Gale','link1':'https://youtu.be/TFr6G5zveS8',
'song2':'Gumnaam Hai Koi','link2':'https://youtu.be/Kjyr9JYd3-I',
'song3':'Mera Saaya Saath Hoga','link3':'https://youtu.be/IB1gg-F0eZY',
'song4':'Aaja Re Pardesi Main','link4':'https://youtu.be/Mm21SSgUHe8',
'song5':'Aayega Aanewala','link5':'https://youtu.be/e24S6d4e3QA '}

malayalam_fear={'song1':'Minnaminuge','link1':'https://youtu.be/9_HXUzSkHo0',
'song2':'Nilaavinte Poonkaavil','link2':'https://youtu.be/eiH1db-uDxg',
'song3':'Oru Murai Vande','link3':'https://youtu.be/DMeE6Q8YrGI',
'song4':'Puthumazhayay Vannoo  ','link4':'https://youtu.be/8g87zvT-Upc ',
'song5':'Nizhalai Ozhuki Varum Njan','link5':'https://youtu.be/CnMfzzCQj3g '}


english_surprise={'song1':'Let Me Love You','link1':'https://youtu.be/SMs0GnYze34 ',
'song2':'It Aint Me','link2':'https://youtu.be/j6sSQq7a_Po',
'song3':'Sorry ','link3':'https://youtu.be/BerNfXSuvJ0 ',
'song4':' Closer ','link4':'https://youtu.be/25ROFXjoaAU',
'song5':'Dance Monkey','link5':'https://youtu.be/1__CAdTJ5JU '}

tamil_surprise={'song1':'Single Pasanga','link1':'https://youtu.be/gsJO5EgOZdo',
'song2':'Vengamavan ','link2':'https://youtu.be/ECV3Jck-Dt8',
'song3':' Rettai Kathirae ','link3':'https://youtu.be/Bjx7Bo5jWwo ',
'song4':'Vadi pulla','link4':'https://youtu.be/i_Wk3fL2WJw',
'song5':'Clubble Mubble','link5':'https://youtu.be/NZME5AUKFhg'}

hindi_surprise={'song1':'440 volt','link1':'https://youtu.be/eb3WdD22JIA',
'song2':'Hor Nach ','link2':'https://youtu.be/rXhZCFgyt2Y',
'song3':'Kajra re ','link3':'https://youtu.be/xiX9E7atp_w',
'song4':'Bin Sajni Ke Jeevan','link4':'https://youtu.be/X_roGNo3daA',
'song5':'Pyar Ki','link5':'https://youtu.be/0cGsi3MJ66s'}

malayalam_surprise={'song1':'Rafthara Song','link1':'https://youtu.be/Yotz3CI6XDU',
'song2':'Thakilu Pukilu','link2':'https://youtu.be/FbsTS7sNxZY',
'song3':'Lailakame','link3':'https://youtu.be/28kVscO2dB8 ',
'song4':' Oru vallam ponnum poovum  ','link4':'https://youtu.be/wvJfxBrs3cs ',
'song5':'CHALAKUDI CHANTHAKU POKUMBOL','link5':'https://youtu.be/DpsiMrMzTP0'}


english_anger={'song1':'Faust','link1':'https://youtu.be/p32jNYGDCAM ',
'song2':'Bloody Valentine','link2':'https://youtu.be/yrwUN-iNLs4',
'song3':'Enter Sandman ','link3':'https://youtu.be/riLJwQ9PqKM ',
'song4':'21st Century Vampire ','link4':'https://youtu.be/Mh2roxsgYag',
'song5':'Back From The Dead','link5':'https://youtu.be/_H37Hh49B6U '}

tamil_anger={'song1':'Bairavaa','link1':'https://youtu.be/9sVbL2vXt1s',
'song2':'Dheera Dheera ','link2':'https://youtu.be/gWcILbCt1zA',
'song3':' Blood Bath  ','link3':'https://youtu.be/x7qwz_1TjLk ',
'song4':'Top Tucker','link4':'https://youtu.be/MweJ-X_COUo',
'song5':'Chinnavaru Sirapputhan','link5':'https://youtu.be/dTvYUJ0vzqQ'}

hindi_anger={'song1':'Brothers Anthem','link1':'https://youtu.be/_NHqpyn5f0E',
'song2':'Challa ','link2':'https://youtu.be/g62J-8nV5FI',
'song3':'Sultan ','link3':'https://youtu.be/abiL84EAWSY',
'song4':'Ziddi Dil Full ','link4':'https://youtu.be/puKD3nkB1h4',
'song5':'Get Ready to fight','link5':'https://youtu.be/lLlkZhsESgc'}

malayalam_anger={'song1':'Kalippu | Premam','link1':'https://youtu.be/PeUjir1kMFM ',
'song2':'Path Of Lakshmana','link2':'https://youtu.be/z9RO8MJ8k7A',
'song3':' Kadavule Pole','link3':'https://youtu.be/HxghNgeC-NE ',
'song4':' Parudeesa  ','link4':'https://youtu.be/O_ZIs4p14Fo ',
'song5':'Kodikayarana Pooramai','link5':'https://youtu.be/xOEFMEOvgCc'}


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

info = {}

haarcascade = "haarcascade_frontalface_default.xml"
label_map = ['Anger', 'Neutral', 'Fear', 'Happy', 'Sad', 'Surprise']
print("+"*50, "loadin gmmodel")
model = load_model('model.h5')
cascade = cv2.CascadeClassifier(haarcascade)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/emotion_detect', methods=["POST"])
def emotion_detect():
	global language,prediction
	language = request.form['language']

	found = False

	cap = cv2.VideoCapture(0)
	while not(found):
		_, frm = cap.read()
		gray = cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)

		faces = cascade.detectMultiScale(gray, 1.4, 1)

		for x,y,w,h in faces:
			found = True
			roi = gray[y:y+h, x:x+w]
			cv2.imwrite("static/face.jpg", roi)

	roi = cv2.resize(roi, (48,48))

	roi = roi/255.0
	
	roi = np.reshape(roi, (1,48,48,1))

	prediction = model.predict(roi)

	print(prediction)

	prediction = np.argmax(prediction)
	prediction = label_map[prediction]

	cap.release()
	return render_template("emotion_detect.html", data=prediction)

@app.route('/song_predict', methods=["GET","POST"])
def song_predict():
	if language=='english' and prediction=='Happy':
		return render_template("song_predict.html", data=english_happy)
	if language=='hindi' and prediction=='Happy':
		return render_template("song_predict.html", data=hindi_happy)
	if language=='tamil' and prediction=='Happy':
		return render_template("song_predict.html", data=tamil_happy)
	if language=='malayalam' and prediction=='Happy':
		return render_template("song_predict.html", data=malayalam_happy)



	if language=='english' and prediction=='Sad':
		return render_template("song_predict.html", data=english_sad)
	if language=='hindi' and prediction=='Sad':
		return render_template("song_predict.html", data=hindi_sad)
	if language=='tamil' and prediction=='Sad':
		return render_template("song_predict.html", data=tamil_sad)
	if language=='malayalam' and prediction=='Sad':
		return render_template("song_predict.html", data=malayalam_sad)



	if language=='english' and prediction=='Neutral':
		return render_template("song_predict.html", data=english_happy)
	if language=='hindi' and prediction=='Neutral':
		return render_template("song_predict.html", data=hindi_happy)
	if language=='tamil' and prediction=='Neutral':
		return render_template("song_predict.html", data=tamil_happy)
	if language=='malayalam' and prediction=='Neutral':
		return render_template("song_predict.html", data=malayalam_happy)
	


	if language=='english' and prediction=='Fear':
		return render_template("song_predict.html", data=english_fear)
	if language=='hindi' and prediction=='Fear':
		return render_template("song_predict.html", data=hindi_fear)
	if language=='tamil' and prediction=='Fear':
		return render_template("song_predict.html", data=tamil_fear)
	if language=='malayalam' and prediction=='Fear':
		return render_template("song_predict.html", data=malayalam_fear)
	


	if language=='english' and prediction=='Surprise':
		return render_template("song_predict.html", data=english_surprise)
	if language=='hindi' and prediction=='Surprise':
		return render_template("song_predict.html", data=hindi_surprise)
	if language=='tamil' and prediction=='Surprise':
		return render_template("song_predict.html", data=tamil_surprise)
	if language=='malayalam' and prediction=='Surprise':
		return render_template("song_predict.html", data=malayalam_surprise)
	

	if language=='english' and prediction=='Anger':
		return render_template("song_predict.html", data=english_anger)
	if language=='hindi' and prediction=='Anger':
		return render_template("song_predict.html", data=hindi_anger)
	if language=='tamil' and prediction=='Anger':
		return render_template("song_predict.html", data=tamil_anger)
	if language=='malayalam' and prediction=='Anger':
		return render_template("song_predict.html", data=malayalam_anger)


	return render_template("song_predict.html", data=english_happy)

if __name__ == "__main__":
	app.run(debug=True)
