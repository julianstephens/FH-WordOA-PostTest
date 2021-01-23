from psychopy import visual, core, event
import ctypes


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
            self.addStimulus(stimulus)

    def playAll(self, verbose=False):
        """Plays all the stimuli in the sequence.

        Args:
            verbose: bool if show stimuli details

        """
        stim_index = 0

        while self.escape_key not in event.getKeys():
            stim_index += 1

            if verbose:
                "Playing stimulus {stim_index}".format(stim_index=stim_index)

            self.playNext()
        core.quit()
        print("Finished")

    def playNext(self, verbose=False):
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
            return stim.show()
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
        """Show the stimulus. Must be implemented by descendant classes"""
        raise NotImplementedError

    def close(self):
        """Close out."""
        core.quit()


class Text(Stimulus):
    def __init__(self, window, text, duration=2.0, keys=None):
        """Initializes a text stimulus

        Args:
            window: the window object
            text: text to display
            duration: the duration the text will appear
            keys: the list of keys to press to continue to the next stimulus (if None, will automatically go to next stimulus)
        """
        self.window = window
        self.text = visual.TextStim(self.window, text=text, units="norm")
        self.duration = duration
        self.keys = keys

    def show(self):
        self.text.draw()
        self.window.flip()
        core.wait(self.duration)

        if self.keys:
            wait_for_key(self.keys)
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

    """

    def __init__(self, window, keys, event="continue"):
        self.window = window
        self.keys = keys
        self.event = event

    def show(self):
        wait_for_key(self.keys)
        self.run_event()
        return self

    def run_event(self):
        if self.event == "exit":
            print("Exiting...")
            self.window.close()
            core.quit()
        if self.event in ["nothing", "continue"]:
            pass
        else:
            print("Warning: Event not recognized. Doing nothing.")


def wait_for_key(keys):
    """Wait for a key that is in a set of keys to be pressed before proceeding.

    Args:
        keys: a list or tuple of keys

    """
    event.clearEvents()
    event.waitKeys(keyList=keys)