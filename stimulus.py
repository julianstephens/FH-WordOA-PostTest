from collections import OrderedDict
import ctypes
import random
import sys
import os

import pandas as pd
from psychopy import core, event, logging, visual

import experiment as ex
from settings import get_settings

settings = get_settings(env="dev", test=True)
logging.console.setLevel(logging.WARNING)
par = None
experiment_timer = None

class Paradigm:
    """Represents a study paradigm.

    Attributes:
        window
        _init_stimulus
        escape_key
        stimuli
        log_data

    """

    def __init__(
        self,
        window_dimensions=(800, 600),
        color="Black",
        escape_key=None,
        *args,
        **kwargs
    ):
        """Initialize a paradigm

        Args:
            window_dimensions: the dimension of the Psychopy window object
            color: the color of the window object
            escape_key: the keyboard button that exits the paradigm

        """
        if window_dimensions == "full_screen":
            self.window = visual.Window(
                fullscr=True, color=color, units="norm", *args, **kwargs
            )
        else:
            self.window = visual.Window(
                window_dimensions, color=color, units="norm", *args, **kwargs
            )

        self.stimuli = []
        self.escape_key = escape_key
        self.log_data = OrderedDict()

    def addStimulus(self, stimulus):
        """Adds a stimulus.

        A stimulus should be a tuple of the form:
            (StimulusType, (arguments))

        Ex: (Text, ('Hello World!', 3.0))

        Args:
            stimulus: the stimulus to be added

        """
        assert type(stimulus) in (
            tuple,
            list,
        ), "Stimulus should be in form (StimulusType, (arguments))"
        self.stimuli.append(stimulus)

    def addStimuli(self, stimuli):
        """Adds multiple stimuli.

        Args:
            stimuli: a list of stimuli

        """
        for stimulus in stimuli:
            self.addStimulus(stimulus)

    def insertStimulus(self, stimulus):
        """Inserts a stimulus to the beginning of the stim list.

        A stimulus should be a tuple of the form:
            (StimulusType, (arguments))

        Ex: (Text, ('Hello World!', 3.0))

        Args:
            stimulus: the stimulus to be added

        """
        assert type(stimulus) in (
            tuple,
            list,
        ), "Stimulus should be in form (StimulusType, (arguments))"
        self.stimuli.insert(0, stimulus)

    def playAll(self, is_odd, verbose=False):
        """Plays all the stimuli in the sequence.

        Args:
            verbose: bool if show stimuli details

        """
        stim_index = 0

        #  Initialize clock for total experiment runtime
        global experiment_timer
        experiment_timer = core.MonotonicClock()
        while self.escape_key not in event.getKeys():
            stim_index += 1

            if verbose:
                "Playing stimulus {stim_index}".format(stim_index=stim_index)

            self.playNext(is_odd)

        core.quit()

    def playNext(self, is_odd, verbose=False):
        """Plays the next stimulus in the sequence

        Args:
            verbose: bool if show stimulus details

        Returns:
            Stimulus to be shown

        """
        if len(self.stimuli) > 0:
            stim_data = self.stimuli.pop(0)
            stim = self._init_stimulus(stim_data)

            if verbose:
                print(stim)

            return stim.show(is_odd)
        else:
            elapsed = experiment_timer.getTime()
            par.log_data["exp_runtime"] = ["Total Experiment Runtime", "", "", "", "", "", "", "", "", elapsed] 

            #  Get participant ID and format
            uid = settings["participant"]
            if int(uid) < 10: 
                uid = "0" + str(uid) 

            #  Create logs directory if doesn't exist
            if not os.path.exists('logs'):
                os.makedirs('logs')

            #  Dump log info to csv
            log_path = "logs/" + str(uid) + "_posttest_log.csv"
            log_df = pd.DataFrame.from_dict(
                par.log_data, orient='index', columns=['NOUN', 'ASSOCIATE', 'MF_RC', 'YO_OM', 'WN_LD', 'RESP_KEY', 'RESP_CODED',
                                                          'RESP_CORRECT', 'KEY_RT', 'PROBE_TYPE'])
            log_df.to_csv(log_path, index=False)

            core.quit()

    def _init_stimulus(self, stim_data):
        """Initialize a stimulus object from a tuple of the form
            (StimulusType, (arguments))

        Args:
            stim_data: the stimulus and its arguments as a tuple

        Returns:
            stim_class with new stimulus object

        """
        stim_class = stim_data[0]
        stim_args = stim_data[1] if type(stim_data[1]) == tuple else tuple()

        try:
            stim_kwargs = stim_data[2] if stim_args else stim_data[1]
        except IndexError:
            stim_kwargs = {}

        return stim_class(self.window, *stim_args, **stim_kwargs)


class Stimulus(object):
    """An abstract stimulus class. All stimulus types will inherit from this class"""

    def show(self):
        #  Show the stimulus. Must be implemented by descendant classes
        raise NotImplementedError

    def close(self):
        #  Close out.
        core.quit()


class Text(Stimulus):
    def __init__(self, window, text, height=0.1, duration=2.0, keys=None, is_probe=False):
        """Initializes a text stimulus

        Args:
            window: the window object
            text: text to display
            duration: the duration the text will appear
            keys: the list of keys to press to continue to the next stimulus (if None, will automatically go to next stimulus)
            is_probe: T/F if stimulus is a word or probe
        """
        self.window = window
        self.word_key = list(text.keys())[0]
        self.height = height
        self.text = visual.TextStim(
            self.window, text=text[self.word_key], height=self.height, units="norm")
        self.duration = duration
        self.keys = keys
        self.is_probe = is_probe

    def show(self, is_odd):
        self.text.draw()
        self.window.flip()
        #  TODO: Create clock
        stim_timer = core.MonotonicClock()

        if self.duration:
            core.wait(self.duration)
        elif self.keys:
            wait = WaitForKey(self.window, self.keys,
                              self.word_key, self.is_probe)

            return wait.show(self, is_odd, stim_timer)

        self.window.flip()
        return self


