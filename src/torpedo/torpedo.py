import loader
import patcher

import math
import copy
import random

false = False
true = True

#########################################
base_string = {
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
}

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
    string['lifetime'] = 1.2

    # new_trail['emitters'].append(string)

    new_trail['emitters'].append({
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
        })


    return [
        {
            "target" : "/pa/ammo/torpedo/torpedo.json",
            "patch" : [
                {"op" : "replace", "path" : "/fx_trail/filename", "value" : "/mod/torpedo/torpedo_trail.json"}
            ]
        },
        {
            "target" : [
                "/pa/units/sea/frigate/frigate_ammo_torpedo.json",
                "/pa/units/sea/torpedo_launcher/torpedo_launcher_ammo.json",
                "/pa/units/sea/torpedo_launcher_adv/torpedo_launcher_adv_ammo.json",
                "/pa/units/sea/nuclear_sub/nuclear_sub_ammo.json",
                "/pa/units/land/assault_bot_adv/assault_bot_adv_torpedo_ammo.json",
                "/pa/units/commanders/base_commander/base_commander_torpedo_ammo.json"
            ],
            "patch" : [
                {"op" : "add", "path" : "/events", "value" : {
                    "died" : {
                        "effect_spec" : "/mod/torpedo/torpedo_hit.json",
                        "effect_scale" : 0.15
                    }
                }}
            ]
        },
        {
            "target" : "/pa/effects/specs/torpedo_proj_trail.pfx",
            "destination" : "/mod/torpedo/torpedo_trail.json",
            "patch" : [
                { "op" : "replace", "path" : "", "value" : new_trail}
            ]
        },
        {
            "target": "/base_arty/base_ammo_hit.json",
            "destination" : "/mod/torpedo/torpedo_hit.json",
            "patch" : [
              {"op" : "replace", "path" : "/emitters/0/spec/red",   "value" : [[0, 100 ], [0.35, 4 ]]},
              {"op" : "replace", "path" : "/emitters/0/spec/green", "value" : [[0, 10 ], [0.35, 2 ]]},
              {"op" : "replace", "path" : "/emitters/0/spec/blue",  "value" : [[0, 30 ], [0.35, 2]]},

              {"op" : "replace", "path" : "/emitters/1/spec/red",   "value" : [[0, 100 ], [0.35, 20 ]]},
              {"op" : "replace", "path" : "/emitters/1/spec/green", "value" : [[0, 10 ], [0.35, 2]]},
              {"op" : "replace", "path" : "/emitters/1/spec/blue",  "value" : [[0, 30 ], [0.35, 2]]},

              {"op" : "replace", "path" : "/emitters/4/spec/red",   "value" : [[0, 10 ], [0.75, 10 ]]},
              {"op" : "replace", "path" : "/emitters/4/spec/green", "value" : [[0, 3  ], [0.75, 1 ]]},
              {"op" : "replace", "path" : "/emitters/4/spec/blue",  "value" : [[0, 8 ], [0.75, 5]]},

              {"op" : "replace", "path" : "/emitters/5/spec/red",   "value" : [[0, 10 ], [0.75, 1 ]]},
              {"op" : "replace", "path" : "/emitters/5/spec/green", "value" : [[0, 1 ], [0.75, 0.5 ]]},
              {"op" : "replace", "path" : "/emitters/5/spec/blue",  "value" : [[0, 1 ], [0.75, 0.5]]},

              {"op" : "replace", "path" : "/emitters/2/spec/red",   "value" : 6.0},
              {"op" : "replace", "path" : "/emitters/2/spec/green", "value" : 0.4},
              {"op" : "replace", "path" : "/emitters/2/spec/blue",  "value" : 0.1}
            ]
        }
    ]
