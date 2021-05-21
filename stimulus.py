from collections import OrderedDict
import ctypes
import os
import random
import re
import sys

import pandas as pd
from psychopy import core, event, visual

import experiment as ex
from settings import get_settings

settings = get_settings(env="production", test=False)
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
            par.log_data["exp_runtime"] = ["Total Experiment Runtime",
                                           "", "", "", "", "", "", "", "", "", "", "", "", "", elapsed]

            #  Get participant ID and format
            uid = settings["participant"]
            if int(uid) < 10:
                uid = "0" + str(uid)

            #  Create logs directory if doesn't exist
            if not os.path.exists(ex.log_dir):
                os.makedirs(ex.log_dir)

            #  Dump log info to csv
            log_path = str(ex.log_dir) + "/" + str(uid) + "_posttest_log.csv"
            log_df = pd.DataFrame.from_dict(
                par.log_data, orient='index', columns=['NOUN', 'ASSOCIATE', 'MF_RC', 'YO_OM', 'WN_LD', 'RESP_KEY', 'RESP_CODED',
                                                       'RESP_CORRECT', 'KEY_RT', 'PROBE_TYPE', 'PROBE', 'PROBE_KEY', 'PROBE_CODED', 'PROBE_CORRECT', 'PROBE_RT'])
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
    def __init__(self, window, text, height, duration, keys, stim_type, probe_details=None):
        """Initializes a text stimulus

        Args:
            window: the window object
            text: text to display
            duration: the duration the text will appear
            keys: the list of keys to press to continue to the next stimulus (if None, will automatically go to next stimulus)
            stim_type: float 0 if probe, 1 if intro, -1 otherwise
            probe_details: dict probe question and answer key 

        """
        self.window = window
        self.word_key = list(text.keys())[0]
        self.height = height
        self.text = visual.TextStim(
            self.window, text=text[self.word_key], height=self.height, units="norm")
        self.duration = duration
        self.keys = keys
        self.stim_type = stim_type
        self.probe_details = probe_details

    def show(self, is_odd):
        self.text.draw()
        self.window.flip()

        #  Create timer for individual stimulus
        stim_timer = core.MonotonicClock()

        if self.duration:
            core.wait(self.duration)
        elif self.keys:
            wait = WaitForKey(self.window, self.keys,
                              self.word_key, self.stim_type, self.probe_details)

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
        stim_type

    """

    def __init__(self, window, keys, word_key, stim_type, probe_details, event="continue"):
        self.window = window
        self.keys = keys
        self.event = event
        self.word_key = word_key
        self.stim_type = stim_type
        self.probe_details = probe_details

    def show(self, stimulus, is_odd, stim_timer):
        #  Get participant answer
        key_pressed = wait_for_key(self.keys)
        key_rt = stim_timer.getTime()

        #  Process answer
        self.run_event(stimulus, is_odd, self.stim_type,
                       self.probe_details, key_pressed, key_rt)

        return self

    def run_event(self, stimulus, is_odd, stim_type, probe_details, key_pressed, key_rt):
        global par

        if self.event == "exit":
            print("Exiting...")
            self.window.close()
            core.quit()

        if stim_type == 0:
            #  Get noun that came before probe
            last_noun = next(reversed(par.log_data.keys()))

            #  Get potential probe answers
            mf_rc = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    last_noun, 'MF_RC'].values[0]
            yo_om = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    last_noun, 'YO_OM'].values[0]
            wn_ld = ex.excel_df.loc[ex.excel_df.NOUN ==
                                    last_noun, 'WN_LD'].values[0]
            last_noun_attributes = [
                mf_rc.upper(), yo_om.upper(), wn_ld.upper()]

            #  Process user response
            probe_question = probe_details['q']
            probe_answer = probe_details[key_pressed].upper()

            correct_flag = 1 if probe_answer in last_noun_attributes else 0

            #  Update log with probe info
            log = par.log_data[last_noun]
            log.extend([probe_question, key_pressed,
                        probe_answer, correct_flag, key_rt])
            par.log_data[last_noun] = log
        elif stim_type < 0:
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

            #  Get misc info related to word from master list
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
        probe_type: str Face or House probe
        is_odd: bool participant ID is odd

    """
    probe_tup = None

    #  Get probe based on type (house or face) and is_odd
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

        #  Extract answer key for check later
        split = keys[0].split(",")
        d_key = split[0]
        k_key = split[1]

        d_answer = d_key[d_key.index('='):][2:]
        k_answer = k_key[k_key.index('='):][2:]
        probe_details = {
            'q': probe,
            'd': d_answer,
            'k': k_answer
        }

        #  Construct stim and add to stimlist
        display_text = dict()
        display_text[probe] = probe + "\n" + keys[0]
        stim = (Text, (display_text, ex.default_text_height,
                       ex.default_duration, ex.default_keys, 0, probe_details))
        insert(stim)

    else:
        #  If unable to get probe, exit
        print("Exiting...")
        core.quit()


def construct_par(is_odd):
    """ Initializes experiment paradigm

    Args:
        is_odd: bool if participant ID is odd

    """
    global par
    par = Paradigm(
        window_dimensions=settings["window_dimensions"], escape_key="escape")

    #  Get list of 40 random nouns
    face_words = ex.face_rows.NOUN.tolist()
    house_words = ex.house_rows.NOUN.tolist()
    random_words = face_words + house_words
    random.shuffle(random_words)

    #  Create intro stimulus
    intro_text = dict()
    intro_text['intro'] = ex.intro

    #  To use separate defaults for intro change below to ex.intro_duration and ex.intro_keys
    stimuli = [(Text, (intro_text, ex.intro_text_height,
                       ex.default_duration, ex.default_keys, 1))]

    #  Create word stimuli
    for word in random_words:
        key_text = ex.noun_odd_key if is_odd else ex.noun_even_key
        display_text = dict()
        display_text[word] = word + "\n" + key_text
        stim = (Text, (display_text, ex.default_text_height,
                       ex.default_duration, ex.default_keys, -1))
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