class Pause(Stimulus):
    """A simple pause

    Attributes:
        duration
        window
    """

    def __init__(self, window, duration):
        self.window = window
        self.duration = float(duration)

    def show(self):
        core.wait(self.duration)
        return self


class WaitForKey(Stimulus):
    """Wait for a key press

    Attributes:
        event
        window
        keys
        word_key

    """

    def __init__(self, window, keys, word_key, is_probe, event="continue"):
        self.window = window
        self.keys = keys
        self.event = event
        self.word_key = word_key
        self.is_probe = is_probe

    def show(self, stimulus, is_odd, stim_timer):
        #  Get participant answer
        key_pressed = wait_for_key(self.keys)
        key_rt = stim_timer.getTime() 

        #  Process answer
        self.run_event(stimulus, is_odd, self.is_probe, key_pressed, key_rt)

        return self

    def run_event(self, stimulus, is_odd, is_probe, key_pressed, key_rt):
        global par

        if self.event == "exit":
            print("Exiting...")
            self.window.close()
            core.quit()

        #  TODO: Add probe data to log
        #  if is_probe:
        #      last = next(reversed(par.log_data.keys()))
        #      log = par.log_data[last]
        #      #  log.append([key_pressed, ])
        if not is_probe:
            #  Create key for answer lookup
            answer_code = dict()

            #  Set keys based on participant ID
            if is_odd:
                answer_code['d'] = 'f'
                answer_code['k'] = 'e'
            else:
                answer_code['d'] = 'e'
                answer_code['k'] = 'f'

            #  Get correct answer
            correct_answer = ex.excel_df.loc[ex.excel_df.NOUN ==
                                             self.word_key, 'recallRespCorrect'].values[0]
            word_type = ex.excel_df.loc[ex.excel_df.NOUN ==
                                        self.word_key].ASSOCIATE.values[0]
            probe_type = word_type.upper()

            mf_rc = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    self.word_key, 'MF_RC'].values[0]
            yo_om = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    self.word_key, 'YO_OM'].values[0]
            wn_ld = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    self.word_key, 'WN_LD'].values[0]
            correct_flag = 1 if correct_answer == answer_code[key_pressed] else 0

            #  Determine probe type
            if not correct_flag:
                probes = ["HOUSE", "FACE"]
                probe_type = probes[random.randint(0, 1)]

            #  Update log
            par.log_data[self.word_key] = [
                self.word_key, word_type.upper(), mf_rc, yo_om, wn_ld, key_pressed, answer_code[key_pressed], correct_flag, key_rt, probe_type]

            get_probe(probe_type, is_odd)

        stimulus.window.flip()
        return stimulus


def wait_for_key(keys):
    """Wait for a key that is in a set of keys to be pressed before proceeding.

    Args:
        keys: a list or tuple of keys
    """
    event.clearEvents()

    return event.waitKeys(keyList=keys)[0]


def get_probe(probe_type, is_odd):
    """Insert probe at beginning of master stim list 

    Args:
        probe_type: Face or House probe
        is_odd: T/F participant ID is odd

    """
    probe_tup = None

    #  Get probe
    if probe_type == 'HOUSE' and is_odd:
        probe_tup = random.choice(ex.house_list_odd)
    elif probe_type == 'HOUSE' and not is_odd:
        probe_tup = random.choice(ex.house_list_even)
    elif probe_type == 'FACE' and is_odd:
        probe_tup = random.choice(ex.face_list_odd)
    elif probe_type == 'FACE' and not is_odd:
        probe_tup = random.choice(ex.face_list_even)

    if probe_tup:
        (probe, keys) = probe_tup

        #  Construct stim and add to stimlist
        display_text = dict()
        display_text[probe] = probe + "\n" + keys[0]
        stim = (Text, (display_text, 0.1, 0.0, ["d", "k"], True))
        insert(stim)

    else:
        #  If unable to get probe, exit
        print("Exiting...")
        core.quit()


def constructPar(is_odd):
    """ Initializes experiment paradigm

    Args:
        is_odd: T/F participant ID is odd

    """
    global par
    par = Paradigm(
        window_dimensions=settings["window_dimensions"], escape_key="escape")
    default_duration = 2.0
    default_keys = ["d", "k"]

    #  Get list of 40 random words
    face_words = ex.face_rows.NOUN.tolist()
    house_words = ex.house_rows.NOUN.tolist()
    random_words = face_words + house_words
    random.shuffle(random_words)

    #  Create intro routine
    intro_text = dict()
    intro_text['intro'] = ex.intro
    stimuli = [(Text, (intro_text, 0.05, ex.intro_duration, ex.intro_key))]

    #  Create word stimuli
    for word in random_words:
        key_text = ex.rand_odd_key if is_odd else ex.rand_even_key
        display_text = dict()
        display_text[word] = word + "\n" + key_text
        stim = (Text, (display_text, 0.1, 0.0, default_keys))
        stimuli.append(stim)

    #  Add stimuli to paradigm
    par.addStimuli(stimuli)


def insert(stimulus):
    """ Inserts stimulus at beginning of master stim list

    Args:
        stimulus: Stimulus to be inserted

    """
    global par
    par.insertStimulus(stimulus)
