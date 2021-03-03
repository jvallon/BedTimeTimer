from flask import Flask, render_template
from datetime import datetime, timedelta
from apa102_pi.driver import apa102
import time
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

stripLen = 9
strip = apa102.APA102(num_led=stripLen,order='rgb',global_brightness=5)

app = Flask(__name__)

def startup():
    strip.clear_strip()
    for x in range(0,stripLen):
        strip.set_pixel(x,255,0,0)
        strip.show()
        time.sleep(.2)
    strip.clear_strip()
    if(datetime.now().hour >= 20 or datetime.now().hour <= 5):
        redLight()

@scheduler.scheduled_job('cron', id='sleep_job', hour=20)
def redLight():
    print("red light")
    strip.clear_strip()
    for x in range(0,3):
        strip.set_pixel(x,255,0,0)
    strip.show()

def yellowLight():
    print("yellow light")
    strip.clear_strip()
    for x in range(3,6):
        strip.set_pixel(x,255,255,0)
    strip.show()

@scheduler.scheduled_job('cron', id='wake_job', hour=5)
def greenLight():
    print("green")
    strip.clear_strip()
    for x in range(6,9):
        strip.set_pixel(x,0,255,0)
    strip.show()

@scheduler.scheduled_job('cron', id='powersave', hour=7)
def clear():
    print("clear")
    strip.clear_strip()
    strip.show()

@app.route("/")
def home():
    now = datetime.now()
    timeStr = now.strftime('%Y-%m-%d %H:%M')
    templateData = {
        'title':'Hello there',
        'time':timeStr
    }
    return render_template('index.html',**templateData)

@app.route("/timeout")
def timeout():
    for x in scheduler.get_jobs():
        if('timeout' in x.id):
            x.remove()
    
    scheduler.add_job(redLight, id='timeout_red')
    scheduler.add_job(yellowLight,'date', id='timeout_yellow', run_date=datetime.now() + timedelta(minutes=1))
    scheduler.add_job(greenLight,'date', id='timeout_green', run_date=datetime.now() + timedelta(minutes=2))
    scheduler.add_job(clear,'date', id='timeout_finish', run_date=datetime.now() + timedelta(minutes=2,seconds=30))
    return render_template('index.html')

@app.route("/test")
def test():
    startup()

@app.route("/led/stoplight")
def ledTest():
    strip.clear_strip()
    strip.set_pixel(0,255,0,0)
    strip.set_pixel(1,255,0,0)
    strip.set_pixel(2,255,0,0)
    strip.set_pixel(3,255,200,0)
    strip.set_pixel(4,255,200,0)
    strip.set_pixel(5,255,200,0)
    strip.set_pixel(6,0,255,0)
    strip.set_pixel(7,0,255,0)
    strip.set_pixel(8,0,255,0)
    strip.show()
    templateData = {
        'title':'Hello there',
        'time':'LED changed'
    }
    return render_template('index.html',**templateData)

@app.route("/led/off")
def ledOff():
    clear()
    templateData = {
        'title':'LED OFF',
        'time':'LED changed'
    }
    return render_template('index.html',**templateData)

startup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
