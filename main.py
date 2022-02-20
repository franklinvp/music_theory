import notes
import chords
import intervals
from modes import root_mode_to_notes
from icecream import ic
from intensions import intension_root_mode_to_notes

def main():
    C = notes.C
    # print(C)
    Bb = notes.Bb
    # print(Bb)
    Gs = notes.Gs
    # print(Gs)
    ic(root_mode_to_notes['F♯', 'Dorian'])
    I = intervals.Interval(-0.5)
    # print(I)
    X = notes._add_interval(C, I)
    # print(X)
    M = X + I
    # print(M)
    ic(intension_root_mode_to_notes['F♯', 'Dorian'])

if __name__ == '__main__':
    main()