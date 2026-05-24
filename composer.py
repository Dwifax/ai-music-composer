#!/usr/bin/env python3
"""AI Music Composer - Generate melodies, chord progressions, and arrangements."""
import random, sys
from dataclasses import dataclass, field
from typing import List

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALES = {
    "major": [0,2,4,5,7,9,11], "minor": [0,2,3,5,7,8,10],
    "pentatonic": [0,2,4,7,9], "blues": [0,3,5,6,7,10],
    "dorian": [0,2,3,5,7,9,10],
}
CHORDS = {"maj":[0,4,7], "min":[0,3,7], "dim":[0,3,6], "maj7":[0,4,7,11], "min7":[0,3,7,10], "dom7":[0,4,7,10]}
PROGRESSIONS = {
    "pop": [(0,"maj"),(4,"min"),(5,"maj"),(4,"min")],
    "jazz": [(0,"maj7"),(4,"min7"),(0,"maj7"),(4,"min7")],
    "epic": [(0,"min"),(3,"maj"),(4,"maj"),(4,"maj")],
    "sad": [(0,"min"),(3,"maj"),(5,"maj"),(4,"maj")],
}

@dataclass
class Note:
    pitch: int; duration: float; velocity: int = 80

class Scale:
    def __init__(self, root=60, scale_type="minor"):
        self.root = root; self.intervals = SCALES[scale_type]
    def notes(self, octaves=2):
        return [self.root + i + o*12 for o in range(octaves) for i in self.intervals]

class MelodyGenerator:
    def __init__(self, scale):
        self.scale = scale
    def generate(self, bars=16):
        notes = self.scale.notes(3); mid = len(notes)//2; idx = mid
        melody = []; beats = bars * 1.0
        while beats > 0:
            dur = random.choice([0.5, 0.5, 1.0, 1.0, 1.5, 2.0])
            dur = min(dur, beats)
            melody.append(Note(notes[min(idx, len(notes)-1)], dur, random.randint(60,100)))
            beats -= dur
            idx = max(0, min(len(notes)-1, idx + random.choices([-2,-1,0,1,2], [0.1,0.3,0.1,0.3,0.2])[0]))
        return melody

class ChordEngine:
    def __init__(self, scale):
        self.scale = scale
    def generate(self, style="pop", reps=2):
        template = PROGRESSIONS.get(style, PROGRESSIONS["pop"])
        chords = []
        for _ in range(reps):
            for deg, ctype in template:
                root = self.scale.root + self.scale.intervals[deg % len(self.scale.intervals)]
                notes = [root + i for i in CHORDS[ctype]]
                chords.append({"root": NOTES[root%12], "type": ctype, "notes": [NOTES[n%12] for n in notes]})
        return chords

def render(melody, chords):
    lines = ["AI Music Composer - Generated Score", "="*50, "", "CHORDS:"]
    beat = 0
    for c in chords:
        lines.append(f"  Beat {beat:5.1f}: {c['root']}{c['type']} ({', '.join(c['notes'])})")
        beat += 1.0
    lines.append("\nMELODY:")
    beat = 0
    for n in melody:
        name = NOTES[n.pitch % 12]; oct = n.pitch // 12 - 1
        lines.append(f"  Beat {beat:5.1f}: {name}{oct} ({n.duration}b, vel={n.velocity})")
        beat += n.duration
    lines.append(f"\nTotal: {len(melody)} notes, {len(chords)} chords")
    return "\n".join(lines)

if __name__ == "__main__":
    root = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    st = sys.argv[2] if len(sys.argv) > 2 else "minor"
    style = sys.argv[3] if len(sys.argv) > 3 else "epic"
    s = Scale(root, st)
    m = MelodyGenerator(s).generate(16)
    c = ChordEngine(s).generate(style)
    print(render(m, c))
