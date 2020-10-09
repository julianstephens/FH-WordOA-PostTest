from psychopy import visual, core, data, gui, event
import glob
import os
from random import shuffle


class Experiment():
    def __init__(self, name, session_id, participant_id, num_trials):
        self.name = "PostTest" + participant_id
        self.session_id = session_id
        self.participant_id = participant_id
        self.num_trials = num_trials

    def createWindow(self):
        """
        Creates the experiment window    
        """
        self.win = visual.Window(size=(1024, 768), fullscr=True, screen=0, winType='pyglet', allowGUI=False,
                                 allowStencil=False, monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', blendMode='avg')
        return self.win
