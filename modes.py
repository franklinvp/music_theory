from functools import partial
from collections import namedtuple 

mode_names = [
    'Ionian',
    'Dorian',
    'Phrygian',
    'Lydian',
    'Mixolydian',
    'Aeolian',
    'Locrian'
]

major_steps = [0, 2, 4, 5, 7, 9, 11]

mode_to_interval_from_root = {}
for i in range(7):
    mode_to_interval_from_root[mode_names[i]] = list(
        map(
            partial(lambda x,i: (x - major_steps[i]) % 12, i=i),
            (major_steps + major_steps)[i: i + 7]
        )
    )
# The result of this computation is
# mode_to_interval_from_root = {
#     'Aeolian': [0, 2, 3, 5, 7, 8, 10],
#     'Dorian': [0, 2, 3, 5, 7, 9, 10],
#     'Ionian': [0, 2, 4, 5, 7, 9, 11],
#     'Locrian': [0, 1, 3, 5, 6, 8, 10],
#     'Lydian': [0, 2, 4, 6, 7, 9, 11],
#     'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
#     'Phrygian': [0, 1, 3, 5, 7, 8, 10]
# }

FormattedNotes = namedtuple('Formatted_names', ['names', 'accidentals'])
Note = namedtuple('Note', ['baseNote', 'accidental'])
NoteFamily = namedtuple('NoteFamily', ['notes', 'accidentals'])
Mode = namedtuple(
    'Mode',
    ['mode', 'rootNote', 'selected', 'notes', 'root'],
    defaults=[None, None]
)


def next_base_note(note):
        # 65 below is ord('A') and 7 is the number of letters in 'ABCDEFG'
        return chr(((ord(note) - 65) + 1) % 7 + 65)


def get_mode_note_names(starting_note, mode):
    mode_notes = list(
        map(
            lambda x: (x + starting_note) % 12,
            mode_to_interval_from_root[mode]
        )
    )
    interval_from_c_to_note = {
        0: 'C',
        2: 'D',
        4: 'E',
        5: 'F',
        7: 'G',
        9: 'A',
        11: 'B'
    }
    note_to_interval_from_c = {v:k for k,v in interval_from_c_to_note.items()}
    def _(sharp, offset):
        if sharp:
            baseNote = (
                interval_from_c_to_note[(starting_note - offset) %12]
                if interval_from_c_to_note.get((starting_note - offset)%12)
                else interval_from_c_to_note[(starting_note - (offset - 1))%12]
            )
            accidentals = (
                (starting_note - note_to_interval_from_c[baseNote]) % 12
            )
            notes = [Note(baseNote=baseNote, accidental=accidentals)]
            for i in range(1,7):
                baseNote = next_base_note(baseNote)
                accidental = (
                    (mode_notes[i] - note_to_interval_from_c[baseNote])%12
                )
                notes.append(Note(baseNote=baseNote, accidental=accidental))
                accidentals += accidental
        else:
            baseNote = (
                interval_from_c_to_note.get((starting_note + offset) % 12)
                if interval_from_c_to_note.get((starting_note + offset) % 12)
                else interval_from_c_to_note[
                    (starting_note + (offset - 1)) % 12
                ]
            )
            accidentals = starting_note - note_to_interval_from_c[baseNote]
            if (accidentals > 0):
                accidentals = accidentals - 12
            notes = [Note(baseNote=baseNote, accidental=accidentals)]
            for i in range(1, 7):
                baseNote = next_base_note(baseNote)
                accidental = (
                    (mode_notes[i] - note_to_interval_from_c[baseNote]) % 12
                )
                if (accidental > 0):
                    accidental = accidental - 12
                accidentals += accidental
                notes.append(Note(baseNote=baseNote, accidental=accidental))
        return NoteFamily(notes=notes, accidentals=accidentals)
    sharps1 = _(True, 2)
    sharps2 = _(True, 1)
    sharps3 = _(True, 0)
    flats0 = _(False, 0)
    flats1 = _(False, 1)
    flats2 = _(False, 2)
    bestSharp = sorted(
        [
            sharps1,
            sharps2,
            sharps3
        ],
        key=lambda a: abs(a.accidentals)
    )[0]
    bestFlat = sorted(
        [
            flats0,
            flats1,
            flats2
        ],
        key=lambda a: abs(a.accidentals)
    )[0]
    def formatNotes(a):
        notes = list(
            map(
                lambda x: x.baseNote + (
                    ''
                    if x.accidental == 0
                    else (
                        (x.accidental)*'♯'
                        if x.accidental > 0
                        else (-x.accidental)*'♭'
                    )
                ),
                a.notes
            )
        )
        return FormattedNotes(names=notes, accidentals=a.accidentals)
    outObject = Mode(mode=mode, rootNote=starting_note, selected=False)
    if (
        bestSharp.accidentals < -bestFlat.accidentals
        or bestSharp.accidentals == 0
    ):
        outObject = outObject._replace(notes=[formatNotes(bestSharp)])
        outObject = outObject._replace(root=outObject.notes[0].names[0])
    elif (bestSharp.accidentals > -bestFlat.accidentals):
        outObject = outObject._replace(notes=[formatNotes(bestFlat)])
        outObject = outObject._replace(root=outObject.notes[0].names[0])
    else:
        outObject = outObject._replace(
            notes=list(
                map(lambda x: formatNotes(x), [bestSharp, bestFlat])
            )
        )
        outObject = outObject._replace(
            root = (
                f'{outObject.notes[0].names[0]} / {outObject.notes[1].names[0]}'
            )
        )
    return outObject

