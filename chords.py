from notes import (
    A, B, C, D, E, F, G,
    Ab, Bb, Cb, Db, Eb, Fb, Gb,
    As, Bs, Cs, Ds, Es, Fs, Gs,
)

chords = {
    # Major
    'A': [A, Cs, E],
    'B': [B, Ds, Fs],
    'C': [C, E, G],
    'D': [D, Fs ,A],
    'E': [E, Gs, B],
    'F': [F, A, C],
    'G': [G, B, D],
    # Minor
    'Am': [A, C, E],
    'Bm': [B, D, Fs],
    'Cm': [C, Eb, G],
    'Dm': [D, F, A],
    'Em': [E, G, B],
    'Fm': [F, Ab, C],
    'Gm': [G, Bb, D],
    # Major 7th
    'A7': [A, Cs, E, Gs],
    'B7': [B, Ds, Fs, As],
    'C7': [C, E, G, B],
    'D7': [D, Fs ,A, Cs],
    'E7': [E, Gs, B, Ds],
    'F7': [F, A, C, E],
    'G7': [G, B, D, Fs],
    # Minot 7th
    'Am': [A, C, E, G],
    'Bm': [B, D, Fs, A],
    'Cm': [C, Eb, G, Bb],
    'Dm': [D, F, A, C],
    'Em': [E, G, B, D],
    'Fm': [F, Ab, C, Eb],
    'Gm': [G, Bb, D, F],
    # Diminished
    'Adim': [A, C, Eb],
    'Bdim': [B, D, F],
    'Cdim': [C, Eb, Gb],
    'Ddim': [D, F, Ab],
    'Edim': [E, G, Bb],
    'Fdim': [F, Ab, Cb],
    'Gdim': [G, Bb, Db],
}
