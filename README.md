# tcp-python-chat: A Chatroom Terminal Application based on TCP-IP built in python

This is a python network TCP chat that contains both the server and client.
The server will be hosted on the current network on a certain port while the client can be ran from any device, any network, any port.

NOTE: The output may look weird or buggy depending on your terminal. For best results, please use terminals that popular linux machines use like the Gnome Terminal.

---

## Running the Chat Server

```
python3 chatserver.py -p PORT -l LOGFILE
```

  PORT can be a random port like 40015 and LOGFILE can just be "log".

---

## Running the Chat Client:

```
python3 chatclient.py -a ADDRESS -p PORT
```

  PORT should be the port you used for the server, ADDRESS should be the IP of the network the server is running on.

---

## While in the Chat as a User:
type a name. if the name is taken, it will assign a unique number to it.

type "chat()" and press enter to see how to operate the chat.

---

## Future Work
* Private Messaging
* UDP for fast transmit of packets
* Refactor and Reorganize code
