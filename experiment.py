import pandas as pd

#  Introduction
introduction = """YOU WILL NOW VIEW ANOTHER SERIES OF WORDS.
THESE ARE THE SAME WORDS YOU WERE ASKED TO 
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

PLEASE PRESS THE SPACE BAR WHEN YOU ARE READY TO BEGIN."""
introDuration = 2.0
introKey = "space"

#  Probes
houseProbe1 = "IS THIS A RESIDENTIAL OR COMMERCIAL BUILDING?"
houseProbe2 = "IS THIS A ONE STORY OR MULTISTORY BUILDING?"
houseProbe3 = "IS THIS A LIGHT COLORED OR A DARK COLORED BUILDING?"
faceProbe1 = "IS THIS A MALE FACE OR A FEMALE FACE?"
faceProbe2 = "IS THIS A YOUNGER PERSON OR AN OLDER PERSON?"
faceProbe3 = "IS THIS PERSON WHITE OR NOT WHITE?"

#  Key assignments for ODD users
houseKey1 = ["'D' = RESIDENTIAL, 'K' = COMMERCIAL"]
houseKey2 = ["'D' = ONE STORY, 'K' = MULTISTORY"]
houseKey3 = ["'D' = LIGHT, 'K' = DARK"]
faceKey1 = ["'D' = MALE, 'K' = FEMALE"]
faceKey2 = ["'D' = YOUNGER, 'K' = OLDER"]
faceKey3 = ["'D' = WHITE, 'K' = NOT WHITE"]

#  Key assignments for EVEN users
houseKey1 = ["'D' = COMMERCIAL, 'K' = RESIDENTIAL"]
houseKey2 = ["'D' = MULTISTORY, 'K' = ONE STORY"]
houseKey3 = ["'D' = DARK, 'K' = LIGHT"]
faceKey1 = ["'D' = FEMALE, 'K' = MALE"]
faceKey2 = ["'D' = OLDER, 'K' = YOUNGER"]
faceKey3 = ["'D' = NOT WHITE, 'K' = WHITE"]

excel_df = pd.read_excel('./Stim_AssociateMasterList.xlsx',
                         index_col=None, usecols='A,C:H')
face_rows = excel_df[excel_df.ASSOCIATE == "Face"].sample(20)
house_rows = excel_df[excel_df.ASSOCIATE == "House"].sample(20)
print(house_rows)
