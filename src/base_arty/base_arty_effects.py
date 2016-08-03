import math
import random
from decimal import Decimal as D
# import lib.loader
import json
import sys
import math
import copy

import loader

false = False
true = True

#########################################
base_string = loader.loads("""{
    "spec" : {
        "shader" : "particle_transparent",
        "shape" : "string",
        "red" : 5,
        "green" : 0.2,
        "blue" : 5,
        "alpha" : [[0, 0], [0.1, 1]],
        "size" : [[0, 0], [0.1, 1], [1, 0]],
        "dataChannelFormat": "PositionColorAndAlignVector",
        "baseTexture": "/pa/effects/textures/particles/flat.papa"
    },
    "emitterLifetime" : 1,
    "emissionRate" : 100,
    "lifetime" : 1,
    "sizeX" : 0.2,
    "cameraPush" : 0.5,
    "useWorldSpace" : true,
    "endDistance" : -1
}""")

base_trail = {
    "emitters" : []
}


base_hit_shell = loader.loads("""{
    "spec": {
        "shader": "particle_clip",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": [[0, 100 ], [0.35, 4 ] ],
        "green": [[0, 10 ], [0.35, 2 ] ],
        "blue": [[0, 100 ], [0.35, 20 ] ],
        "alpha": [[0.0, 0.4 ], [1, 0]],
        "size": [[0, 0 ], [0.1, 0.5 ], [0.2, 0.75 ], [0.3, 0.87 ], [0.4, 0.95 ], [0.5, 1 ]],
        "papa": "/pa/effects/fbx/particles/sphere_ico16seg.papa",
        "materialProperties": {
            "Texture": "/pa/effects/textures/particles/fire_puff.papa"
        }
    },
    "sizeX": 25,
    "sizeY": 25,
    "rotationRange": 3.2,
    "lifetime": 0.8,
    "emissionBursts": 1,
    "bLoop": false,
    "endDistance": 2000
}""")

base_hit_shell_inner = loader.loads("""{
    "spec": {
        "shader": "particle_clip",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": [[0, 100 ], [0.35, 20 ] ],
        "green": [[0, 10 ], [0.35, 2 ] ],
        "blue": [[0, 100 ], [0.35, 20 ] ],
        "alpha": [[0, 1 ], [0.8, 0.5], [1, 0]],
        "size": [[0, 0 ], [0.1, 0.5 ], [0.2, 1 ], [0.3, 0.87 ], [0.4, 0.7 ], [0.5, 0 ]],
        "papa": "/pa/effects/fbx/particles/sphere_ico16seg.papa",
        "materialProperties": {
            "Texture": "/pa/effects/textures/particles/flat.papa"
        }
    },
    "sizeX": 14,
    "sizeY": 10,
    "rotationRange": 3.2,
    "lifetime": 1.2,
    "emissionBursts": 1,
    "bLoop": false,
    "endDistance": 2000
}""")

base_hit_light = loader.loads("""{
    "spec": {
        "shape": "pointlight",
        "red": 6,
        "green": 0.4,
        "blue": 5,
        "alpha": [[0, 3 ], [0.25, 1 ], [1, 0 ] ]
    },
    "offsetZ" : 10,
    "sizeX": 30,
    "emissionBursts": 1,
    "lifetime": 0.8,
    "emitterLifetime": 0.5,
    "bLoop": false,
    "endDistance": 2000
}""")

base_hit_sparks = loader.loads("""{
    "spec": {
        "shader": "particle_add",
        "facing": "Velocity",
        "size": [[0, 0 ], [0.2, 1 ], [1, 0 ]],
        "red": 2,
        "green": 0.4,
        "blue": 0.1,
        "temp_alpha": [[0, 1 ], [1, 0 ] ],
        "baseTexture": "/pa/effects/textures/particles/dot.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionColorAndAlignVector"
    },
    "type": "SHELL",
    "offsetRangeX": 3,
    "offsetRangeY": 3,
    "offsetRangeZ": 3,
    "offsetAllowNegZ": true,
    "velocityZ": 0.0,
    "velocity": 70,
    "velocityRange": 20.0,
    "useRadialVelocityDir": true,
    "sizeX": 0.4,
    "sizeY": 19,
    "sizeRangeY": 7,
    "emissionBursts": 15,
    "lifetime": 0.5,
    "lifetimeRange": 0.1,
    "emitterLifetime": 0.1,
    "bLoop": false,
    "endDistance": 850
}""")

