description = """
Converts statistics to objective values.
by samipourquoi
"""

pack = """{
    "pack": {
        "description": "Every scoreboard, for Minecraft %s!",
        "pack_format": 5
    }
}
"""

tag_text = """{
	"values": [
		%s
	]
}"""

import argparse
import requests
import json
import os
import sys
import time

# Arguments
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-S", "--statslocation", help="set the path from where the program will get the statistics")
parser.add_argument("-D", "--dictionary", help="set the path from where the program will get the objectives dictionary")
parser.add_argument("-d", "--dig", required=False, help="(optional) set the name of the total dig objective")
parser.add_argument("-p", "--picks", required=False, help="(optional) set the name of the total pick uses objective")
parser.add_argument("-s", "--shovels", required=False,
                    help="(optional) set the name of the total shovel uses objective")
parser.add_argument("-a", "--axes", required=False, help="(optional) set the name of the axe uses objective")
args = parser.parse_args()


def main():
	minecraft_version = args.dictionary.split("/")[-1][11:-5]

	# Create required files/folders
	os.makedirs("./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/",
	            exist_ok=True)
	os.makedirs("./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/tags/functions",
	            exist_ok=True)
	# Creates the pack.mcmeta file
	pack_mcmeta = open("./datapacks/every-scoreboard-" + minecraft_version + "/pack.mcmeta", "w+")
	pack_mcmeta.write(pack % minecraft_version)
	pack_mcmeta.close()

	# Reads dictionary
	dictionary_file = open(args.dictionary, "r")
	dictionary = json.load(dictionary_file)
	dictionary_file.close()

	location = args.statslocation
	files = os.listdir(location)

	done = 0
	commands = ""
	for uuid in files:
		done += 1

		# If ever there is a random OS file
		if uuid[36:] != ".json":
			continue

		file = open(location + "/" + uuid, "r")
		stats = json.load(file)["stats"]
		file.close()

		mined = stats_to_commands(stats["minecraft:mined"] if "minecraft:mined" in stats else {}, "m-", dictionary)
		used = stats_to_commands(stats["minecraft:used"] if "minecraft:used" in stats else {}, "u-", dictionary)
		crafted = stats_to_commands(stats["minecraft:crafted"] if "minecraft:crafted" in stats else {}, "c-",
		                            dictionary)
		broken = stats_to_commands(stats["minecraft:broken"] if "minecraft:broken" in stats else {}, "b-", dictionary)
		picked_up = stats_to_commands(stats["minecraft:picked_up"] if "minecraft:picked_up" in stats else {}, "p-",
		                              dictionary)
		dropped = stats_to_commands(stats["minecraft:dropped"] if "minecraft:dropped" in stats else {}, "d-",
		                            dictionary)
		killed = stats_to_commands(stats["minecraft:killed"] if "minecraft:killed" in stats else {}, "k-", dictionary)
		killed_by = stats_to_commands(stats["minecraft:killed_by"] if "minecraft:killed_by" in stats else {}, "kb-",
		                              dictionary)
		custom = stats_to_commands(stats["minecraft:custom"] if "minecraft:custom" in stats else {}, "z-", dictionary)

		# Random check to see if it's a fake player or not
		if len(mined) < 10:
			continue

		username = get_username(uuid[:36])
		commands += str.join("\n",mined + used + crafted + broken + picked_up + dropped + killed + killed_by + custom).replace("%s", username) + "\n"

		# Prints
		sys.stdout.write(
			"\r" + "Updating " + username + "'s scores...\n\r" + str(done) + "/" + str(len(files)) + " done")
		sys.stdout.flush()

	# It's messy code but it works ig
	i = 0
	commands = commands.split("\n")
	function_names = []
	has_ran_once = True
	max_length = 10000 #65536
	while has_ran_once or len(commands) > 0:
		update_mcfunction = open(
			"./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/update" + str(i) + ".mcfunction",
			"w+")
		update_mcfunction.write(str.join("\n", commands[:max_length]))
		update_mcfunction.close()
		function_names.append("\"every-scoreboard:update" + str(i) + "\"")
		i += 1
		commands = commands[max_length:]

		if has_ran_once:
			has_ran_once = False

	# Creates the tag to run all of these function files
	tag = open(
			"./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/tags/functions/update.json",
			"w+")
	tag.write(tag_text % str.join(",\n\t\t", function_names))
	tag.close()




def stats_to_commands(stats, prefix, dictionary):
	commands = []
	dig = 0
	picks = 0
	shovels = 0
	axes = 0
	for i in stats:
		try:
			# Custom dig scoreboards
			if prefix == "m-":
				dig += stats[i]
			if prefix == "u-":
				if "pickaxe" in i[10:]:
					picks += stats[i]
				if "shovel" in i[10:]:
					shovels += stats[i]
				if "_axe" in i[10:]:
					axes += stats[i]

			commands.append("scoreboard players set %s " + dictionary[prefix + i[10:]] + " " + str(stats[i]))
		except:
			()

	# Custom dig scoreboards
	if prefix == "m-" and args.dig != None:
		commands.append("scoreboard players set %s " + args.dig + " " + str(dig))
	if prefix == "u-" and args.picks != None:
		commands.append("scoreboard players set %s " + args.picks + " " + str(picks))
	if prefix == "u-" and args.shovels != None:
		commands.append("scoreboard players set %s " + args.shovels + " " + str(shovels))
	if prefix == "u-" and args.axes != None:
		commands.append("scoreboard players set %s " + args.axes + " " + str(axes))

	return commands


def get_username(uuid):
	# Removes the '-'
	uuid = uuid.replace("-", "")
	# Requests to mojang api
	body = json.loads(requests.get("https://api.mojang.com/user/profiles/" + uuid + "/names").text)
	# Gets the current username
	try:
		username = body[-1]["name"]
		return username
	except:
		time.sleep(10)
		return get_username(uuid)


if __name__ == "__main__":
	main()
