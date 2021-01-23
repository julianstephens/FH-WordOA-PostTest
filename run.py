from psychopy import core, gui, logging
from stimulus import Paradigm, Text

from settings import get_settings
import experiment as ex

settings = get_settings(env="dev", test=True)


def run_experiment():
    exp_info = {"participant": "", "session:": "001"}
    dlg = gui.DlgFromDict(exp_info, sortKeys=False, title=settings["exp_name"])

    if dlg.OK == False:
        core.quit()

    isOdd = True if int(exp_info["participant"]) % 2 != 0 else False

    par = constructPar()
    if par:
        par.playAll()


def constructPar():
    par = Paradigm(window_dimensions=settings["window_dimensions"], escape_key="escape")

    stimuli = [(Text, (ex.introduction01, ex.duration01, ex.keys01))]

    par.addStimuli(stimuli)

    return par


if __name__ == "__main__":
    logging.console.setLevel(settings["logging_level"])
    run_experiment()