base_hit_rings = loader.loads("""[
{
      "spec": {
        "shader": "particle_add",
        "facing": "EmitterZ",
        "size": [[0, 0 ], [0.2, 0.667 ], [0.4, 0.889 ], [0.6, 0.963 ], [0.8, 0.98 ], [1, 1 ] ],
        "red": 0.05,
        "green": 0.35,
        "blue": 5.0,
        "alpha": [[0.2, 2 ], [0.3, 1 ], [0.6, 0.5 ], [1, 0 ] ],
        "baseTexture": "/pa/effects/textures/particles/simpleExplosionRing.papa",
        "cameraPush" : 0.2,
        "dataChannelFormat": "PositionAndColor"
      },
      "offsetZ": 1,
      "sizeX": 30,
      "emissionBursts": 1,
      "rotationRange": 3.1415,
      "lifetime": 0.25,
      "emitterLifetime": 1,
      "bLoop": false,
      "endDistance": 1000
    },
    {
      "spec": {
        "shader": "particle_add",
        "facing": "EmitterZ",
        "size": {"keys": [[0, 0 ], [0.2, 0.667 ], [0.4, 0.889 ], [0.6, 0.963 ], [0.8, 0.98 ], [1, 1 ] ], "stepped": false },
        "red": 0.05,
        "green": 0.35,
        "blue": 5.0,
        "alpha": {"keys": [[0, 1 ], [0.3, 1 ], [0.6, 0.05 ], [1, 0 ] ], "stepped": false },
        "cameraPush" : 0.2,
        "baseTexture": "/pa/effects/textures/particles/simpleExplosionRing.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 25,
      "offsetZ": 1.5,
      "emissionBursts": 1,
      "rotationRange": 0.5,
      "lifetime": 1,
      "emitterLifetime": 2,
      "bLoop": false,
      "sort": "NoSort",
      "endDistance": 1000
    },
    {
      "spec": {
        "shader": "particle_add",
        "facing": "EmitterZ",
        "size": {"keys": [[0, 0 ], [1, 1 ] ], "stepped": false },
        "red": 0.05,
        "green": 0.35,
        "blue": 5.0,
        "cameraPush" : 0.2,
        "alpha": {"keys": [[0, 1 ], [0.3, 1 ], [0.6, 0.02 ], [1, 0 ] ], "stepped": false },
        "baseTexture": "/pa/effects/textures/particles/simpleExplosionRing.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 60,
      "offsetZ": 1.5,
      "emissionBursts": 1,
      "rotationRange": 0.5,
      "lifetime": 0.8,
      "emitterLifetime": 2,
      "bLoop": false,
      "sort": "NoSort",
      "endDistance": 1000
    }
]""")

base_hit_smoke = loader.loads("""[
    {
        "spec": {
            "shader": "particle_transparent_ramp",
            "size": [[0, 0 ], [0.05, 1 ], [0.25, 1.2 ], [1, 0 ] ],
            "red": [[0, 10 ], [0.75, 10 ] ],
            "green": [[0, 3 ], [0.75, 1 ] ],
            "blue": [[0, 10 ], [0.75, 10 ] ],
            "alpha": [[0.5, 1 ], [1, 0 ] ],
            "cameraPush": 1,
            "baseTexture": "/pa/effects/textures/particles/simpleSmokeSingle.papa",
            "rampTexture": "/pa/effects/textures/particles/uncompressed/simpleSmokeCenter_ramp.papa",
            "dataChannelFormat": "PositionAndColor"
        },
        "type": "SHELL",
        "velocityZ": 0.25,
        "velocityRangeX": 0.1,
        "velocityRangeY": 0.1,
        "offsetRangeX" : 10,
        "offsetRangeY" : 10,
        "offsetRangeZ" : 10,
        "offsetAllowNegZ": false,
        "useRadialVelocityDir": true,
        "velocity": 6,
        "velocityRange" : 2,
        "sizeX": [[0, 2.5 ], [0.25, 0.1 ] ],
        "sizeRangeX": 0.3,
        "rampV": 0.25,
        "gravity": -0.1,
        "drag": 0.99,
        "dragRange" : 0.01,
        "emissionRate": 30,
        "maxParticles": 150,
        "rotationRange": 0.1,
        "rotationRateRange": 0.25,
        "lifetime": 2.8,
        "lifetimeRange": 0.25,
        "emitterLifetime": 0.9,
        "bLoop": false,
        "endDistance": 850
    },
    {
        "spec": {
            "shader": "particle_transparent_ramp",
            "size": [[0, 0 ], [0.05, 1 ], [0.25, 1.2 ], [1, 0 ] ],
            "red": [[0, 10 ], [0.75, 1 ] ],
            "green": [[0, 1 ], [0.75, 0.5 ] ],
            "blue": [[0, 10 ], [0.75, 1 ] ],
            "alpha": [[0, 0], [0.5, 0.5], [1, 0 ] ],
            "cameraPush": 1,
            "baseTexture": "/pa/effects/textures/particles/simpleSmoke.papa",
            "rampTexture": "/pa/effects/textures/particles/uncompressed/simpleSmokeCenter_ramp.papa",
            "dataChannelFormat": "PositionAndColor"
        },
        "type": "SHELL",
        "offsetZ": 0,
        "offsetRangeX": 2,
        "offsetRangeY": 2,
        "offsetRangeZ": 2,
        "offsetAllowNegZ": false,
        "velocityZ": 0.25,
        "velocityRangeX": 0.1,
        "velocityRangeY": 0.1,
        "useRadialVelocityDir": true,
        "velocity": 9,
        "sizeX": 10,
        "sizeRangeX": 0.5,
        "rampV": 0.5,
        "rampRangeV": 0.5,
        "gravity": -0.1,
        "drag": 0.985,
        "emissionBursts": 8,
        "rotationRange": 0.1,
        "rotationRateRange": 0.25,
        "lifetime": 2.8,
        "lifetimeRange": 0.25,
        "emitterLifetime": 2,
        "bLoop": false,
        "endDistance": 850
    }
]""")

