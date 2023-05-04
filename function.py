import smtplib
from email.message import EmailMessage

def send_email(subject, body_text, mail_to, mail_from = None, from_user= None, to_user= None):

    USERNAME = "no.reply.xxxxxxx@gmail.com"
    PASSWORD = 'xxxxyyyyzzzzqqqq'
    EMAIL_HOST = "smtp.gmail.com"
    PORT = 587

    if mail_from is None: mail_from = USERNAME
    if to_user is None: to_user = ""
    if from_user is None: from_user = "ABC Company"

    message = """From: %s\nTo: %s\nnSubject: %s\n\n%s""" % (mail_from, mail_to, subject, body_text)
    print (message)

    body = f"""\
            <html>
              <body>
                <p>Hi {to_user},<br><br>
                   Hope You are doing well?<br><br>
                   {body_text}
                </p>
                <p>
                    Thanks & Regards <br>
                    {from_user}
                </p>
              </body>
            </html>
            """

   
    
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = mail_from
    email['To'] = mail_to
    email.set_content(body, subtype='html')

    try:
        server = smtplib.SMTP(EMAIL_HOST, PORT)
        server.ehlo()
        server.starttls()
        server.login(USERNAME, PASSWORD)
        # server.sendmail(mail_from, mail_to, message)
        server.send_message(email)
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False

def lambda_handler(event, context):
    
    print("event ====================================")
    print(event)
    
    records = event["Records"]

    
    for record in records:

        event_name = record["eventName"]
        print("eventName ====================================")
        print(event_name)
        
        if(event_name == "INSERT"):
            dynamodbData = record["dynamodb"]["NewImage"]
        
            print("data ====================================")
            print(get_field_value(dynamodbData, 'ToEmailId'))
            
            mail_from = get_field_value(dynamodbData, 'FromEmailId')
            mail_to = get_field_value(dynamodbData, 'ToEmailId')     # separate multiple recipient by comma. eg: "abc@gmail.com, xyz@gmail.com"
        
            subject = get_field_value(dynamodbData, 'Subject') 
            body_text = get_field_value(dynamodbData, 'Message') 
            from_user = get_field_value(dynamodbData, 'FromUser')
            to_user = get_field_value(dynamodbData, 'ToUser')
            
            print("mail_from: " + mail_from)
            print("mail_to: " + mail_to)
            
            if(mail_from != "" and mail_to != ""):
                print("yes: " )
         
                send_email(subject, body_text, mail_to, mail_from, from_user, to_user)
        

    # mail_from = "adritasharma@gmail.com"
    # mail_to = "adritasharma7@gmail.com"     # separate multiple recipient by comma. eg: "abc@gmail.com, xyz@gmail.com"

    # subject = "Documents Requested"
    # body_text = "Please Share the documents"
    # from_user = "Adrita Sharma"
    # to_user = "Riya Chakraborty"

    # return send_email(subject, body_text, mail_to, mail_from, from_user, to_user)
    return True
    
    
def get_field_value(item_dict, field_name):
    value = item_dict.get(field_name)
    if value is None:
        return ""
    else:
        return value["S"]