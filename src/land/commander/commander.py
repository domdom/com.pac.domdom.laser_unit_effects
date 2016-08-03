import copy
import math

import loader

def _round_time_curve(curve, digits=3):
    return [[round(x, digits), round(y, digits)] for [x,y] in curve]

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


def bullet_trail():
    base_effect = loader.loads("""{
            "emitters" : [
                {
                    "spec" : {
                        "shader" : "particle_add",
                        "red" : 0.05,
                        "green" : 7,
                        "blue" : 0.1,
                        "alpha" : 10,
                        "baseTexture" : "/pa/effects/textures/particles/dot.papa"
                    },
                    "sizeX" : 1,
                    "emissionBursts" : 1
                }
            ]
        }""")

    base_string = loader.loads("""{
        "spec" : {
            "shader" : "particle_transparent",
            "shape" : "string",
            "red" : 0.05,
            "green" : 7,
            "blue" : 0.1,
            "size" : [[0, 1], [0.1, 0.05], [0.5, 0]],
            "alpha" : 1,
            "baseTexture" : "/pa/effects/textures/particles/flat.papa"
        },
        "lifetime" : 0.6,
        "sizeX" : 1,
        "emissionRate" : 60,
        "useWorldSpace" : true,
        "bLoop" : true
    }""")

    sparks = 6
    sparks_amp = 1

    for i in range(sparks):
        string = copy.deepcopy(base_string)

        string['spec']['size'] = [[0, 1], [0.5, 0]]
        string['spec']['blue'] = 2
        string['spec']['green'] = 0.1

        string['sizeX'] = 0.25
        string['lifetime'] = 0.3

        string['offsetRangeX'] = sparks_amp
        string['offsetRangeZ'] = sparks_amp

        base_effect['emitters'].append(string)



    base_effect['emitters'].append(base_string)

    base_effect['emitters'].append(loader.loads("""{
            "spec" : {
                "shape" : "pointlight",
                "red" : 0.1,
                "green" : 1,
                "blue" : 0.2,
                "alpha" : 0.05
            },
            "sizeX" : 20,
            "lifetime" : 10,
            "killOnDeactivate" : true
        }
        """))

    base_effect['emitters'].append(loader.loads("""{
          "spec": {
            "shape": "pointlight",
            "red": 0,
            "green": [[0, 2.1], [0.2, 0.1], [0.4, 2]],
            "blue": [[0.2, 2.2], [0.4, 0]],
            "alpha": [[0.2, 0.06], [1, 0]],
            "size": [[0.2, 1], [1, 0.3]]
          },
          "offsetY": 0,
          "sizeX": 25,
          "emissionRate": 40,
          "lifetime": 0.35,
          "bLoop": true,
          "useWorldSpace" : true,
          "endDistance": 850
        }"""))

    return base_effect



