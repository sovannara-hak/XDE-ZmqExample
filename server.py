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

class ZmqServer(xdefw.rtt.Task) :
    def __init__(self, name, time_step, ip, port):
        super(ZmqServer, self).__init__(rtt_interface.PyTaskFactory.CreateTask(name))
        self.s.setPeriod(time_step)

        self.i = 0.0

        self.newMsg = True

        # Initialization of the socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind("tcp://"+ip+":"+str(port))

    def startHook(self):
        pass

    def stopHook(self):
        pass

    def updateHook(self):
        if self.newMsg:
            self.i += 0.1

        data = [ self.i, self.i+2, self.i+4 ]
        msg = ""
        for v in data:
            msg += str(v)+" "

        try:
            self.socket.send(msg, zmq.NOBLOCK)
            self.newMsg = True
        except:
            print "Fail to push data"
            self.newMsg = False

TIME_STEP = .01

wm = xwm.WorldManager()

wm.createAllAgents(TIME_STEP)

wm.startAgents()

server = ZmqServer("server", TIME_STEP, "127.0.0.1", 5555)
server.s.start()