base_hit = {
    "emitters" : []
}

def _round_time_curve(curve, digits=7):
    return [[round(x, digits), round(y, digits)] for [x,y] in curve]

# period - time to create waves over
# frequency - the lowest frequency wave with a period of 'period'
# waves - the number of sub wavelets to add to the system (will have a period that is equal to base)
# amplitude - how big the waves are
# amplitudeRange - range of amplitude size for sub wavelets
def sine(waves, amplitude, amplitudeRange):
    wavelets = []
    s = list(range(1, waves * 2))
    waves = int(waves)
    for w in range(waves):
        f = random.choice(s)
        s.remove(f)
        a = amplitude + random.uniform(-1, 1) * amplitudeRange
        b = f * math.pi * 2
        c = random.uniform(0, math.pi * 2)
        wavelets.append([a, b, c])
    return wavelets

def wave_to_offset(wavelets, period, dt):
    t = 0.0
    offset = []
    while t < period:
        v = 0
        for w in wavelets:
            v += w[0] * math.sin(w[1] * t / period * math.pi * 2 + w[2])
        offset.append([t, v])
        t += dt
    return offset

def run():
    ds = 0.05
    base_string['lifetime'] = 0.8
    wave_rings = [
            [0.50,  2, math.pi / 2],
            [0.75, -1, math.pi / 5],
            [0.25,  1, 2 * math.pi / 5],
            [0.75, -2, 3 * math.pi / 5],
            [0.75, +3, math.pi * 2 / 3],
            [0.75, -3, math.pi * 4 / 3]
            ]
    for t in range(5):
        string = copy.deepcopy(base_string)
        wave_x = wave_rings[t][:]
        wave_z = wave_rings[t][:]

        wave_x[1] *= 1
        wave_z[1] *= 1

        wave_z[2] += math.pi / 2

        wave_life = base_string['emitterLifetime']
        wave_ds = wave_life * ds

        string['offsetX'] = _round_time_curve(wave_to_offset([wave_x], wave_life, wave_ds))
        string['offsetZ'] = _round_time_curve(wave_to_offset([wave_z], wave_life, wave_ds))

        string['velocityX'] = _round_time_curve(wave_to_offset([wave_x], wave_life, wave_ds))
        string['velocityZ'] = _round_time_curve(wave_to_offset([wave_z], wave_life, wave_ds))

        string['velocity'] = 3.0
        string['drag'] = 0.97

        base_trail['emitters'].append(string)

    string = copy.deepcopy(base_string)

    string['lifetime'] = 1
    string['sizeX'] = 1
    string['spec']['green'] = [[0, 1], [1, 0.5]]

    base_trail['emitters'].append(string)

    base_hit['emitters'].append(base_hit_shell)
    base_hit['emitters'].append(base_hit_shell_inner)
    base_hit['emitters'].append(base_hit_light)
    base_hit['emitters'].append(base_hit_sparks)
    base_hit['emitters'].extend(base_hit_smoke)
    base_hit['emitters'].extend(base_hit_rings)
    # base_hit['emitters'].extend(base_hit_smoke_burst)

    loader.dump_effect(base_trail, "base_ammo_trail.pfx")
    loader.dump_effect(base_hit, "base_ammo_hit.pfx")


if __name__ == "__main__":
    run()
