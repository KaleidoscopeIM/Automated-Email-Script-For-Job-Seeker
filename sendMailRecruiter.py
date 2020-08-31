from email.mime.text import MIMEText
from smtplib import SMTP 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase 
from email import encoders 
from jinja2 import Environment, FileSystemLoader
import os
import json
import pandas as pd
from credentials import my_email_id,my_password
from datetime import datetime

def generate_email_html_content(data):
    content = json.loads(data)
    templateLoader = FileSystemLoader(searchpath="templates/")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template('emailHTML.html')
    rendered_template = template.render(content = content)
    return rendered_template
    
def send_email(to_id,subject,mail_content):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = my_email_id
    message['To'] = to_id
    # message['Cc'] = my_email_id
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email_id, my_password)
    try:  
        message.attach(MIMEText(mail_content, "html"))
        
        filename = "Gautam Saini - Resume.docx"
        resume = open(filename, "rb") 
        mBase = MIMEBase('application', 'octet-stream') 
        mBase.set_payload((resume).read()) 
        encoders.encode_base64(mBase) 
        mBase.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        message.attach(mBase)        
        
        email_body = message.as_string()        
        server.sendmail(my_email_id, to_id, email_body)
        print('Send email success:',to_id)
        server.quit()
        return "SUCCESS"
    except Exception:
        print('Error in sending email',Exception)
        return "FAILED"      
    
def startRoutine():
    tracker_cols = ['EmailSend','Status']
    df_tracker = pd.read_csv('emailTracking.csv',usecols=tracker_cols)
    df_tracker.reset_index(drop=True, inplace=True)
    
    df_processing = pd.read_csv('emailData.csv')
    #df_processing.rename(columns={'RecruiterEmail':'rEmail','RecruiterName':'rName','JobSkills':'js','JobTitle':'jt','CompanyName':'cName','CompanyLocation':'cLocation','AdditionalDetails':'aDetails'},inplace=True)
    df_processing.fillna('',inplace=True)
    df_email = df_processing[~df_processing['RecruiterEmail'].isin(df_tracker['EmailSend'])]
    totalSuccess = 0
    for index,aRow in df_email.iterrows():
        to = aRow['RecruiterEmail']
        subject = "Regarding " + aRow['JobTitle'] + " opening at " + aRow['CompanyName']
        html_email = generate_email_html_content(aRow.to_json())
       
        status = send_email(aRow['RecruiterEmail'],subject,html_email)
        if len(df_tracker.loc[df_tracker['EmailSend']== to,'Status'])==0:
            df_tracker = df_tracker.append({'EmailSend':to,'Status':status},ignore_index=True)
        else:
            df_tracker.loc[df_tracker['EmailSend']== to,'Status'] = status        

        if status == 'SUCCESS':
            totalSuccess += 1
    
    today = datetime.today()
    print("Total new email send ",today," :",totalSuccess)
    df_tracker.to_csv('emailTracking.csv')     
    
startRoutine()


