import loader
import pajson
import utils
import os
import copy

PA_MEDIA_DIR = utils.pa_media_dir()

base_dot = pajson.loadf('dots/dot.json')

dot_small = copy.deepcopy(base_dot)
dot_small['sizeX'] = 1

dot_medium = copy.deepcopy(base_dot)
dot_medium['sizeX'] = 2

dot_large = copy.deepcopy(base_dot)
dot_large['sizeX'] = 3

dot_huge = copy.deepcopy(base_dot)
dot_huge['sizeX'] = 4

dots = {
	"small" : dot_small,
	"medium" : dot_medium,
	"large" : dot_large,
	"huge" : dot_huge
}
# get all the units
#  - get each weapon on the unit
#  - get each ammo type
#  		- use damage to decide dot size
#         (small, medium, large)

def _get_source_file_path(target, dirs):
    if target[0] == "/":
        target = target[1:]

    for d in dirs:
        path = os.path.join(d, target)
        if os.path.isfile(path):
            return path

    return None

_cache = {}
def load(path):
	path = _get_source_file_path(path, ["..", PA_MEDIA_DIR])

	if path not in _cache:
		_cache[path] = pajson.loadf(path)
	return _cache[path]


def parseSpec(spec_id):
	base_spec = {}

	spec = load(spec_id)

	if 'base_spec' in spec:
		base_spec = parseSpec(spec['base_spec'])

	base_spec.update(spec)
	return base_spec

unit_list = load('/pa/units/unit_list.json')

# going to store the effect file patches here
patches = []

visited_fx_files = {}


_checked_ammo_ids = {}
for unit_file in unit_list['units']:
	# get unit data
	unit = parseSpec(unit_file)

	printing_on = False

	# iterate over unit weapons
	for tool_obj in unit.get('tools', []):
		tool = parseSpec(tool_obj['spec_id'])

		# ignore tools which are not weapons
		if tool.get('tool_type', 'TOOL_BuildArm') == 'TOOL_BuildArm':
			continue

		# we might get an actual ammo_id here or an array of them
		ammo_id = tool.get('ammo_id', None)

		if ammo_id:
			# if we have a list, map to the ammo_id values
			if isinstance(ammo_id, list):
				ammo_ids = map(lambda item: item['id'], ammo_id)
			else:
				ammo_ids = [ammo_id]
			for aid in ammo_ids:
				# doing ammo id caching
				if aid in _checked_ammo_ids: continue
				_checked_ammo_ids[aid] = True

				ammo = parseSpec(aid)

				# must be ammo_projectile type, or its the uber cannon projectile
				if ammo['ammo_type'] == 'AMMO_Projectile' or (ammo['ammo_type'] == 'Projectile' and 'uber' in aid):
					fx_id = ammo['fx_trail']['filename']

					if printing_on:
						print(aid + ' projectile')

					if ammo['damage'] <= 24:
						size = "small"
					elif ammo['damage'] <= 200:
						size = "medium" 
					elif ammo['damage'] <= 400:
						size = "large"
					else:
						size = "huge"

					fx_name = fx_id + '-' + size + ".pfx"

					# print (fx_name)

					# make sure we only generate the effect once
					if fx_name not in visited_fx_files:
						visited_fx_files[fx_name] = True
						patches.append({
							"target" : fx_id,
							"destination" : fx_name,
							"patch" : [
								{"op" : "add", "path" : "/emitters/-", "value": dots[size]}
							]
						})

					# get the ammo again, but this time only the top level
					# (we don't want inherited values for computed the patch at this level)
					ammo = load(aid)
					print (aid)

					if 'fx_trail' not in ammo:
						patches.append({
							"target": aid,
							"patch" : [
								{"op": "add", "path": "/fx_trail", "value": {
									"filename" : fx_name
								}}
							]
						})
					else:
						patches.append({
							"target": aid,
							"patch" : [
								{"op": "replace", "path": "/fx_trail/filename", "value": fx_name}
							]
						})


def run():
	return patches
