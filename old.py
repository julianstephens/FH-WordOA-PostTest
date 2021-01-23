from psychopy import visual, core, data, gui, event
from psychopy.hardware import keyboard
import glob
import os
import random

class Experiment:
    def __init__(
        self, name, session_id, participant_id, num_trials, words_path, escape_key=None
    ):
        self.name = "PostTest - " + str(participant_id)
        self.session_id = session_id
        self.participant_id = participant_id
        self.num_trials = num_trials
        self.words_path = words_path
        self.clock = core.Clock()
        self.stimuli = []
        self.escape_key = escape_key

    def createWindow(self):
        """Creates the experiment window"""
        self.win = visual.Window(
            size=(1024, 768),
            fullscr=True,
            screen=0,
            winType="pyglet",
            allowGUI=False,
            allowStencil=False,
            monitor="testMonitor",
            color=[0, 0, 0],
            colorSpace="rgb",
            blendMode="avg",
        )

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

        text_stim = visual.TextStim(
            win=self.win,
            ori=0,
            name=self.name,
            text=self.text,
            font="Arial",
            pos=self.pos,
            height=self.height,
            color=self.color,
            colorSpace="rgb",
            wrapWidth=None,
            opacity=1,
            languageStyle="LTR",
            depth=0.0,
        )

        return text_stim

    def presentStimulus(self, stim, target):
        self.stimulus = stim
        self.target = target
        self.win.flip()

        if self.stimulus == "text":
            self.text_on_screen.setText(target)
            self.text_on_screen.draw()
        elif self.stimulus == "image":
            self.target.draw()

    def createKeyboard(self):
        kb = Keyboard()

        return kb

    def createTrials(self, num_words):
        """Creates list of trials to be conducted

        Args:
            num_words: Number of words participants are shown in a single trial

        """
        # randomly selects 40 lines from total length of provided sheet
        #  TODO: figure out if there's a space efficient way to calculate total rows in xlxs file
        select_rows = random.sample(range(121), num_words)

        return data.importConditions(self.words_path, selection=select_rows)

    def experimentTrials(self, trials, name, num_reps, expInfo):
        """

        Args:
            trials:
            name:
            num_reps:
            expInfo:

        """
        self.exp_info = expInfo

        #  sets up handler to randomize conditions
        self.trials = data.TrialHandler(
            nReps=num_reps,
            method="random",
            extraInfo=self.exp_info,
            originPath=-1,
            trialList=self.createTrials(40),
            seed=None,
            name=name,
        )

        #  TODO: look into best way to handle looping over trials and runs

    def experimentInfo(self):
        self.expName = "FH_WordOA_PostTest"
        self.expInfo = {"participant": "", "session": "001"}
        self.expInfo["date"] = date.getDataStr()
        self.info_dlg = gui.DlgFromDict(
            dictionary=self.expInfo, sortKeys=False, title=self.expName
        )

        _thisDir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(_thisDir)
        self.datafile = (
            _thisDir
            + os.sep
            + u"data/%s_%s_%s"
            % (self.expInfo["participant"], self.expName, self.expInfo["date"])
        )

        if self.info_dlg.OK:
            return self.expInfo
        else:
            return "Cancelled"