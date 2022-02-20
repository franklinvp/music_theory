"""Define classes
 * noteA, noteB, ..., noteG
 * noteAb, noteBb, ..., noteGb
 * noteAs, noteBs, ..., noteGs
and classes
 * A, B, ..., G
 * Ab, Bb, ..., Gb
 * As, Bs, ..., Gs
"""

__note_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

class note:
    pass

def note_repr(name: str) -> str:
    return 

__g = globals()

# Note classes noteA, noteB, ..., noteG
for _name in __note_names:
    _note_name = 'note' + _name
    __g[_note_name] = type(
        _note_name,
        (note,),
        {
            '__repr__': lambda self, _my_name=_name: _my_name,
            '__hash__': lambda self: hash(_name)
        }
    )

# Flat note classes noteAb, noteBb, ..., noteGb
for _name in __note_names:
    _note_name = ''.join(['note', _name, 'b'])
    __g[_note_name] = type(
        _note_name,
        (note,),
        {
            '__repr__': lambda self, _my_name=_name + '♭': _my_name,
            '__hash__': lambda self: hash(_name + '♭')
        }
    )

# Sharp note names noteAs, noteBs, ..., noteGs
for _name in __note_names:
    _note_name = ''.join(['note', _name, 's'])
    __g[_note_name] = type(
        _note_name,
        (note,),
        {
            '__repr__': lambda self, _my_name=_name + '♯': _my_name,
            '__hash__': lambda self: hash(_name + '♯')
        }
    )

# Note instances A, B, ..., G
for _name in __note_names:
    __g[_name] = __g['note' + _name]()

# Flat note instances Ab, Bb, ..., Gb
for _name in __note_names:
    __g[_name + 'b'] = __g[''.join(['note', _name, 'b'])]()

# Sharp note instances As, Bs, ..., Gs
for _name in __note_names:
    __g[_name + 's'] = __g[''.join(['note', _name, 's'])]()

note_equivalences = {
    C: C,
    Cs: Cs,
    Db: Cs,
    D: D,
    Ds: Ds,
    Eb: Ds,
    E: E,
    Es: F,
    Fb: E,
    F: F,
    Fs: Fs,
    Gb: Fs,
    G: G,
    Gs: Gs,
    Ab: Gs,
    A: A,
    As: As,
    Bb: As,
    B: B,
    Bs: C,
}

def _add_interval(n: note, i: 'Interval') -> note:
    L = [C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B]
    return L[(L.index(note_equivalences[n]) + int(2*i.value)) % 12]
