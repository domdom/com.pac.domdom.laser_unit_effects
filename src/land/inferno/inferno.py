import copy
import math

import loader

def muzzle_sparks_patch():
    base_spark_patch = loader.loads("""
        {"op" : "add", "path" : "/emitters/-", "value" : {
            "spec" : {
                "shader": "particle_transparent",
                "shape": "beam",
                "alpha": [[0.5, 1], [0.55, 0.25], [1, 0]],
                "sizeX": [[0, 0.25], [0.2, 3.5], [0.5, 1]],
                "baseTexture": "/pa/effects/textures/particles/flat.papa"
            },
            "useWorldSpace" : true,
            "offsetRangeX": [[0, 0], [0.01, 1], [1, 3]],
            "offsetRangeZ": [[0, 0], [0.01, 1], [1, 3]],
            "offsetRangeY": [[0, 0], [0.01, 1], [1, 3]],
            "velocityRangeX": [[0, 0], [0.01, 1], [0.7, 1], [1, 2]],
            "velocityRangeZ": [[0, 0], [0.01, 1], [0.7, 1], [1, 2]],
            "velocityRangeY": [[0, 0], [0.01, 0.1], [0.7, 0.1], [1, 0]],
            "velocityRange" : 1,
            "offsetY" : [[0, 0], [1, -15]],
            "red": 0.05,
            "green": 5,
            "blue": 100,
            "sizeX": [[0, 0.08], [0.5, 0.1], [1, 0]],
            "sizeRangeX" : 0.08,
            "emissionBursts": 1,
            "maxParticles" : 10,
            "lifetime": [[0, 0], [1, 0.25]],
            "emitterLifetime": 0.5,
            "bLoop": false,
            "endDistance": 1000
        }}
    """)
    base_extra_flames_patch = loader.loads("""
       { "op" : "add", "path" : "/emitters/-", "value" : {
            "spec": {
                "shader": "particle_transparent",
                "facing": "velocity",
                "size": [[0, 0.5], [0.5, 1.25], [1, 0]],
                "red": [[0, 2.0], [0.2, 2.0], [0.65, 1.5]],
                "green": [[0, 2.0], [0.2, 0.6], [0.65, 0.05]],
                "blue": [[0, 2.0], [0.2, 0.2], [0.65, 0.01]],
                "alpha" : [[0, 0.7], [1, 0]],
                "baseTexture": "/pa/effects/textures/particles/simpleSmokeSingle.papa",
                "dataChannelFormat": "PositionColorAndAlignVector"
            },
            "useWorldSpace" : true,
            "velocityY": -1,
            "velocityRangeX": 0.1,
            "velocityRangeZ": 0.1,
            "velocity": 90.0,
            "velocityRange": 20.0,
            "drag": 0.92,
            "gravity": 25,
            "sizeX": 2,
            "sizeY": 3.5,
            "sizeRangeY": 1.5,
            "emissionBursts": 1,
            "emissionRate": 60,
            "lifetime": 0.5,
            "emitterLifetime": 0.3,
            "useWorldSpace": true,
            "endDistance": 1600,
            "bLoop": false
          }}
      """)

    base_glitter = loader.loads("""{ "op" : "add", "path" : "/emitters/-", "value" : {
            "spec" : {
                "facing" : "velocity",
                "shader" : "particle_add",
                "red" : 0.05,
                "green" : 5.00,
                "blue" : 100,
                "baseTexture" : "/pa/effects/textures/particles/flat.papa"
            },
            "useWorldSpace" : true,
            "type" : "EMITTER",
            "linkIndex" : 5,
            "sizeX" : 0.1,
            "sizeY" : 0.5,
            "offsetRangeX" : 1,
            "offsetRangeY" : 1,
            "offsetRangeZ" : 1,
            "velocityRangeX" : 1,
            "velocityRangeY" : 1,
            "velocityRangeZ" : 1,
            "useRadialVelocityDir" : false,
            "velocity" : 10,
            "velocityRange" : 5,
            "emissionRate" : 9,
            "emitterLifetime" : 0.3,
            "lifetime" : 0.2
        }}""")

    patch = [base_extra_flames_patch, base_glitter]


    num_sparks = 4
    duration_sparks = 0.3

    for i in range(num_sparks):
        spark = copy.deepcopy(base_spark_patch)

        spark['value']['delay'] = i * duration_sparks / float(num_sparks)

        patch.append(spark)

    patch.append(loader.loads("""{ "op" : "replace", "path" : "/emitters/0/spec/alpha/keys/1/1", "value" : 1}"""))



    return patch
         
def run():
    muzzle_patch = loader.dumps(muzzle_sparks_patch())

    return loader.loads("""[
        {
           "target" : "/pa/units/land/tank_armor/tank_armor.json",
            "patch" : [
                {"op" : "replace", "path" : "/events/fired/effect_spec", "value" : "/mod/com.pa.domdom.laser_unit_effects/inferno/spark_muzzle_flash.pfx socket_muzzle"}
            ]
        },        
        {
            "target" : "/pa/units/land/tank_armor/tank_armor_muzzle_flame.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/inferno/spark_muzzle_flash.pfx",
            "patch" : """ + muzzle_patch + """
        },
        {
            "target" : "/blueflamethrower.papa",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/blueflamethrower.papa"
        },
        {
            "target" : "/pa/units/land/tank_armor/tank_armor_muzzle_flame.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/inferno/spark_muzzle_flash.pfx",
            "patch" : [
                {"op" : "move", "path" : "/emitters/0/spec/_blue", "from" : "/emitters/0/spec/red"},
                {"op" : "move", "path" : "/emitters/0/spec/red", "from" : "/emitters/0/spec/blue"},
                {"op" : "move", "path" : "/emitters/0/spec/blue", "from" : "/emitters/0/spec/_blue"},

                {"op" : "move", "path" : "/emitters/1/spec/_blue", "from" : "/emitters/1/spec/red"},
                {"op" : "move", "path" : "/emitters/1/spec/red", "from" : "/emitters/1/spec/blue"},
                {"op" : "move", "path" : "/emitters/1/spec/blue", "from" : "/emitters/1/spec/_blue"},

                {"op" : "move", "path" : "/emitters/2/spec/_blue", "from" : "/emitters/2/spec/red"},
                {"op" : "move", "path" : "/emitters/2/spec/red", "from" : "/emitters/2/spec/blue"},
                {"op" : "move", "path" : "/emitters/2/spec/blue", "from" : "/emitters/2/spec/_blue"},

                {"op" : "move", "path" : "/emitters/3/spec/_blue", "from" : "/emitters/3/spec/red"},
                {"op" : "move", "path" : "/emitters/3/spec/red", "from" : "/emitters/3/spec/blue"},
                {"op" : "move", "path" : "/emitters/3/spec/blue", "from" : "/emitters/3/spec/_blue"},

                {"op" : "replace", "path" : "/emitters/1/spec/baseTexture", "value" : "/mod/com.pa.domdom.laser_unit_effects/blueflamethrower.papa"}
            ]
        }
    ]""")