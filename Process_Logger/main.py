"""
4. Design automation script which accept directory name and mail id from user and create log
file in that directory which contains information of running processes as its name, PID,
Username. After creating log file send that log file to the specified mail.
"""

import MyModules as mod;

def main():
	
	# args filter
	if (len(mod.sys.argv) < 2) or (len(mod.sys.argv) > 5):		
		print("invalid args");
		exit();
	
	if ((mod.sys.argv[1] == "-h") or (mod.sys.argv[1] == "-H")):
		print("Help: This script mails a log of running processes");
		exit();
		
	if ((mod.sys.argv[1] == "-u") or (mod.sys.argv[1] == "-U")):
		print("Usage: ScriptName DirName sender_mailid sender_password rec_mailid");
		exit();
		
	
	filepath = mod.ProcLogger(mod.sys.argv[1]);
	connected = mod.is_connected();
	if connected:
		mod.MailSender(mod.sys.argv[2], mod.sys.argv[3], mod.sys.argv[4], filepath);
	else:
		print("NO internet Connection");
		
		
if __name__ == "__main__":
	
	main();
		


