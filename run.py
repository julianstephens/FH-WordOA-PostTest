from psychopy import logging
import random
import sys

import pandas as pd
from psychopy import core, gui, logging
import xlsxwriter

import experiment as ex
import stimulus as st
from settings import get_settings

settings = get_settings(env="dev", test=True)
logging.console.setLevel(logging.WARNING)

stimuli = []

def run_experiment():
    exp_info = {"participant": "", "session:": "001"}
    dlg = gui.DlgFromDict(exp_info, sortKeys=False, title=settings["exp_name"])

    if dlg.OK == False:
        core.quit()

    #  Check if participant ID is odd
    is_odd = True if int(exp_info["participant"]) % 2 != 0 else False

    #  Initialize experiment paradigm
    par = constructPar(is_odd)
    if par:
        #  Start clock for total experiment runtime
        experiment_timer = core.MonotonicClock()
        par.playAll(is_odd)
        sys.stdout.flush()

        #  Write total runtime to log
        exp_runtime = experiment_timer.getTime()
        ex.log_df.at[0, 'Experiment_Runtime'] = exp_runtime

        #  Dump logs to xlsx
        log_path = settings["log_file"]
        writer = pd.ExcelWriter(log_path, engine='xlsxwriter')
        ex.log_df.to_excel(writer, 'Experiment Info')
        ex.key_log_df.to_excel(writer, 'Key Responses')
        writer.close()


def constructPar(is_odd):
    par = st.Paradigm(
        window_dimensions=settings["window_dimensions"], escape_key="escape")

    default_duration = 2.0
    default_keys = ["d", "k"]
    global stimuli

    #  Get list of 40 random words
    face_words = ex.face_rows.NOUN.tolist()
    house_words = ex.house_rows.NOUN.tolist()
    random_words = face_words + house_words
    random.shuffle(random_words)

    #  Create intro routine
    intro_text = dict()
    intro_text['intro'] = ex.intro
    stimuli = [(st.Text, (intro_text, 0.05,
                          ex.intro_duration, ex.intro_key))]

    #  Create word stimuli
    for word in random_words:
        key_text = ex.rand_odd_key if is_odd else ex.rand_even_key
        display_text = dict()
        display_text[word] = word + "\n" + key_text
        stim = (st.Text, (display_text, 0.1, 0.0, default_keys))
        stimuli.append(stim)

    #  Add stimuli to paradigm
    par.addStimuli(stimuli)

    return par


if __name__ == "__main__":
    logging.console.setLevel(settings["logging_level"])
    run_experiment()
