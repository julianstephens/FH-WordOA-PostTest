import ctypes
import random
import sys

from psychopy import core, event, visual

import experiment as ex
import run


class Paradigm:
    """Represents a study paradigm.

    Attributes:
        window
        _init_stimulus
        escape_key
        stimuli

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
            print("Added Stimulus")
            self.addStimulus(stimulus)

    def playAll(self, is_odd, verbose=False):
        """Plays all the stimuli in the sequence.

        Args:
            verbose: bool if show stimuli details

        """
        stim_index = 0

        while self.escape_key not in event.getKeys():
            stim_index += 1

            if verbose:
                "Playing stimulus {stim_index}".format(stim_index=stim_index)

            self.playNext(is_odd)
        core.quit()
        print("Finished")

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
    def __init__(self, window, text, height=0.1, duration=2.0, keys=None):
        """Initializes a text stimulus

        Args:
            window: the window object
            text: text to display
            duration: the duration the text will appear
            keys: the list of keys to press to continue to the next stimulus (if None, will automatically go to next stimulus)
        """
        self.window = window
        self.word_key = list(text.keys())[0]
        self.height = height
        self.text = visual.TextStim(
            self.window, text=text[self.word_key], height=self.height, units="norm")
        self.duration = duration
        self.keys = keys

    def show(self, is_odd):
        self.text.draw()
        self.window.flip()

        if self.duration:
            core.wait(self.duration)
        elif self.keys:
            print("waiting for key")
            wait = WaitForKey(self.window, self.keys, self.word_key)
            print("created wait")

            return wait.show(self, is_odd)

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

    def __init__(self, window, keys, word_key, event="continue"):
        self.window = window
        self.keys = keys
        self.event = event
        self.word_key = word_key

    def show(self, stimulus, is_odd):
        print("In wait show")

        #  Get participant answer
        key_pressed = wait_for_key(self.keys)

        #  Process answer
        self.run_event(stimulus, is_odd, key_pressed)

        return self

    def run_event(self, stimulus, is_odd, key_pressed):
        if self.event == "exit":
            print("Exiting...")
            self.window.close()
            core.quit()

        #  Create key for answer lookup
        answer_code = {}

        #  Set keys based on participant ID
        if is_odd:
            answer_code['d'] = 'f'
            answer_code['k'] = 'e'
        else:
            answer_code['d'] = 'e'
            answer_code['k'] = 'f'

        #  Get correct answer
        correct_answer = ex.excel_df[ex.excel_df.NOUN ==
                                     self.word_key].recallRespCorrect
        word_type = ex.excel_df.loc[ex.excel_df.Noun ==
                                    self.word_key].ASSOCIATE
        probe_type = "HOUSE"

        #  Update participant score if correct
        print("Par Answer: ", answer_code[key_pressed],
              "\nCorrect Answer: ", correct_answer)
        if correct_answer == answer_code[key_pressed]:
            curr_score = ex.log_df.at[0, 'Num_Correct_Nouns']

            if curr_score:
                new_score = int(curr_score) + 1
                ex.log_df.at[0, 'Num_Correct_Nouns'] = new_score
            else:
                ex.log_df.at[0, 'Num_Correct_Nouns'] = 1

            probe_type = word_type
        else:
            probes = ["HOUSE", "FACE"]
            probe_type = probes[random.randint(0, 1)]

        get_probe(probe_type, is_odd)

        stimulus.window.flip()
        return stimulus


def wait_for_key(keys):
    """Wait for a key that is in a set of keys to be pressed before proceeding.

    Args:
        keys: a list or tuple of keys
    """
    event.clearEvents()
    event.waitKeys(keyList=keys)

    return event.getKeys()


def get_probe(probe_type, is_odd):
    print("Creating probe")
    probe_tup = None

    #  Get probe
    if probe_type == 'HOUSE' and is_odd:
        probe_tup = random.choice(ex.house_list_odd)
    elif probe_type == 'HOUSE' and not is_odd:
        probe_tup = random.choice(ex.house_list_even)
    if probe_type == 'FACE' and is_odd:
        probe_tup = random.choice(ex.face_list_odd)
    elif probe_type == 'FACE' and not is_odd:
        probe_tup = random.choice(ex.face_list_even)

    #  If unable to get probe, exit
    if probe_tup:
        (probe, keys) = probe_tup
    else:
        print("Exiting...")
        core.quit()

    #  Construct stim and add to stimlist
    display_text = dict()
    display_text[probe] = probe + "\n" + keys
    stim = (Text, (display_text, 0.1, 0.0, ["d", "k"]))

    run.stimuli.insert(0, stim)
