#!/usr/bin/env python

from duckietown_msgs.msg import LanePose, FSMState
import rospy
import matplotlib.pyplot as plt
import numpy as np


class GraphNode():

    def __init__(self):

        self.active = False

        self.d_lst = []
        self.phi_lst = []


        self.subMode = rospy.Subscriber("/default/fsm_node/mode",FSMState, self.updateState)
        self.getError = rospy.Subscriber("/default/lane_filter_node/lane_pose", LanePose, self.updateErrorArray)



    def updateErrorArray(self,msg):
        if self.active:
            self.d_lst.append(msg.d)
            self.phi_lst.append(msg.phi)


    def updateState(self,msg):
        if msg.state == "EXITING_FROM_PARKING":
            self.active = True
        else:
            if self.active:
                self.printAndClose()


    def printAndClose(self):

        fileD = open('d_exit.txt','a')

        for element in self.d_lst:
            fileD.write(str(element))
            fileD.write('\t')
        fileD.write('\n')
        fileD.close()

        filePhi = open('angolo_exit.txt','a')

        for element in self.phi_lst:
            filePhi.write(str(element))
            filePhi.write('\t')
        filePhi.write('\n')
        filePhi.close()

        t = np.arange(0, len(self.d_lst), 1)  # see also linspace
        #nc = len(t)

        #self.e = np.zeros(nc)

        rospy.loginfo("DONEEEEE")
        fig_1 = plt.figure(1)
        plt.plot(t, self.d_lst, label='Errore')
        plt.title('Errore', fontsize=12)
        plt.xlabel('t')
        plt.ylabel('e')
        plt.grid(True)
        plt.legend()
        # plt.show()
        plt.savefig('errore.png')
        self.active = False
        #self.lst.clear(self)
        del self.d_lst[:]
        del self.phi_lst[:]


    def onShutdown(self):
        rospy.loginfo("[GraphNode] Shutdown.")

    def loginfo(self, s):
        rospy.loginfo('[%s] %s' % (self.node_name, s))


if __name__ == '__main__':
    rospy.init_node('graph_node', anonymous=False)
    graph_node_class = GraphNode()
    rospy.on_shutdown(graph_node_class.onShutdown)
    rospy.spin()

