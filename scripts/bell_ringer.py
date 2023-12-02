import time
from time import sleep
from gpiozero import Servo
import board
from imapclient import IMAPClient
from digitalio import DigitalInOut, Direction
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = Servo(14, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ = 0.25

USERNAME = 'jasoncastillanestsp@gmail.com'
PASSWORD = 'sys8Iaq!@697'
NEWMAIL_OFFSET = 0

green_led = DigitalInOut(board.D18)
red_led = DigitalInOut(board.D23)
green_led.direction = Direction.OUTPUT
red_led.direction = Direction.OUTPUT
counter = 0

def mail_check(counter):
    server = IMAPClient(HOSTNAME, use_uid = True, ssl = True)
    server.login(USERNAME,PASSWORD)

    unseen = server.folder_status(MAILBOX, ['UNSEEN'])

    newmail_count = (unseen[b'UNSEEN'])
    print('%d unseen messages' % newmail_count)

    if newmail_count > (NEWMAIL_OFFSET + counter):
        servo.max()
        sleep(0.25)
        servo.min()
        sleep(0.25)
    else:
        servo.min()
    time.sleep(MAIL_CHECK_FREQ)
    return newmail_count

while True:
    counter = mail_check(counter)