def laser_trail():
    base_effect = loader.loads("""{
        "emitters" : [
            {
                "spec" : {
                    "shader" : "particle_add",
                    "red" : 0.05,
                    "green" : 7,
                    "blue" : 0.1,
                    "alpha" : 10,
                    "baseTexture" : "/pa/effects/textures/particles/dot.papa"
                },
                "sizeX" : 0.5,
                "emissionBursts" : 1
            },
            {
                "spec" : {
                    "shader" : "particle_transparent",
                    "shape" : "string",
                    "red" : 0.05,
                    "green" : 7,
                    "blue" : 0.1,
                    "size" : [[0, 1], [0.5, 0]],
                    "alpha" : 1,
                    "baseTexture" : "/pa/effects/textures/particles/flat.papa"
                },
                "lifetime" : 0.5,
                "sizeX" : 0.4,
                "emissionRate" : 60,
                "useWorldSpace" : true,
                "bLoop" : true
            }
        ]
    }""")
    
    ring_amp = 0.4
    ring_life = 2
    ring_revs = 14
    ring_dt = ring_life / 240

    rings = 3

    for i in range(rings):
        string = copy.deepcopy(base_effect['emitters'][1])

        string['emissionRate'] = 240
        string['emitterLifetime'] = ring_life
        string['lifetime'] = 0.3

        string['sizeX'] = 0.4
        string['spec']['red'] = 3
        string['spec']['green'] = 7
        string['spec']['blue'] = 0
        string['offsetX'] = _round_time_curve(wave_to_offset([[ring_amp, ring_revs, 2 * math.pi / rings * i]],                  ring_life, ring_dt))
        string['offsetZ'] = _round_time_curve(wave_to_offset([[ring_amp, ring_revs, 2 * math.pi / rings * i + math.pi / 2]],    ring_life, ring_dt))

        string['velocityX'] = _round_time_curve(wave_to_offset([[ring_amp, ring_revs, 2 * math.pi / rings * i]],                  ring_life, ring_dt))
        string['velocityZ'] = _round_time_curve(wave_to_offset([[ring_amp, ring_revs, 2 * math.pi / rings * i + math.pi / 2]],    ring_life, ring_dt))
        string['velocity'] = 3
        string['drag'] = 0.98

        base_effect['emitters'].append(string)

        # string['velocityX'] = _round_time_curve(wave_to_offset([[ring_amp, 1, 2 * math.pi / 3 * i]], wave_life, wave_ds))
        # string['velocityZ'] = _round_time_curve(wave_to_offset([[ring_amp, 1, 2 * math.pi / 3 * i]], wave_life, wave_ds))

    base_effect['emitters'].append(loader.loads("""{
            "spec" : {
                "shape" : "pointlight",
                "red" : 0.1,
                "green" : 1,
                "blue" : 0.2,
                "alpha" : 0.05
            },
            "sizeX" : 20,
            "lifetime" : 10,
            "killOnDeactivate" : true
        }
        """))

    base_effect['emitters'].append(loader.loads("""{
          "spec": {
            "shape": "pointlight",
            "red": [[0, 1], [1, 0]],
            "green": 5,
            "blue": 0.05,
            "alpha": [[0, 0.04], [1, 0]],
            "size": [[0.2, 1], [1, 0.3]]
          },
          "offsetY": 0,
          "sizeX": 25,
          "emissionRate": 30,
          "lifetime": 0.35,
          "bLoop": true,
          "useWorldSpace" : true,
          "endDistance": 850
        }"""))


    return base_effect   



def rocket_trail():
    base_effect = loader.loads("""{
            "emitters" : [
                {
                    "spec" : {
                        "shader" : "particle_transparent",
                        "shape" : "string",
                        "red" : 0.05,
                        "green" : 7,
                        "blue" : 0.1,
                        "size" : [[0, 0], [0.1, 1], [1, 0]],
                        "alpha" : [[0, 0.8], [1, 0]],
                        "baseTexture" : "/pa/effects/textures/particles/flat.papa"
                    },
                    "lifetime" : 0.25,
                    "sizeX" : 1,
                    "sizeRangeX" : 0.5,
                    "emissionRate" : 60,
                    "useWorldSpace" : true,
                    "bLoop" : true
                },
                {
                    "spec" : {
                        "shader" : "particle_add_ramp",
                        "red" : [[0, 0], [2, 1.0]],
                        "green" : 0.2,
                        "blue" : 5,
                        "alpha" : [[0, 6], [1, 0]],
                        "baseTexture" : "/pa/effects/textures/particles/flat.papa",
                        "rampTexture" : "/pa/effects/textures/particles/uncompressed/flicker_ramp.papa"
                    },
                    "rotationRange" : 6.28,
                    "velocityY" : 1,
                    "velocityRangeX" : 0.5,
                    "velocityRangeZ" : 0.5,
                    "velocityRange" : 20,
                    "velocity" : 8,
                    "drag" : 0.97,
                    "gravity" : -9.8,
                    "sizeX" : 0.2,
                    "sizeY" : 0.9,
                    "sizeRangeY" : 0.3,
                    "sizeRangeX" : 0.1,
                    "lifetime" : 0.25,
                    "lifetimeRange" : 0.15,
                    "emissionRate" : 200,
                    "offsetRangeX" : 0.5,
                    "offsetRangeZ" : 0.5,
                    "useWorldSpace" : true,
                    "emitterLifetime" : 1,
                    "bLoop" : true
                }
            ]
        }""")

    base_effect['emitters'].append(loader.loads("""{
            "spec" : {
                "shape" : "pointlight",
                "red" : 0.1,
                "green" : 1,
                "blue" : 0.5,
                "alpha" : 0.05
            },
            "sizeX" : 20,
            "lifetime" : 10,
            "killOnDeactivate" : true
        }
        """))

    base_effect['emitters'].append(loader.loads("""{
          "spec": {
            "shape": "pointlight",
            "red": 0.05,
            "green": 3,
            "blue": 0.5,
            "alpha": [[0, 0.04], [1, 0]],
            "size": [[0.2, 1], [1, 0.3]]
          },
          "offsetY": 0,
          "sizeX": 25,
          "emissionRate": 40,
          "lifetime": 0.35,
          "bLoop": true,
          "useWorldSpace" : true,
          "endDistance": 850
        }"""))

    return base_effect