def createData():
    data = []
    for i in range(12):
        for mode in mode_names:
            data.append(get_mode_note_names(i, mode))
    return data


root_mode_to_notes = {}
for entry in createData():
    if '/' in entry.root:
        for idx, root in enumerate(entry.root.split(' / ')):
            root_mode_to_notes[(root, entry.mode)] = entry.notes[idx].names
    else:
        root_mode_to_notes[(entry.root, entry.mode)] = entry.notes[0].names

# This is the result put in a dictionary
# root_mode_to_notes = {
#     ('A', 'Aeolian'): ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
#     ('A', 'Dorian'): ['A', 'B', 'C', 'D', 'E', 'F♯', 'G'],
#     ('A', 'Ionian'): ['A', 'B', 'C♯', 'D', 'E', 'F♯', 'G♯'],
#     ('A', 'Locrian'): ['A', 'B♭', 'C', 'D', 'E♭', 'F', 'G'],
#     ('A', 'Lydian'): ['A', 'B', 'C♯', 'D♯', 'E', 'F♯', 'G♯'],
#     ('A', 'Mixolydian'): ['A', 'B', 'C♯', 'D', 'E', 'F♯', 'G'],
#     ('A', 'Phrygian'): ['A', 'B♭', 'C', 'D', 'E', 'F', 'G'],
#     ('A♭', 'Dorian'): ['A♭', 'B♭', 'C♭', 'D♭', 'E♭', 'F', 'G♭'],
#     ('A♭', 'Ionian'): ['A♭', 'B♭', 'C', 'D♭', 'E♭', 'F', 'G'],
#     ('A♭', 'Lydian'): ['A♭', 'B♭', 'C', 'D', 'E♭', 'F', 'G'],
#     ('A♭', 'Mixolydian'): ['A♭', 'B♭', 'C', 'D♭', 'E♭', 'F', 'G♭'],
#     ('A♯', 'Locrian'): ['A♯', 'B', 'C♯', 'D♯', 'E', 'F♯', 'G♯'],
#     ('A♯', 'Phrygian'): ['A♯', 'B', 'C♯', 'D♯', 'E♯', 'F♯', 'G♯'],
#     ('B', 'Aeolian'): ['B', 'C♯', 'D', 'E', 'F♯', 'G', 'A'],
#     ('B', 'Dorian'): ['B', 'C♯', 'D', 'E', 'F♯', 'G♯', 'A'],
#     ('B', 'Ionian'): ['B', 'C♯', 'D♯', 'E', 'F♯', 'G♯', 'A♯'],
#     ('B', 'Locrian'): ['B', 'C', 'D', 'E', 'F', 'G', 'A'],
#     ('B', 'Lydian'): ['B', 'C♯', 'D♯', 'E♯', 'F♯', 'G♯', 'A♯'],
#     ('B', 'Mixolydian'): ['B', 'C♯', 'D♯', 'E', 'F♯', 'G♯', 'A'],
#     ('B', 'Phrygian'): ['B', 'C', 'D', 'E', 'F♯', 'G', 'A'],
#     ('B♭', 'Aeolian'): ['B♭', 'C', 'D♭', 'E♭', 'F', 'G♭', 'A♭'],
#     ('B♭', 'Dorian'): ['B♭', 'C', 'D♭', 'E♭', 'F', 'G', 'A♭'],
#     ('B♭', 'Ionian'): ['B♭', 'C', 'D', 'E♭', 'F', 'G', 'A'],
#     ('B♭', 'Lydian'): ['B♭', 'C', 'D', 'E', 'F', 'G', 'A'],
#     ('B♭', 'Mixolydian'): ['B♭', 'C', 'D', 'E♭', 'F', 'G', 'A♭'],
#     ('B♭', 'Phrygian'): ['B♭', 'C♭', 'D♭', 'E♭', 'F', 'G♭', 'A♭'],
#     ('C', 'Aeolian'): ['C', 'D', 'E♭', 'F', 'G', 'A♭', 'B♭'],
#     ('C', 'Dorian'): ['C', 'D', 'E♭', 'F', 'G', 'A', 'B♭'],
#     ('C', 'Ionian'): ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
#     ('C', 'Locrian'): ['C', 'D♭', 'E♭', 'F', 'G♭', 'A♭', 'B♭'],
#     ('C', 'Lydian'): ['C', 'D', 'E', 'F♯', 'G', 'A', 'B'],
#     ('C', 'Mixolydian'): ['C', 'D', 'E', 'F', 'G', 'A', 'B♭'],
#     ('C', 'Phrygian'): ['C', 'D♭', 'E♭', 'F', 'G', 'A♭', 'B♭'],
#     ('C♭', 'Lydian'): ['C♭', 'D♭', 'E♭', 'F', 'G♭', 'A♭', 'B♭'],
#     ('C♯', 'Aeolian'): ['C♯', 'D♯', 'E', 'F♯', 'G♯', 'A', 'B'],
#     ('C♯', 'Dorian'): ['C♯', 'D♯', 'E', 'F♯', 'G♯', 'A♯', 'B'],
#     ('C♯', 'Locrian'): ['C♯', 'D', 'E', 'F♯', 'G', 'A', 'B'],
#     ('C♯', 'Mixolydian'): ['C♯', 'D♯', 'E♯', 'F♯', 'G♯', 'A♯', 'B'],
#     ('C♯', 'Phrygian'): ['C♯', 'D', 'E', 'F♯', 'G♯', 'A', 'B'],
#     ('D', 'Aeolian'): ['D', 'E', 'F', 'G', 'A', 'B♭', 'C'],
#     ('D', 'Dorian'): ['D', 'E', 'F', 'G', 'A', 'B', 'C'],
#     ('D', 'Ionian'): ['D', 'E', 'F♯', 'G', 'A', 'B', 'C♯'],
#     ('D', 'Locrian'): ['D', 'E♭', 'F', 'G', 'A♭', 'B♭', 'C'],
#     ('D', 'Lydian'): ['D', 'E', 'F♯', 'G♯', 'A', 'B', 'C♯'],
#     ('D', 'Mixolydian'): ['D', 'E', 'F♯', 'G', 'A', 'B', 'C'],
#     ('D', 'Phrygian'): ['D', 'E♭', 'F', 'G', 'A', 'B♭', 'C'],
#     ('D♭', 'Ionian'): ['D♭', 'E♭', 'F', 'G♭', 'A♭', 'B♭', 'C'],
#     ('D♭', 'Lydian'): ['D♭', 'E♭', 'F', 'G', 'A♭', 'B♭', 'C'],
#     ('D♭', 'Mixolydian'): ['D♭', 'E♭', 'F', 'G♭', 'A♭', 'B♭', 'C♭'],
#     ('D♯', 'Aeolian'): ['D♯', 'E♯', 'F♯', 'G♯', 'A♯', 'B', 'C♯'],
#     ('D♯', 'Locrian'): ['D♯', 'E', 'F♯', 'G♯', 'A', 'B', 'C♯'],
#     ('D♯', 'Phrygian'): ['D♯', 'E', 'F♯', 'G♯', 'A♯', 'B', 'C♯'],
#     ('E', 'Aeolian'): ['E', 'F♯', 'G', 'A', 'B', 'C', 'D'],
#     ('E', 'Dorian'): ['E', 'F♯', 'G', 'A', 'B', 'C♯', 'D'],
#     ('E', 'Ionian'): ['E', 'F♯', 'G♯', 'A', 'B', 'C♯', 'D♯'],
#     ('E', 'Locrian'): ['E', 'F', 'G', 'A', 'B♭', 'C', 'D'],
#     ('E', 'Lydian'): ['E', 'F♯', 'G♯', 'A♯', 'B', 'C♯', 'D♯'],
#     ('E', 'Mixolydian'): ['E', 'F♯', 'G♯', 'A', 'B', 'C♯', 'D'],
#     ('E', 'Phrygian'): ['E', 'F', 'G', 'A', 'B', 'C', 'D'],
#     ('E♭', 'Aeolian'): ['E♭', 'F', 'G♭', 'A♭', 'B♭', 'C♭', 'D♭'],
#     ('E♭', 'Dorian'): ['E♭', 'F', 'G♭', 'A♭', 'B♭', 'C', 'D♭'],
#     ('E♭', 'Ionian'): ['E♭', 'F', 'G', 'A♭', 'B♭', 'C', 'D'],
#     ('E♭', 'Lydian'): ['E♭', 'F', 'G', 'A', 'B♭', 'C', 'D'],
#     ('E♭', 'Mixolydian'): ['E♭', 'F', 'G', 'A♭', 'B♭', 'C', 'D♭'],
#     ('E♯', 'Locrian'): ['E♯', 'F♯', 'G♯', 'A♯', 'B', 'C♯', 'D♯'],
#     ('F', 'Aeolian'): ['F', 'G', 'A♭', 'B♭', 'C', 'D♭', 'E♭'],
#     ('F', 'Dorian'): ['F', 'G', 'A♭', 'B♭', 'C', 'D', 'E♭'],
#     ('F', 'Ionian'): ['F', 'G', 'A', 'B♭', 'C', 'D', 'E'],
#     ('F', 'Locrian'): ['F', 'G♭', 'A♭', 'B♭', 'C♭', 'D♭', 'E♭'],
#     ('F', 'Lydian'): ['F', 'G', 'A', 'B', 'C', 'D', 'E'],
#     ('F', 'Mixolydian'): ['F', 'G', 'A', 'B♭', 'C', 'D', 'E♭'],
#     ('F', 'Phrygian'): ['F', 'G♭', 'A♭', 'B♭', 'C', 'D♭', 'E♭'],
#     ('F♯', 'Aeolian'): ['F♯', 'G♯', 'A', 'B', 'C♯', 'D', 'E'],
#     ('F♯', 'Dorian'): ['F♯', 'G♯', 'A', 'B', 'C♯', 'D♯', 'E'],
#     ('F♯', 'Ionian'): ['F♯', 'G♯', 'A♯', 'B', 'C♯', 'D♯', 'E♯'],
#     ('F♯', 'Locrian'): ['F♯', 'G', 'A', 'B', 'C', 'D', 'E'],
#     ('F♯', 'Mixolydian'): ['F♯', 'G♯', 'A♯', 'B', 'C♯', 'D♯', 'E'],
#     ('F♯', 'Phrygian'): ['F♯', 'G', 'A', 'B', 'C♯', 'D', 'E'],
#     ('G', 'Aeolian'): ['G', 'A', 'B♭', 'C', 'D', 'E♭', 'F'],
#     ('G', 'Dorian'): ['G', 'A', 'B♭', 'C', 'D', 'E', 'F'],
#     ('G', 'Ionian'): ['G', 'A', 'B', 'C', 'D', 'E', 'F♯'],
#     ('G', 'Locrian'): ['G', 'A♭', 'B♭', 'C', 'D♭', 'E♭', 'F'],
#     ('G', 'Lydian'): ['G', 'A', 'B', 'C♯', 'D', 'E', 'F♯'],
#     ('G', 'Mixolydian'): ['G', 'A', 'B', 'C', 'D', 'E', 'F'],
#     ('G', 'Phrygian'): ['G', 'A♭', 'B♭', 'C', 'D', 'E♭', 'F'],
#     ('G♭', 'Ionian'): ['G♭', 'A♭', 'B♭', 'C♭', 'D♭', 'E♭', 'F'],
#     ('G♭', 'Lydian'): ['G♭', 'A♭', 'B♭', 'C', 'D♭', 'E♭', 'F'],
#     ('G♯', 'Aeolian'): ['G♯', 'A♯', 'B', 'C♯', 'D♯', 'E', 'F♯'],
#     ('G♯', 'Dorian'): ['G♯', 'A♯', 'B', 'C♯', 'D♯', 'E♯', 'F♯'],
#     ('G♯', 'Locrian'): ['G♯', 'A', 'B', 'C♯', 'D', 'E', 'F♯'],
#     ('G♯', 'Phrygian'): ['G♯', 'A', 'B', 'C♯', 'D♯', 'E', 'F♯']
# }
