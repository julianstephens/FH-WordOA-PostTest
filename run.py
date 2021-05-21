from psychopy import logging
from psychopy import core, gui, logging

import stimulus as st


def run_experiment():
    #  Get participant ID
    exp_info = {"participant": "", "session:": "001"}
    dlg = gui.DlgFromDict(exp_info, sortKeys=False,
                          title=st.settings["exp_name"])

    #  Save participant ID
    st.settings["participant"] = exp_info["participant"]

    if dlg.OK == False:
        core.quit()

    #  Check if participant ID is odd
    is_odd = True if int(exp_info["participant"]) % 2 != 0 else False

    #  Initialize experiment paradigm
    st.construct_par(is_odd)
    if st.par:
        #  Start clock for total experiment runtime
        experiment_timer = core.MonotonicClock()
        st.par.playAll(is_odd)
        elapsed = experiment_timer.getTime()


if __name__ == "__main__":
    logging.console.setLevel(st.settings["logging_level"])
    run_experiment()
