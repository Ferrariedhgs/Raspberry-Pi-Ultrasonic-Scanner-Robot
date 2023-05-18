from flask import Flask
from flask import render_template
import pigpio
import RPi.GPIO as rpi
import time
import numpy as np
import matplotlib.pyplot as plt
import os

app=Flask(__name__,template_folder='Templates')
IMG_FOLDER = os.path.join('static', 'IMG')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

ledpin=16
echo=33
trig=32
buzzer=18

in1=7
in2=11
in3=13
in4=15

motor1=29
motor2=31
motor3=35
motor4=37

rad = np.linspace(0,(2 * np.pi),256)

pi=pigpio.pi()
pi.set_mode(buzzer, pigpio.OUTPUT)

rpi.setwarnings(False)
rpi.setmode(rpi.BOARD)
rpi.setup(echo, rpi.OUT)
rpi.setup(trig, rpi.OUT)
rpi.output(trig, 0)
rpi.output(echo, 0)
rpi.setup(buzzer, rpi.OUT)
rpi.output(buzzer, 0)
rpi.setup(in1, rpi.OUT)
rpi.setup(in2, rpi.OUT)
rpi.setup(in3, rpi.OUT)
rpi.setup(in4, rpi.OUT)
rpi.output(in1, 0)
rpi.output(in2, 0)
rpi.output(in3, 0)
rpi.output(in4, 0)
rpi.setup(motor1, rpi.OUT)
rpi.setup(motor2, rpi.OUT)
rpi.setup(motor3, rpi.OUT)
rpi.setup(motor4, rpi.OUT)
rpi.output(motor1, 0)
rpi.output(motor2, 0)
rpi.output(motor3, 0)
rpi.output(motor4, 0)
rpi.setup(ledpin, rpi.OUT)
rpi.output(ledpin, 0)

step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
motor_pins = [in1,in2,in3,in4]

print("Initialized")
pi.hardware_PWM(buzzer, 500, 500000)
time.sleep(1)
pi.hardware_PWM(buzzer, 0, 0)
time.sleep(0.05)						#use the buzzer to announce that the program starts
rpi.output(ledpin, 1)
time.sleep(1)
rpi.output(ledpin, 0)

def cleanup():
    rpi.output( in1, rpi.LOW )
    rpi.output( in2, rpi.LOW )
    rpi.output( in3, rpi.LOW )			#turn off the stepper
    rpi.output( in4, rpi.LOW )
    
def move_stepper(unit):
    motor_step_counter=0
    if unit>0:
        direction=-1
    else:
       direction=1
    unit=abs(unit)
    i=0
    for i in range(unit*16):
        for pin in range(0, len(motor_pins)):
            rpi.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==1:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==-1:
            motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(0.002)
    cleanup()

def calculate_distance():
    rpi.output(trig, rpi.HIGH)
    time.sleep(0.00001)
    rpi.output(trig, rpi.LOW)
    start = time.time()
    stop = time.time()
    while rpi.input(echo) == 0:
        start = time.time()
    while  rpi.input(echo) == 1:
        stop = time.time()
    duration = stop - start
    distance = 34300/2 * duration
    if distance < 0.5 and distance > 400:
        return 0
    else:
        return distance

@app.route('/')
def index():
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)


@app.route('/back')
def back():
    rpi.output(motor1, 0)
    rpi.output(motor2, 0)
    rpi.output(motor3, 0)
    rpi.output(motor4, 0)
    
    rpi.output(motor1, 1)
    rpi.output(motor2, 0)
    
    rpi.output(motor3, 1)
    rpi.output(motor4, 0)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/left')
def left():
    rpi.output(motor1, 0)
    rpi.output(motor2, 0)
    rpi.output(motor3, 0)
    rpi.output(motor4, 0)
    
    rpi.output(motor1, 1)
    rpi.output(motor2, 0)
    
    rpi.output(motor3, 0)
    rpi.output(motor4, 1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/stop')
def stop():
    rpi.output(motor1, 0)
    rpi.output(motor2, 0)
    rpi.output(motor3, 0)
    rpi.output(motor4, 0)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/right')
def right():
    rpi.output(motor1, 0)
    rpi.output(motor2, 0)
    rpi.output(motor3, 0)
    rpi.output(motor4, 0)
    
    rpi.output(motor1, 0)
    rpi.output(motor2, 1)
    
    rpi.output(motor3, 1)
    rpi.output(motor4, 0)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/forward')
def forward():
    rpi.output(motor1, 0)
    rpi.output(motor2, 0)
    rpi.output(motor3, 0)
    rpi.output(motor4, 0)
    
    rpi.output(motor1, 0)
    rpi.output(motor2, 1)
    
    rpi.output(motor3, 0)
    rpi.output(motor4, 1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/led')
def led():
    led_state = rpi.input(ledpin)
    if led_state:
        rpi.output(ledpin, 0)
    else:
        rpi.output(ledpin, 1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/scan')
def scan():
    pi.hardware_PWM(buzzer, 500, 500000)
    time.sleep(1)
    pi.hardware_PWM(buzzer, 0, 0)
    time.sleep(0.5)
    pi.hardware_PWM(buzzer, 500, 500000)
    time.sleep(1)
    pi.hardware_PWM(buzzer, 0, 0)
    time.sleep(0.05)
    left=[]
    right=[]
    move_stepper(128)
    print("for")
    for j in range(255):
        move_stepper(-1)
        print("stepper")
        if j<128:
            print("if")
            a=calculate_distance()
            right.append(a)
            print(a)
        else:
            print("else")
            a=calculate_distance()
            left.append(a)
            print(a)
    move_stepper(128)
    new=left+right
    new.append(new[1])
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.set_theta_zero_location("N")

    ax.plot(rad,new)
    ax.set_title("Scanarea")
    plt.savefig('static/IMG/fig.png', bbox_inches='tight')
    pi.hardware_PWM(buzzer, 500, 500000)
    time.sleep(0.5)
    pi.hardware_PWM(buzzer, 0, 0)
    time.sleep(0.1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/cl')
def calibrateleft():
    move_stepper(-1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)

@app.route('/cr')
def calibrateright():
    move_stepper(1)
    picture = os.path.join(app.config['UPLOAD_FOLDER'], 'fig.png')
    return render_template("webpage.html", user_image=picture)


if __name__=="__main__":
    print("Start")
    app.run(debug=True, host='Replace with the IP of the Pi')
