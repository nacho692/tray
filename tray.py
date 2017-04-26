import os, sys, json
from subprocess import *
import atexit
import threading
import paramiko

def open_tunnel(nodehost,tunnelport):
    serverhost = 'milagro.dc.uba.ar'
    nodeport = 22

    tunnelcmd = "ssh -S /tmp/ssh_tunnel" + str(tunnelport) +  ".sock -o ExitOnForwardFailure=yes -f -M -N -L " \
    + str(tunnelport) + ":" + nodehost + ":" + str(nodeport) + " " + serverhost
    print(tunnelcmd)
    call(tunnelcmd.split())

def close_tunnel(tunnelport):
    closetunnel = "ssh -q -S /tmp/ssh_tunnel" + str(tunnelport) +  ".sock -O exit serverhost"
    call(closetunnel.split())


def quit(portb):
	for (i,client) in sshC:
		try:
			print("Closing client {}".format(i))
			client.close()
		except:
			pass

	print("Closing tunnels")
	for i in pcs:
		close_tunnel(portb + i)

def sshConnection(i):
	try:
		open_tunnel("ws{}.labo{}.lab.dc.uba.ar".format(i,labo),portb+i)
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect("localhost",portb + i, timeout=5)
		print("{} conectado".format(i))
		sshC.append((i,client))
	except:
		print("{} no conectado".format(i))
		pass


#PARAMETROS
threads = []
sshC = []
portb = 50000
atexit.register(quit,portb)
labo = 4
pcs = range(1,21)

for i in pcs:
	thr = threading.Thread(target=sshConnection, args=(i,))
	threads.append(thr)
	thr.start()

for thr in threads:
	thr.join()

print("Threads terminados")

#eject -T
#eject -t
cmd = ''
while cmd != 'gg':
	cmd = input()
	for (i,client) in sshC:
		client.exec_command(cmd)



