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
import sys 
import git

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

def send_self_summary_mail(sCount, fCount, slist, fList):
    message = MIMEMultipart()
    message['Subject'] = "Job hunting summary:: " + str(datetime.today())
    message['From'] = my_email_id
    message['To'] = my_email_id
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email_id, my_password)
    email_body = ""
    email_body += "\n\n------ Total mail send success ------ :: "+str(sCount)
    email_body += "\n\nSuccess emails :: "
    for a in slist:
        email_body += a 
        email_body += "\n"
    email_body += "\n\n------ Total mail send failed ------ :: "+str(fCount)
    email_body += "\n\nFailed emails :: "
    for a in fList:
        email_body += a 
        email_body += "\n"
    email_body += "\n\n-------------------------------------------- "
    message.attach(MIMEText(email_body, 'plain'))
    final_body = message.as_string()
    server.sendmail(my_email_id, my_email_id, final_body)
    server.quit()
    
def startRoutine(env):
    tracker_cols = ['EmailSend','Status']
    df_tracker = pd.read_csv('emailTracking.csv',usecols=tracker_cols)
    df_tracker.reset_index(drop=True, inplace=True)
    
    if env == "SERVER":
        df_processing = pd.read_csv('emailData.csv')
    else:
        df_processing = pd.read_csv('localEmailTestData.csv')
    
    #df_processing.rename(columns={'RecruiterEmail':'rEmail','RecruiterName':'rName','JobSkills':'js','JobTitle':'jt','CompanyName':'cName','CompanyLocation':'cLocation','AdditionalDetails':'aDetails'},inplace=True)
    df_processing.fillna('',inplace=True)
    df_email = df_processing[~df_processing['RecruiterEmail'].isin(df_tracker['EmailSend'])]
    totalSuccess = 0
    totalFail = 0
    totalSuccessEmail = []
    totalFailEmail = []
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
            totalSuccessEmail.append(to)
            totalSuccess += 1
        else:
            totalFail += 1
            totalFailEmail.append(to)
    
    today = datetime.today()
    send_self_summary_mail(totalSuccess,totalFail,totalSuccessEmail,totalFailEmail)
    print("Total new email send ",today," :",totalSuccess)
    df_tracker.to_csv('emailTracking.csv')     
    
if __name__ == "__main__":
    env = ""
    if len(sys.argv) >=2 and sys.argv[1] == 'SERVER': # if server then refresh codes before executing
        repo = git.Repo('./')
        repo.remotes.origin.pull()
        env = "SERVER"
        print('Git pull success')
    startRoutine(env)
    
