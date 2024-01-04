import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

LOG_DIRECTORY_NAME = "App logs"
os.makedirs(LOG_DIRECTORY_NAME,exist_ok=True)
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
FILE_NAME =f"log_{CURRENT_TIME_STAMP}.txt"
FILE_PATH = os.path.join(LOG_DIRECTORY_NAME,FILE_NAME)



def send_docs(data, content , subject):
    # Mail getting
    mails = pd.read_csv('mails_data.csv')
    mail = 0
    temp = 0
    sent_mail = []
    total_iteration = mails.shape[0]*10
    iteration_count = 0
    for student in data:
        if iteration_count <= total_iteration:
            break
        if (temp <= 10) and (mail < mails.shape[0]):
            forwarded_mail = []

            sender_email = mails.loc[mail]['Email']
            sender_password = mails.loc[mail]['Password']
            sender_name = mails.loc[mail]['Name']

            # Email content
            subjective = subject


            body = f"Dear {student['name']},\n\n {content}.\n\nBest Regards Team Upflairs,\n{sender_name} \nUpflairs Pvt. Ltd. Jaipur Rajasthan\n6350417917"

            # Creating the email message
            message = MIMEMultipart()
            message['From'] = f'{sender_name} <{sender_email}>'
            message['To'] = student['email']
            message['Subject'] = subjective

            # Attach the certificate file (replace 'certificate.pdf' with your actual file)
            with open(student['file_path'], 'rb') as attachment:
                part = MIMEText(body)
                message.attach(part)

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="certificate.png"')
                message.attach(part)

            iteration_count+=1
            # Connect to Gmail's SMTP server
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)

                    # Send the email
                    server.sendmail(sender_email, student['email'], message.as_string())
                    temp+=1  # for batch sending

                    forwarded_mail.append(student['name'])
                    forwarded_mail.append(student['email'])
                    sent_mail.append(tuple(forwarded_mail))

                    data_sent = student['name']+","+student['email']+'\n'
                    with open(FILE_PATH,'a+') as logfile:
                        logfile.write(data_sent)

            except Exception as e:  #  <-- identifie the error
                temp = 0 
                mail += 1

        else:
            temp = 0
            mail +=1

    return sent_mail
                    
            






