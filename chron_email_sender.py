import multiprocessing
from databaseWrapper import DatabaseWrapper
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import xlwt
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from datetime import datetime, tzinfo
from pytz import timezone





class RunEmail(multiprocessing.Process, DatabaseWrapper):

    def __init__(self, database):
        multiprocessing.Process.__init__(self)
        DatabaseWrapper.__init__(self, database)
        self.database = database
        self.you_list = ['psheldon@randolphcollege.edu',
                         'apphysics@verizon.net',
                         'bbzylstra@randolphcollege.edu']

        #jobstores = {
        #    'default': SQLAlchemyJobStore(url='mysql://brad:moxie100@localhost/jobstore')
        #}

        executors = {
            'default': ThreadPoolExecutor(20),
        }

        self.scheduler = BlockingScheduler(executors    = executors)

    def dump_database(self):

        if not self.fetch_from_database(database_name   = 'ap_app',
                                        table_name      = 'AP_Physics',
                                        to_fetch        = '*'):
            return []
        else:
            metric_data = self.fetchall()

        if len(metric_data) == 0:
            return []
        else:
            return zip(*list(zip(*metric_data)))

    def write_spreadsheet(self, data):

        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        sheet1.write(0, 0, "Time")
        sheet1.write(0, 1, "Test-id")
        sheet1.write(0, 2, "Number")
        sheet1.write(0, 3, "Initials")
        sheet1.write(0, 4, "Date")
        for row_index, row in enumerate(data):
            for col_index, column in enumerate(row):
                sheet1.write(row_index +1, col_index, column)
        book.save("ap_physics_stats.xls")

    def email_spreadsheet(self, you):

        eastern = timezone('US/Eastern')
        current_est_time = datetime.now(tz=eastern)
        fmt = '%Y-%m-%d %H:%M:%S'
        current_est_time = current_est_time.strftime(fmt)

        me = 'ap_app_automatic@mail.com'
        SUBJECT = "AP Physics Stats: " + current_est_time

        msg = MIMEMultipart()
        msg['Subject'] = SUBJECT
        msg['From'] = me
        msg['To'] = you

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("ap_physics_stats.xls", "rb").read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="ap_physics_stats.xls"')

        msg.attach(part)
        s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
        s.starttls()
        s.ehlo()
        s.login(user='AKIAIT6YYNXSVVVTGTLQ',password='AmpnuPQdUECljleQ3oM/9wV6pmOXLLGVm47SsTI3Y2Fn')
        s.sendmail(me, [you], msg.as_string())
        s.quit()

    def run(self):
        data = self.dump_database()
        self.write_spreadsheet(data)

        for name in self.you_list:
            self.email_spreadsheet(name)
        return True


class RunEmailCron(RunEmail):

    def job(self):
        data = self.dump_database()
        self.write_spreadsheet(data)
        for name in self.you_list:
            self.email_spreadsheet(name)

    def run(self):
        job = self.scheduler.add_job(func=self.job,
                                     trigger = 'cron',
                                     hour    = '20,22',
                                     minute  = 15)

        job = self.scheduler.add_job(func=self.job,
                                     trigger = 'cron',
                                     hour    = 15,
                                     minute  = 30)

        job = self.scheduler.add_job(func=self.job,
                                     trigger = 'cron',
                                     hour    = 17,
                                     minute  = 45)
        self.scheduler.start()

        return True


