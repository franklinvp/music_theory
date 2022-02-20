
from modes import root_mode_to_notes
import chords

intension = {
    'stability': {1, 3, 6},
    'change': {4, 2},
    'tension': {5, 7}
}

intension_root_mode_to_notes = {}
for root_mode, notes in root_mode_to_notes.items():
    intension_root_mode_to_notes[root_mode] = {
        intsion: [notes[_ - 1] for _ in intension[intsion]] for intsion in intension
    }