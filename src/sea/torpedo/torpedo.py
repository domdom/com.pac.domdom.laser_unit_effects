import loader
import patcher

import math
import copy
import random

false = False
true = True

#########################################
base_string = loader.loads("""{
    "spec" : {
        "shader" : "particle_transparent",
        "shape" : "string",
        "red" : 5,
        "green" : 0.8,
        "blue" : 0.8,
        "alpha" : [[0, 1], [0.1, 1], [1, 0]],
        "size" : [[0, 1], [0.1, 1], [1, 0]],
        "cameraPush" : 0.4,
        "dataChannelFormat": "PositionColorAndAlignVector",
        "baseTexture": "/pa/effects/textures/particles/flat.papa"
    },
    "emissionRate" : 30,
    "emitterLifetime" : 3.0,

    "velocityRangeX" : 0.1,
    "velocityRangeZ" : 0.1,
    "velocity" : 0.6,
    "drag" : 0.98,
    "lifetime" : 1,
    "sizeX" : 0.2,
    "sizeRangeX" : 0.15,
    "cameraPush" : 0.5,
    "useWorldSpace" : true,
    "alignVelocityToSurface" : true,
    "bLoop" : true,
    "endDistance" : 2000
}""")

# period - time to create waves over
# frequency - the lowest frequency wave with a period of 'period'
# waves - the number of sub wavelets to add to the system (will have a period that is equal to base)
# amplitude - how big the waves are
# amplitudeRange - range of amplitude size for sub wavelets
def sine(waves, amplitude, amplitudeRange=0):
    wavelets = []
    s = list(range(1, waves * 2))
    waves = int(waves)
    for w in range(waves):
        f = random.choice(s)
        s.remove(f)
        a = amplitude + random.uniform(-1, 1) * amplitudeRange
        b = f * math.pi * 2
        c = random.uniform(0, math.pi * 2)
        wavelets.append([a, b, c, 0])
    return wavelets

def wave_to_offset(wavelets, period, dt):
    t = 0.0
    offset = []
    while t < period:
        v = 0
        for w in wavelets:
            v += w[0] * math.sin(w[1] * t / period * math.pi * 2 + w[2]) + w[3]
        offset.append([t, v])
        t += dt
    return offset

def run():
    new_trail = { "emitters" : []}

    base_string['lifetime'] = 1

    string = copy.deepcopy(base_string)
    new_trail['emitters'].append(string)
    string = copy.deepcopy(base_string)
    string['spec']['red'] = 1.0
    string['spec']['green'] = 1.0
    string['spec']['blue'] = 1.0
    string['spec']['cameraPush'] = 0
    string['spec']['alpha'] = 0.1
    string['velocity'] = 0
    string['lifetime'] = 0.8

    # new_trail['emitters'].append(string)

    new_trail['emitters'].append(loader.loads("""{
            "spec" : {
                "shader" : "particle_add",
                "facing" : "axialY",
                "red" : 2.0,
                "green" : 0.2,
                "blue" : 0.4,
                "cameraPush" : 0.5,
                "baseTexture" : "/pa/effects/textures/particles/dot.papa"
            },
            "emissionBurts" : 1,
            "lifetime" : 0.2,
            "sizeX" : 0.6,
            "sizeY" : 1,
            "offsetY" : 1.2
        }"""))

    loader.dump_effect(new_trail, 'torpedo_trail.pfx')
