from playwright.sync_api import sync_playwright
import smtplib, os, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
from dotenv import load_dotenv  


load_dotenv() 


def send_whatsapp_message(text):
    account_sid = os.getenv('ACCT_SID')
    auth_token = os.getenv('AUTH')
    phone_number1 = os.getenv('PHONE_NUMBER_1')
    twilio_whatsapp_number = os.getenv('TWILIO_NUMBER')

    print("Twilio Account SID:", "SET" if account_sid else "NOT SET")
    print("Twilio Auth Token:", "SET" if auth_token else "NOT SET")
    print("Phone Number 1:", phone_number1)
    print("Twilio WhatsApp Number:", twilio_whatsapp_number)


    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body=text,
            from_=twilio_whatsapp_number,
            to =phone_number1
        )
    print(f'Message sent to {phone_number1} with SID: {message.sid}')





def send_emma_whatsapp_message(text):
    account_sid = os.getenv('ACCT_SID')
    auth_token = os.getenv('AUTH')
    
    phone_number2 = os.getenv('PHONE_NUMBER_2')
    twilio_whatsapp_number = os.getenv('TWILIO_NUMBER')

    print("Twilio Account SID:", "SET" if account_sid else "NOT SET")
    print("Twilio Auth Token:", "SET" if auth_token else "NOT SET")
    print("Phone Number 2:", "SET" if phone_number2 else "NOT SET")
    print("Twilio WhatsApp Number:", "SET" if twilio_whatsapp_number else "NOT SET")
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body=text,
            from_=twilio_whatsapp_number,
            to=phone_number2
        )
    print(f'Message sent to {phone_number2} with SID: {message.sid}')




def notify_mail(text):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    password = os.getenv('EMAIL_PASSWORD')
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL').split(',')

    if not password or not sender_email or not receiver_email:
        print("Environment variables for email are not set properly.")
        return

    subject = "Hello"
    body = text

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ",".join(receiver_email)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)

        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()


def check_result():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        studentID = os.getenv('STUDENT_ID')
        print(studentID)
        password = os.getenv('PORTAL_PASSWORD')
        print(password)

        if not studentID or not password:
            print("Student ID or portal password environment variables are not set.")
            return

        try:
            page.goto('https://portal.unilorin.edu.ng/', timeout=60000)
            
            studentID_input = page.get_by_label('Staff/Student ID')
            password_input = page.get_by_label("Password", exact=True)
            login = page.get_by_text("LOGIN")

            studentID_input.fill(studentID)
            password_input.fill(password)
            login.click()

        except TimeoutError:
            print('Ignoring timeout')

        time.sleep(10)

        try:
            


            page.goto('https://portal.unilorin.edu.ng/student/my-results', timeout=60000)
           
            page.wait_for_selector('text=2022/2023 Second Semester Semester Result')
            
            # content = page.content()
            # if page.locator('text=CPE341').count() > 0:
            #     text = 'Your result has been released. CPE341'
            #     print(text)
            #     send_whatsapp_message(text)
            #     notify_mail(text)
            if page.locator('text=CPE342').count() > 0:
                text = 'ALL YOUR RESULTS HAVE BEEN RELEASED'
                print(text)
                send_whatsapp_message(text)
                send_emma_whatsapp_message(text)
                notify_mail(text)
            else:
                text = "THERE'S NO NEW RESULT ON YOUR PORTAL"
                # send_emma_whatsapp_message(text)
                # send_whatsapp_message(text)
                # notify_mail(text)
                print(text)
            
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            browser.close()

check_result()