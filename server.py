import socket			 
import threading
import sys
import os
from colorama import Fore
from colorama import Back
from colorama import Style

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((str(sys.argv[1]),int(sys.argv[2])))		 
s.listen(5)

while True:
    print "Waiting for client..."
    
    c, addr = s.accept()

    print "Client Connected from" + Fore.YELLOW + " <" + str(addr) + ">" + Style.RESET_ALL

    def receiver_fn():
        while True:
            data = ''
            try:
                data = c.recv(1024)
                if data: 
                    if(data[:32] == "Receiving a file from the client"):
                        print data
                        comp_str = (str(data)[33:].split(' of size '))
                        filename = comp_str[0]
                        filesize = long((comp_str[1]).split('B')[0])
                        fl = open('new_'+filename, 'wb')
                        file_data = c.recv(1024)
                        totaldata = len(file_data)
                        fl.write(file_data)
                        while totaldata < filesize:
                            file_data = c.recv(1024)
                            prev_percent_recvd = (100*(totaldata))/filesize
                            totaldata += len(file_data)
                            fl.write(file_data)
                            nxt_percent_recvd = (100*(totaldata))/filesize
                            if(prev_percent_recvd!=nxt_percent_recvd):
                                print "Receiving... " + Fore.CYAN + str(nxt_percent_recvd) +Style.RESET_ALL + "% Done"
                        print Fore.CYAN + Style.BRIGHT + "File received successfully!" + Style.RESET_ALL
                        fl.close()
                    elif data!="quit()":
                        print Fore.MAGENTA + Style.BRIGHT + "Client: " + data + Style.RESET_ALL
                    else:
                        print Back.RED + "--- Client quit the chat ---" + Style.RESET_ALL + "\n"
                        c.close()
                        break
            except socket.error:
                c.close()
                break
    
    def sender_fn():
        while True:
            sent = raw_input()
            if sent:
                if (sent[:5] == 'send ' or  sent[:5] == 'Send ' or sent[:5] == 'SEND '):
                    filename = sent[5:]
                    if(os.path.isfile(filename)):
                        c.send("Receiving a file from the server "+ str(filename) +" of size " + str(os.path.getsize(filename))+"Bytes...")
                        f = open(filename, 'rb')
                        file_data = f.read(1024)
                        c.send(file_data)
                        while file_data!="":
                            file_data = f.read(1024)
                            c.send(file_data)
                        print Fore.CYAN + "File sent successfully!" + Style.RESET_ALL
                        f.close()
                    else:
                        print Back.RED + "*** Oops! The entered filename doesn't correspond to any existing files! ***" + Style.RESET_ALL
                else:
                    c.send(sent)
            else:
                print Back.RED + "*** Oops! Empty message cannot be sent! ***" + Style.RESET_ALL
    
    print "Conversation with Client started"
    
    sender_thread = threading.Thread(target = sender_fn)
    recv_thread = threading.Thread(target = receiver_fn)
    
    sender_thread.daemon = True
    recv_thread.daemon = True
    
    recv_thread.start()
    sender_thread.start()

    recv_thread.join()
