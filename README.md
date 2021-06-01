# FH_WordOA_PostTest

## File Structure

### `fh_wordoa_posttest.py`: Main file

This file contains the application's main method. See comments for code explanation.

### `experiment.py`: Stimulus definitions

This is where the introduction text is defined, as well as the probe text. The default keys and durations can also be found here.
Additionally, the list of 40 random nouns is pulled from `Stim_AssociateMasterList.xlsx` her.

### `settings.py`: Psychopy logging settings

This file contains the default settings for the experiment logging and naming. It also defines the window dimensions, experiment name, mouse visibility, etc.
Additional settings can be added here depending on needs.

### `stimulus.py`: Paradigm and Stimulus classes

This is where the brunt of the experiment logic is housed.

Notable Functions

- construct_par: initializes experiment paradigm
- get_probe: chooses probe type and inserts at front of stim list
- WaitForKey.run_event: answer processing after user input received
- Paradigm.playNext: contains log dump to csv

### `Stim_AssociateMasterList.xlsx`

Excel sheet with master list of available nouns and their attributes. **Note: if the location of this file changes, make sure to update the `excel_df` assignment in `experiment.py`**

## Modifying the Experiment

Most of modifications will occur in `experiment.py` or `Stim_AssociateMasterList.xlsx`. **After modifying any of the project files, you'll need to rebuild the executable.** See below for instructions on how to do so. 

### How to create a new `fh_wordoa_posttest.exe`

We will be using the Python package [Nuitka](https://nuitka.net/doc/user-manual.html) to do this. If you don't already have Python and Nuitka installed, download the latest version of Python [here](https://www.python.org/downloads/) (be sure to check the box to add Python to your environment variables). In your terminal (command line for Windows), type the following command to verify that Python is installed correctly: `python --version`. Now to install Nuitka, use the command `python -m pip install nuitka`. You can verify the installation with `python -m nuitka --version`. 

Once Python and Nuitka are installed, navigate to the project directory. Once in the directory, use the command `python -m nuitka --follow-imports fh_wordoa_posttest.py` to generate an executable. This may take a long time to complete depending on your computer. When the command is finished executing, you should see a program called `fh_wordoa_posttest.exe` in the project directory. **Note: The executable type will reflect the operating system that it's being generated on (i.e. running this command on a Windows computer will result in a Windows executable)**
