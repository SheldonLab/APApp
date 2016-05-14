import socket
from httpServer import httpServer
import multiprocessing
from chron_email_sender import RunEmailCron

host = "localhost"
user = "root"
password = "moxie100"
database = (host, user, password)

ip = socket.gethostbyname(socket.getfqdn())
thr = multiprocessing.Process(target=httpServer, args=(ip, 8000))
thr.start()

#email = RunEmailCron(database)
#email.start()
