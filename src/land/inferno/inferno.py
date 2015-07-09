import copy
import math

import loader

def trail():
    base_effect = loader.loads('{"emitters":[]}')

    base_spark = loader.loads("""{
        "spec" : {
            "shader": "particle_transparent",
            "shape": "beam",
            "alpha": [[0.5, 1], [0.55, 0.25], [1, 0]],
            "sizeX": [[0, 0.25], [0.2, 3.5], [0.5, 1]],
            "baseTexture": "/pa/effects/textures/particles/flat.papa"
        },
        "offsetRangeX": [[0, 0], [0.01, 1], [0.99, 1], [1, 0]],
        "offsetRangeZ": [[0, 0], [0.01, 1], [0.99, 1], [1, 0]],
        "offsetRangeY": [[0, 0], [0.01, 0.1], [0.99, 0.1], [1, 0]],
        "velocityRangeX": [[0, 0], [0.01, 1], [0.99, 1], [1, 0]],
        "velocityRangeZ": [[0, 0], [0.01, 1], [0.99, 1], [1, 0]],
        "velocityRangeY": [[0, 0], [0.01, 0.1], [0.99, 0.1], [1, 0]],
        "velocityRange" : 1,

        "red": 0.05,
        "green": 5,
        "blue": 100,
        "sizeX": 0.1,
        "emissionBursts": 1,
        "beamSegmentLength": 1.8,
        "maxParticles" : 10,
        "lifetime": [[0, 0], [1, 0.3]],
        "emitterLifetime": 0.5,
        "bLoop": false,
        "endDistance": 1000
        }""")

    num_sparks = 4
    duration_sparks = 0.3

    for i in range(num_sparks):
        spark = copy.deepcopy(base_spark)

        spark['delay'] = i * duration_sparks / float(num_sparks)

        base_effect['emitters'].append(spark)

    return base_effect

def hit():
    base_effect = {'emitters':[]}

    base_light = loader.loads("""{
            "spec" : {
                "shape" : "pointlight",
                "red" : 0.01,
                "green" : 0.2,
                "blue" : 1,
                "alpha" : [[0.5, 0.4], [1, 0]]
            },
            "sizeX" : 15,
            "lifetime" : 0.4
        }""")

    base_dot = loader.loads("""{
            "spec" : {
                "shader": "particle_transparent",
                "red" : 0.05,
                "green" : 5,
                "blue" : 100,
                "alpha" : [[0.5, 1], [1, 0]],
                "cameraPush" : 2,
                "baseTexture": "/pa/effects/textures/particles/softdot.papa"
            },
            "sizeX" : 3,
            "lifetime" : 0.4,
            "emissionBursts" : 1,
            "bLoop" : false
        }""")

    base_sparks = loader.loads("""{
            "spec" : {
                "facing" : "velocity",
                "shader" : "particle_add",
                "red" : 0.05,
                "green" : 5.00,
                "blue" : 100,
                "baseTexture" : "/pa/effects/textures/particles/flat.papa"
            },
            "sizeX" : 0.1,
            "sizeY" : 0.5,
            "offsetRangeX" : 1,
            "offsetRangeY" : 1,
            "offsetRangeZ" : 1,
            "useRadialVelocityDir" : true,
            "velocity" : 15,
            "emissionRate" : 60,
            "emitterLifetime" : 0.3,
            "lifetime" : 0.2
        }""")

    base_effect['emitters'].append(base_light)
    base_effect['emitters'].append(base_dot)
    base_effect['emitters'].append(base_sparks)
    return base_effect


def muzzle():
    return loader.loads("""{
      "emitters":[
        {
          "spec": {
            "shader": "particle_add_soft",
            "red": 0.0,
            "green": 0.25,
            "blue": 0.7,
            "cameraPush": 0.5,
            "baseTexture": "/pa/effects/textures/particles/softdot.papa",
            "dataChannelFormat": "PositionAndColor"
          },
          "offsetY": -0.5,
          "sizeX": 6,
          "emissionBursts": 1,
          "lifetime": 0.4,
          "emitterLifetime": 0.1,
          "bLoop": false,
          "endDistance": 1400,
          "sort": "NoSort"
        },
        {
          "spec": {
            "shader": "particle_transparent",
            "facing": "AxialY",
            "red": [[0.3, 0.5], [1, 0.0]],
            "green": [[0.3, 2], [1, 0.6]],
            "blue": [[0.3, 5], [1, 1.0]],
            "alpha": [[0, 1], [1, 0]],
            "baseTexture": "/pa/effects/textures/particles/muzzle_flash_a.papa",
            "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
            "dataChannelFormat": "PositionColorAndAlignVector"
          },
          "rotationRange" : 1,
          "rotationRangeRate" : 1,
          "sizeX": 2.5,
          "sizeRangeX" : 0.2,
          "emissionBursts": 1,
          "offsetY": -1.5,
          "lifetime": 0.4,
          "emitterLifetime": 0.25,
          "bLoop": false,
          "endDistance": 1400
        },
        {
          "spec": {
            "shader": "particle_transparent",
            "facing": "EmitterY",
            "red": [[0.3, 0.5], [1, 0.0]],
            "green": [[0.3, 2], [1, 0.6]],
            "blue": [[0.3, 5], [1, 1.0]],
            "alpha": [[0, 1], [1, 0]],
            "baseTexture": "/pa/effects/textures/particles/muzzle_flash_b.papa",
            "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
            "dataChannelFormat": "PositionAndColor"
          },
          "sizeX": 2.5,
          "sizeRangeX" : 0.2,
          "emissionBursts": 1,
          "offsetY": -0.4,
          "rotationRange": 7,
          "lifetime": 0.4,
          "emitterLifetime": 0.25,
          "bLoop": false,
          "endDistance": 1400
        },
        {
          "spec": {
            "shape": "pointlight",
            "red": 0.2,
            "green": 0.3,
            "blue": 1.0,
            "alpha": [[0.6, 0.8], [1, 0]]
          },
          "offsetY": -0.5,
          "sizeX": 20,
          "emissionBursts": 1,
          "lifetime": 0.15,
          "emitterLifetime": 0.1,
          "bLoop": false,
          "endDistance": 850
        }
      ]
    }""")

def run():

    

    loader.dump_effect(trail(), "spark_trail.pfx")
    loader.dump_effect(hit(),  "spark_hit.pfx")

    loader.dump_effect(muzzle(),  "muzzle_flash.pfx")

    return loader.loads("""[
         {
           "target" : "/pa/units/land/tank_armor/tank_armor.json",
            "patch" : [
                {"op" : "replace", "path" : "/events/fired/effect_spec", "value" : "/mod/inferno/spark_muzzle_flash.pfx socket_muzzle"}
            ]
        },
        {
           "target" : "/pa/units/land/tank_armor/tank_armor_ammo.json",
            "patch" : [
                {"op" : "add", "path" : "/fx_beam_spec", "value" : "/mod/inferno/spark_trail.pfx"},
                {"op" : "add", "path" : "/fx_collision_spec", "value" : "/mod/inferno/spark_hit.pfx"}
            ]
        },
        {
            "target" : "/spark_trail.pfx",
            "destination" : "/mod/inferno/spark_trail.pfx"
        },
        {
            "target" : "/muzzle_flash.pfx",
            "destination" : "/mod/inferno/spark_muzzle_flash.pfx"
        },
        {
            "target" : "/spark_hit.pfx",
            "destination" : "/mod/inferno/spark_hit.pfx"
        }

    ]""")