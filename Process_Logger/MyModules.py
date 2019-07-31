
#modules
import psutil;
import sys;
import os;
import time;
import email, smtplib, ssl;
import smtplib;
import urllib.request;

#p
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#
curr_time = "";

################################################################################
def ProcessDisplay():
	
	listProc = [];
	
	for p in psutil.process_iter():
		
		try:
			
			pinfo = p.as_dict(attrs = ['name','pid','username']);
			listProc.append(pinfo);
			
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			
			pass;
		
	return listProc;
################################################################################


################################################################################
def ChkProcess(procname):
		
	for p in psutil.process_iter():
		
		try:
			
			if p.name() == procname:
				pinfo = p.as_dict(attrs = ['name','pid','username']);
				vms =p.memory_info().vms/(1024 * 1024);
				pinfo['vms'] = vms;
				print(pinfo);
				break;
			
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			
			pass;

################################################################################


################################################################################
def ProcLogger(_dir = "Logs"):
	
	listProc = ProcessDisplay();
	
	if not os.path.exists(_dir):
		try:
			os.mkdir(_dir);
		except:
			pass;
		
	sep = "*"*80;
	global curr_time; 
	curr_time = time.ctime();
	lpath = os.path.join(_dir, "Log "+curr_time+".log");
	with open(lpath, "w") as fd:
		fd.write(sep+"\n"+"Process Logger at: "+curr_time+"\n"+sep+"\n");
		fd.writelines(str(i)+"\n" for i in listProc);
	
	return lpath;
################################################################################

################################################################################
def MailSender(user, passwd, recp, filename):
	
	subject = "This mail contains Process log";
	sender_email = user;
	receiver_email = recp;
	password = passwd;
	body = """
	This is an auto-generated mail.
	Please find the attachment of process log created at: """ + curr_time + """
	"""
	
	message = MIMEMultipart();
	message["From"] = sender_email;
	message["To"] = receiver_email;
	message["Subject"] = subject;
	message["Bcc"] = receiver_email;
	
	message.attach(MIMEText(body, "plain"));
	
	with open(filename, "rb") as attachment:
		part = MIMEBase("application", "octet-stream");
		part.set_payload(attachment.read());
	
	encoders.encode_base64(part);
	part.add_header(
		"Content-Disposition",
		f"attachment; filename= {filename}",
	);
	
	message.attach(part);
	text = message.as_string();
	
	try:
		context = ssl.create_default_context();
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(sender_email, password);
			server.sendmail(sender_email, receiver_email, text);
		
		print("Mail sent successsfully");
		
	except Exception as e:
		
		print("Unable to send mail ", e);
	
################################################################################


################################################################################
def is_connected():
	
	try:
		urllib.request.urlopen("http://216.58.192.142",timeout=5);
		return True;
	except urllib.urlerror as err:
		return False;
################################################################################