def run():

    bullet = bullet_trail()
    laser = laser_trail()
    rocket = rocket_trail()

    loader.dump_effect(bullet, "bullet_trail.pfx")
    loader.dump_effect(laser,  "laser_trail.pfx")
    loader.dump_effect(rocket, "rocket_trail.pfx")

    return loader.loads("""[
        {
           "target" : "/pa/units/commanders/base_commander/base_commander.json",
            "patch" : [
                {"op" : "add", "path" : "/events/fired", "value" : {"effect_spec" : "/mod/com.pa.domdom.laser_unit_effects/commander/commander_muzzle_flash.pfx socket_rightMuzzle"}}
            ]
        },
        {
            "target": "/pa/effects/specs/tank_muzzle_flash.pfx",
            "destination": "/mod/com.pa.domdom.laser_unit_effects/commander/commander_muzzle_flash.pfx",
            "patch": [
                {"op": "replace", "path": "/emitters/0/spec/red", "value": 0.0 },
                {"op": "replace", "path": "/emitters/0/spec/green", "value": 0.7 },
                {"op": "replace", "path": "/emitters/0/spec/blue", "value": 0.3 },
                {"op": "replace", "path": "/emitters/1/spec/red", "value":   [[0.3, 0.5 ], [1, 0.0 ] ] },
                {"op": "replace", "path": "/emitters/1/spec/green", "value": [[0.3, 5 ], [1, 1.00 ] ] },
                {"op": "replace", "path": "/emitters/1/spec/blue", "value":  [[0.3, 2 ], [1, 0.60 ] ] },

                {"op": "copy", "path": "/emitters/2/spec/red", "from": "/emitters/1/spec/red"},
                {"op": "copy", "path": "/emitters/2/spec/green", "from": "/emitters/1/spec/green"},
                {"op": "copy", "path": "/emitters/2/spec/blue", "from": "/emitters/1/spec/blue"},
                {"op": "copy", "path": "/emitters/3/spec/red", "from": "/emitters/0/spec/red"},
                {"op": "copy", "path": "/emitters/3/spec/green", "from": "/emitters/0/spec/green"},
                {"op": "copy", "path": "/emitters/3/spec/blue", "from": "/emitters/0/spec/blue"},
                {"op": "add", "path": "/emitters/-", "value": {
                    "spec": {
                        "shape": "pointlight",
                        "red": 0.2,
                        "green": 1.0,
                        "blue": 0.3,
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
              }
            ]
        },
        {
            "target" : "/pa/units/commanders/base_commander/base_commander_ammo_bullet.json",
            "patch" : [
                {"op" : "add", "path" : "/fx_trail", "value" : {"filename" : "/mod/com.pa.domdom.laser_unit_effects/commander/bullet_trail.pfx"}},
                {"op" : "add", "path" : "/events/died", "value" : {}},
                {"op" : "add", "path" : "/events/died/effect_spec", "value" : "/mod/com.pa.domdom.laser_unit_effects/commander/proj_hit.pfx"},
                {"op" : "add", "path" : "/events/died/effect_scale", "value" : 0.15}
            ]
        },
        {
            "target" : "/pa/units/commanders/base_commander/base_commander_ammo_laser.json",
            "patch" : [
                {"op" : "add", "path" : "/fx_trail", "value" : {"filename" : "/mod/com.pa.domdom.laser_unit_effects/commander/laser_trail.pfx"}},
                {"op" : "add", "path" : "/events/died/effect_spec", "value" : "/mod/com.pa.domdom.laser_unit_effects/commander/proj_hit.pfx"},
                {"op" : "add", "path" : "/events/died/effect_scale", "value" : 0.15}
            ]
        },
        {
            "target" : "/pa/units/commanders/base_commander/base_commander_ammo_missile.json",
            "patch" : [
                {"op" : "add", "path" : "/fx_trail", "value" : {
                    "filename" : "/mod/com.pa.domdom.laser_unit_effects/commander/rocket_trail.pfx",
                    "offset": [0.0, 0.9, 0.0]
                }},
                {"op" : "add", "path" : "/events/died/effect_spec", "value" : "/mod/com.pa.domdom.laser_unit_effects/commander/proj_hit.pfx"},
                {"op" : "add", "path" : "/events/died/effect_scale", "value" : 0.15}
            ]
        },
        {
            "target" : "bullet_trail.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/commander/bullet_trail.pfx"
        },
        {
            "target" : "laser_trail.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/commander/laser_trail.pfx"
        },
        {
            "target" : "rocket_trail.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/commander/rocket_trail.pfx"
        },
        {
            "target" : "/base_arty/base_ammo_hit.pfx",
            "destination" : "/mod/com.pa.domdom.laser_unit_effects/commander/proj_hit.pfx",
            "patch" : [
              {"op" : "replace", "path" : "/emitters/0/spec/red",     "value" : [[0, 0 ], [0.35, 2 ]]},
              {"op" : "replace", "path" : "/emitters/0/spec/green",   "value" : [[0, 100 ], [0.35, 20 ]]},
              {"op" : "replace", "path" : "/emitters/0/spec/blue",    "value" : [[0, 0 ], [0.35, 1]]},

              {"op" : "replace", "path" : "/emitters/1/spec/red",     "value" : [[0, 0 ], [0.35, 2 ]]},
              {"op" : "replace", "path" : "/emitters/1/spec/green",   "value" : [[0, 100 ], [0.35, 20 ]]},
              {"op" : "replace", "path" : "/emitters/1/spec/blue",    "value" : [[0, 1 ], [0.35, 4]]},

              {"op" : "replace", "path" : "/emitters/5/spec/red",     "value" : [[0, 10 ], [0.75, 1 ]]},
              {"op" : "replace", "path" : "/emitters/5/spec/green",   "value" : [[0, 10 ], [0.75, 10 ]]},
              {"op" : "replace", "path" : "/emitters/5/spec/blue",    "value" : [[0, 0 ],  [0.75, 0]]},

              {"op" : "replace", "path" : "/emitters/4/spec/red",     "value" : [[0, 3 ], [0.75, 1 ]]},
              {"op" : "replace", "path" : "/emitters/4/spec/green",   "value" : [[0, 15 ], [0.75, 15 ]]},
              {"op" : "replace", "path" : "/emitters/4/spec/blue",    "value" : [[0, 20 ], [0.75, 5]]},

              {"op" : "replace", "path" : "/emitters/2/spec/red",   "value" : 0.9},
              {"op" : "replace", "path" : "/emitters/2/spec/green", "value" : 6.0},
              {"op" : "replace", "path" : "/emitters/2/spec/blue",  "value" : 0.4},

              {"op" : "replace", "path" : "/emitters/3/spec/red",   "value" : 0.9},
              {"op" : "replace", "path" : "/emitters/3/spec/green", "value" : 6.0},
              {"op" : "replace", "path" : "/emitters/3/spec/blue",  "value" : 0.7}
            ]
        }
    ]""")