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

		# TODO: Add digs objectives

		# Random check to see if it's a fake player or not
		if len(mined) < 10:
			continue

		username = get_username(uuid[:36])
		commands += str.join("\n",
		                     mined + used + crafted + broken + picked_up + dropped + killed + killed_by + custom).replace(
			"%s", username) + "\n"

		# Prints
		sys.stdout.write(
			"\r" + "Updating " + username + "'s scores...\n\r" + str(done) + "/" + str(len(files)) + " done")
		sys.stdout.flush()

	# TODO: Split into multiple files if number of lines > 65536

	update_mcfunction = open(
		"./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/update.mcfunction",
		"w+")
	update_mcfunction.write(commands)
	update_mcfunction.close()


def stats_to_commands(stats, prefix, dictionary):
	commands = []
	for i in stats:
		try:
			commands.append("scoreboard players set %s " + dictionary[prefix + i[10:]] + " " + str(stats[i]))
		except:
			()

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
