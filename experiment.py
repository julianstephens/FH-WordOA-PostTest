import pandas as pd

#  Experiment defaults
default_duration = 0.0
default_keys = ["d", "k"]
default_text_height = 0.1

#  Introduction
intro = """YOU WILL NOW VIEW ANOTHER SERIES OF WORDS.  THESE ARE THE SAME WORDS YOU WERE ASKED TO 
REMEMBER DURING THE PREVIOUS SEGMENTS.
WHEN YOU SEE THE WORD, YOU WILL AGAIN BE ASKED
TO INDICATE WHETHER THIS WORD WAS ASSOCIATED WITH
OF A FACE OR A PICTURE OF A HOUSE. AFTER SOME
RESPONSES YOU MAY BE ASKED A FOLLOW UP QUESTION
ABOUT THE DETAILS YOU REMEMBER ABOUT THE ASSOCIATED
IMAGE. IF YOU DO NOT KNOW THE ANSWER, PLEASE MAKE
YOUR BEST GUESS. YOU WILL HAVE 6 SECONDS TO RESPOND
SO PLEASE TAKE YOUR TIME AND BE AS ACCURATE AS 
POSSIBLE. 

PLEASE PRESS D or K WHEN YOU ARE READY TO BEGIN."""
intro_text_height = 0.05

#  Uncomment below to set separate defaults for introduction
#  intro_duration = 0.0
#  intro_key = ["d", "k"]

#  Noun key assignments
noun_odd_key = "'D' = BUILDING, 'K' = FACE"
noun_even_key = "'D' = FACE, 'K' =  BUILDING"

#  Probes
house_probe_1 = "IS THIS A RESIDENTIAL OR COMMERCIAL BUILDING?"
house_probe_2 = "IS THIS A ONE STORY OR MULTISTORY BUILDING?"
house_probe_3 = "IS THIS A LIGHT COLORED OR A DARK COLORED BUILDING?"
face_probe_1 = "IS THIS A MALE FACE OR A FEMALE FACE?"
face_probe_2 = "IS THIS A YOUNGER PERSON OR AN OLDER PERSON?"
face_probe_3 = "IS THIS PERSON WHITE OR NOT WHITE?"

#  Probe key assignments for ODD users
house_key_odd_1 = ["'D' = RESIDENTIAL, 'K' = COMMERCIAL"]
house_key_odd_2 = ["'D' = ONE STORY, 'K' = MULTISTORY"]
house_key_odd_3 = ["'D' = LIGHT, 'K' = DARK"]
face_key_odd_1 = ["'D' = MALE, 'K' = FEMALE"]
face_key_odd_2 = ["'D' = YOUNGER, 'K' = OLDER"]
face_key_odd_3 = ["'D' = WHITE, 'K' = NOT WHITE"]

#  Probe key assignments for EVEN users
house_key_even_1 = ["'D' = COMMERCIAL, 'K' = RESIDENTIAL"]
house_key_even_2 = ["'D' = MULTISTORY, 'K' = ONE STORY"]
house_key_even_3 = ["'D' = DARK, 'K' = LIGHT"]
face_key_even_1 = ["'D' = FEMALE, 'K' = MALE"]
face_key_even_2 = ["'D' = OLDER, 'K' = YOUNGER"]
face_key_even_3 = ["'D' = NOT WHITE, 'K' = WHITE"]

#  ----DO NOT MODIFY BELOW----
house_list_odd = [(house_probe_1, house_key_odd_1), (house_probe_2,
                                                     house_key_odd_2), (house_probe_3, house_key_odd_3)]
house_list_even = [(house_probe_1, house_key_even_1), (house_probe_2,
                                                       house_key_even_2), (house_probe_3, house_key_even_3)]
face_list_odd = [(face_probe_1, face_key_odd_1), (face_probe_2,
                                                  face_key_odd_2), (face_probe_3, face_key_odd_3)]
face_list_even = [(face_probe_1, face_key_even_1), (face_probe_2,
                                                    face_key_even_2), (face_probe_3, face_key_even_3)]
#  ----DO NOT MODIFY ABOVE----

#  Load stim list and get 40 random rows
excel_df = pd.read_excel('resources/Stim_AssociateMasterList.xlsx',
                         index_col=None, usecols='A,C:H')
face_rows = excel_df[excel_df.ASSOCIATE == "Face"].sample(20)
house_rows = excel_df[excel_df.ASSOCIATE == "House"].sample(20)

#  Location of log files (if outside project directory, be sure to use the full path)
log_dir = "logs"
