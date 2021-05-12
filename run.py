from psychopy import logging
import random
import sys

import pandas as pd
from psychopy import core, gui, logging
import xlsxwriter

import experiment as ex
import stimulus as st


def run_experiment():
    exp_info = {"participant": "", "session:": "001"}
    dlg = gui.DlgFromDict(exp_info, sortKeys=False, title=st.settings["exp_name"])

    if dlg.OK == False:
        core.quit()

    #  Check if participant ID is odd
    is_odd = True if int(exp_info["participant"]) % 2 != 0 else False

    #  Initialize experiment paradigm
    st.constructPar(is_odd)
    if st.par:
        #  Start clock for total experiment runtime
        experiment_timer = core.MonotonicClock()
        st.par.playAll(is_odd)
        sys.stdout.flush()

        #  Write total runtime to log
        exp_runtime = experiment_timer.getTime()
        ex.log_df.at[0, 'Experiment_Runtime'] = exp_runtime

        #  Dump logs to xlsx
        log_path = st.settings["log_file"]
        writer = pd.ExcelWriter(log_path, engine='xlsxwriter')
        ex.log_df.to_excel(writer, 'Experiment Info')
        ex.key_log_df.to_excel(writer, 'Key Responses')
        writer.close()



if __name__ == "__main__":
    logging.console.setLevel(st.settings["logging_level"])
    run_experiment()
