import smtplib
import email.message
import praw
from pprint import pprint
from pyowm import OWM

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header



## CONFIG ##

#EMAIL
server = 'smtp.gmail.com'
port = 587
password = '*b$I609NxBGZLHAT'
email_login = 'jarredkelly@gmail.com'
from_email = 'jarredkelly@gmail.com'
to_email = 'jkelly@stellarbpo.com.au'

# WEATHER
weather_api = '4289b40458387dddb8c6d05b98fec118'

# REDDIT
reddit_secret = 'PFDicp7xkuZ5igpxO6wcDW0on1o'
reddit_client = '5SRsxjvqXzhjjQ'
num_submissions = 5



## CODE ##
def sendEmail(subject, body):
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    msg.add_header('Content-Type', 'text/html; charset=utf-8')
    
    msg.set_payload(body)
    
    smtpObj = smtplib.SMTP(server, port)
    
    smtpObj.starttls()
    smtpObj.login(email_login, password)
    smtpObj.sendmail(msg['From'], msg['To'], msg.as_string().encode("utf8"))
    
    smtpObj.quit()


def getWeather(location):
    owm = OWM(weather_api)
    obs = owm.weather_at_place(location)
    w = obs.get_weather()
    #print(w.get_temperature(unit='celsius'))
    temps = w.get_temperature(unit='celsius')
    curr_temp = temps['temp']
    min_temp = temps['temp_min']
    max_temp = temps['temp_max'] 
    humidity = w.get_humidity()
    status = w.get_detailed_status()
    output = ("Current Temp:\t%.1f\nMin Temp:\t%.1f\nMax Temp:\t%.1f\nHumidity:\t%.1f\n%s"
        % (curr_temp, min_temp, max_temp, humidity, status))
    return output

def getReddit(sub):
    output = "Top 10 Posts from /r/%s:<ul>" % (sub)
    
    reddit = praw.Reddit(client_id=reddit_client, client_secret=reddit_secret, 
                        user_agent='Jared')
    
    for submission in reddit.subreddit(sub).hot(limit=num_submissions):
        output += "<li>" + " - [<a href='" + submission.url + "'>link</a>] " + submission.title + "</li>"
        
    output += "</ul>"
    return output

#sendEmail("subject", "body")


output = getReddit('worldnews')
output += getWeather('brisbane,australia')

sendEmail("test", output)