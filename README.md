# FH_WordOA_PostTest

## `run.py`: Main file

This file contains the application's main method. See comments for code explanation.

## `experiment.py`: Stimulus definitions

This is where the introduction text is defined, as well as the probe text. The default keys and durations can also be found here.
Additionally, the list of 40 random nouns is pulled from `Stim_AssociateMasterList.xlsx` her.

## `settings.py`: Psychopy logging settings

This file contains the default settings for the experiment logging and naming. It also defines the window dimensions, experiment name, mouse visibility, etc.
Additional settings can be added here depending on needs.

## `stimulus.py`: Paradigm and Stimulus classes

This is where the brunt of the experiment logic is housed.

Notable Functions

- construct_par: initializes experiment paradigm
- get_probe: chooses probe type and inserts at front of stim list
- WaitForKey.run_event: answer processing after user input received
- Paradigm.playNext: contains log dump to csv

## `Stim_AssociateMasterList.xlsx`

Excel sheet with master list of available nouns and their attributes. **Note**: if the location of this file changes, make sure to update the `excel_df` assignment in `experiment.py`
