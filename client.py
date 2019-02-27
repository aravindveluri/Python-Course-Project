import socket
import threading
import sys
import os
from colorama import Fore
from colorama import Style
from colorama import Back

#colorama module imported and installed from https://pypi.org/project/colorama/

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((str(sys.argv[1]), int(sys.argv[2])))

def sender_fn():
    while True:
        sent = raw_input()
        if sent:
            if (sent[:5] == 'send ' or  sent[:5] == 'Send ' or sent[:5] == 'SEND '):
                filename = sent[5:]
                if(os.path.isfile(filename)):
                    s.send("Receiving a file from the client "+ str(filename) +" of size " + str(os.path.getsize(filename))+"Bytes...")
                    f = open(filename, 'rb')
                    file_data = f.read(1024)
                    s.send(file_data)
                    while file_data!="":
                        file_data = f.read(1024)
                        s.send(file_data)
                    print Fore.CYAN + Style.BRIGHT + "File sent successfully!" + Style.RESET_ALL
                    f.close()
                else:
                    print Back.RED + "*** Oops! The entered filename doesn't correspond to any existing files! ***" + Style.RESET_ALL
            else:
                s.send(sent)
                if sent == "quit()":
                    s.close()
                    break
        else:
            print Back.RED + "***  Oops! Empty message cannot be sent! ***" + Style.RESET_ALL

def receiver_fn():
    while True:
        data = '' 
        try:
            data = s.recv(1024)
        except socket.error:
            pass
        if data: 
            if(data[:32] == "Receiving a file from the server"):
                print data
                comp_str = (str(data)[33:].split(' of size '))
                filename = comp_str[0]
                filesize = long((comp_str[1]).split('B')[0])
                fl = open('new_'+filename, 'wb')
                file_data = s.recv(1024)
                totaldata = len(file_data)
                fl.write(file_data)
                while totaldata < filesize:
                    file_data = s.recv(1024)
                    prev_percent_recvd = (100*(totaldata))/filesize
                    totaldata += len(file_data)
                    fl.write(file_data)
                    nxt_percent_recvd = (100*(totaldata))/filesize
                    if(prev_percent_recvd!=nxt_percent_recvd):
                        print "Receiving... " + Fore.CYAN + str(nxt_percent_recvd) + Style.RESET_ALL + "% Done"
                print Fore.CYAN + Style.BRIGHT + "File received successfully!" + Style.RESET_ALL
                fl.close()
            else:
                print Fore.CYAN + Style.BRIGHT + "Server: " + data + Style.RESET_ALL


print "Conversation with Server started"

send_thread = threading.Thread(target = sender_fn)
recv_thread = threading.Thread(target = receiver_fn)

recv_thread.daemon = True

send_thread.start()
recv_thread.start()
