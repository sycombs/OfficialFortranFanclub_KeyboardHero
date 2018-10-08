"""@package docstring
   BeatmapGenerator_Proto.py is used to create quick and simple beatmaps by
   hand in order to test various structures and organizational formats

   Terminology:
        Structure: A repeated pattern or predetermined entry?
        Note: An dictionary entry that...



"""

# Generate a note
def create_note(structure = None):
"""
    create_note(structure = None) simply creates a single note

    Case 1: When no structure is passed, the user is prompted to enter all
         of the neccessary information. *** NOT CURRENTLY IMPLEMENTED ***

    Case 2: When a structure is passed, every entry is copied over

    *** NOTE: BECAUSE THIS IS A DEVELOPER TOOL ONLY, ERROR CHECKING WILL NOT
    BE ADDED UNTIL LATER
"""
    note = {}

    '''
    if structure is None:
        note['TimeToWait'] = input("Enter TimeToWait: ")
        note['Up']    = structure['Up']
        note['Down']  = structure['Down']
        note['Left']  = structure['Left']
        note['Right'] = structure['Right']input()
    '''

    else:
        note['TimeToWait'] = structure['TimeToWait']
        note['Up']    = structure['Up']
        note['Down']  = structure['Down']
        note['Left']  = structure['Left']
        note['Right'] = structure['Right']

    return note

def show_beatmap():
"""
    show_beatmap() displays all of the available beatmap data in the following
    format

    Note #n - TIME INITIATED: t [s]
    noteN = {'TimeToWait' : t, 'Up' : BOOL, 'Down' : BOOL, 'Left' : BOOL, 'Right' : BOOL}
"""
