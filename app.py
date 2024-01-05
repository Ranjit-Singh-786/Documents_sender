from flask import Flask,render_template,url_for,request
from doc_sender import send_docs
from datetime import datetime
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
            email_id = username

            data_item['name'] = student_name
            data_item['email'] = email_id
            data_item['file_path'] = file_path
            data.append(data_item)
        else:
            print(f"You have one mismatch file in this folder : {item}")
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
        content = str(request.form['body'])


        data = get_data_structure(folder_path=folder_path)

        sent_mail = send_docs(data=data,content=content,subject=subject)

        return render_template('final.html',sent_mails=sent_mail)
       

if __name__ == "__main__":
    app.run(host="0.0.0.0",port='8080',debug=True)