from psychopy import visual, core, data, gui, event
import glob
import os
from random import shuffle


class Experiment():
    def __init__(self, name, session_id, participant_id, num_trials, words_path):
        self.name = "PostTest" + str(participant_id)
        self.session_id = session_id
        self.participant_id = participant_id
        self.num_trials = num_trials
        self.words_path = words_path

    def createWindow(self):
        """Creates the experiment window    
        """
        self.win = visual.Window(size=(1024, 768), fullscr=True, screen=0, winType='pyglet', allowGUI=False,
                                 allowStencil=False, monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', blendMode='avg')
        return self.win

    def createTextStimulus(self, win, text, pos, name, height, color):
        """Creates text stimulus

        Args:
            win: window to display on
            text: text to be displayed
            pos: location of text on window
            name: name of text stimulus object
            height: height of object
            color: text color

        Returns:
            text_stim TextStim 
        """
        self.text = text
        self.pos = pos
        self.name = name
        self.height = height
        self.color = color

        text_stim = visual.TextStim(win=self.win, ori=0, name=self.name, text=self.text,
                                    font='Arial', pos=self.pos, height=self.height, color=self.color, colorSpace='rgb')

        return text_stim

    def createTrials(self, num_words):
        """Creates list of trials to be conducted

        Args:
            num_words: Number of words participants are shown in a single trial

        """
        # randomly selects 40 lines from total length of provided sheet
        #  TODO: figure out if there's a space efficient way to calculate total rows in xlxs file
        select_rows = random.sample(range(121), num_words)

        return data.importConditions(self.words_path, selection=select_rows)

    def experimentTrials(self, trials, expInfo):
        self.exp_info = expInfo

        #  sets up handler to randomize conditions
        self.trials = data.TrialHandler(nReps=1, method='random', extraInfo=self.exp_info,
                                        originPath=-1, trialList=createTrials(40), seed=None, name='trials')

        #  TODO: look into best way to handle looping over trials and runs
