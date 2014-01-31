#!/usr/bin/env python

####################################
#                                  #
# Import all modules: configure... #
#                                  #
####################################
import xde_world_manager as xwm

import rtt_interface
import xdefw.rtt
import zmq

class ZmqClient(xdefw.rtt.Task) : 
    def __init__(self, name, time_step, ip, port):
        super(ZmqClient, self).__init__(rtt_interface.PyTaskFactory.CreateTask(name))

        self.s.setPeriod(time_step)

        self.address = "tcp://"+ip+":"+str(port)

        # Initialization of the socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect(self.address)

    def stopHook(self):
        pass

    def startHook(self):
        pass

    def updateHook(self):
        try:
            #Receive and parse and do not block if no data available
            msg = self.socket.recv(zmq.NOBLOCK)
            result = [float(v) for v in msg.split()]

            print result
        except:
            print "Can't pull data"


TIME_STEP = .01

wm = xwm.WorldManager()

wm.createAllAgents(TIME_STEP)

wm.startAgents()

client = ZmqClient("client", TIME_STEP, "127.0.0.1", 5555)
client.s.start()


