from flask import Flask,render_template,url_for,request
from doc_sender import send_docs
from logger import logging
import os


def get_data_structure(folder_path):
    list_of_items = os.listdir(folder_path)

    data = []
    
    for item in list_of_items:
        if item.endswith("png"):
            data_item = dict()
            student_name , user_name = item.split('-')
            file_path = os.path.join(folder_path,item)

            #username editing
            username = user_name[0:-4]
            email_id = username+"@gmail.com"

            data_item['name'] = student_name
            data_item['email'] = email_id
            data_item['file_path'] = file_path
            data.append(data_item)
        else:
            print(f"Keep This file in another folder {item}")
    logging.info("Successfully Get The Data From Direcotry !!")
    return data



app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')


@app.route('/help',methods=['GET','POST'])
def help():
    return render_template('help.html')


@app.route('/send',methods=['GET','POST'])
def send():
    if request.method == 'POST':
        
        folder_path = str(request.form['folder_path'])
        subject = str(request.form['subject'])
        body = str(request.form['body'])


        data = get_data_structure(folder_path=folder_path)

        sent_mail = []
        for student in data:
            forwarded_mail = []
            send_docs(student_name=student['name'], student_email=student['email'], file_path=student['file_path'])
            logging.info(f"Sent :- {student['name']}  --> {student['email']}")
            forwarded_mail.append(student['name'])
            forwarded_mail.append(student['email'])
            sent_mail.append(tuple(forwarded_mail))

        return render_template('final.html',sent_mails=sent_mail)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port='8080',debug=True)