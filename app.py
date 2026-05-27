import RPi.GPIO as GPIO
from flask import Flask, render_template
 
app = Flask(__name__)
 
GPIO.setmode(GPIO.BCM)
 
# 핀 번호, 이름, 상태를 담을 dictionary
pins = {
    23: {'name': 'GPIO 23', 'state': GPIO.LOW},
    24: {'name': 'GPIO 24', 'state': GPIO.LOW}
}
 
# 모든 핀을 출력으로 설정하고 LOW로 초기화
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
 
 
@app.route("/")
def main():
    # 각 핀의 현재 상태를 읽어와 dictionary에 저장
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {'pins': pins}
    return render_template('main.html', **templateData)
 
 
@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
 
    if action == "on":
        GPIO.output(changePin, GPIO.HIGH)
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
 
    # 상태 갱신
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
 
    templateData = {'pins': pins}
    return render_template('main.html', **templateData)
 
 
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=False)
    finally:
        GPIO.cleanup()
