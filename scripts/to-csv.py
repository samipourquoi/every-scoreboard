description = """
Converts statistics to objective values, and puts them in a .csv file.
by samipourquoi
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
parser.add_argument("-d", "--dig", required=False, help="(optional) set the name of the total dig objective")
parser.add_argument("-p", "--picks", required=False, help="(optional) set the name of the total pick uses objective")
parser.add_argument("-s", "--shovels", required=False,
                    help="(optional) set the name of the total shovel uses objective")
parser.add_argument("-a", "--axes", required=False, help="(optional) set the name of the axe uses objective")
args = parser.parse_args()


def main():
	os.makedirs("csv", exist_ok=True)

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
		try:
			stats = json.load(file)["stats"]
		except:
			continue

		file.close()

		mined = stats_to_commands(stats["minecraft:mined"] if "minecraft:mined" in stats else {}, "m-")
		used = stats_to_commands(stats["minecraft:used"] if "minecraft:used" in stats else {}, "u-")
		crafted = stats_to_commands(stats["minecraft:crafted"] if "minecraft:crafted" in stats else {}, "c-")
		broken = stats_to_commands(stats["minecraft:broken"] if "minecraft:broken" in stats else {}, "b-")
		picked_up = stats_to_commands(stats["minecraft:picked_up"] if "minecraft:picked_up" in stats else {}, "p-")
		dropped = stats_to_commands(stats["minecraft:dropped"] if "minecraft:dropped" in stats else {}, "d-")
		killed = stats_to_commands(stats["minecraft:killed"] if "minecraft:killed" in stats else {}, "k-")
		killed_by = stats_to_commands(stats["minecraft:killed_by"] if "minecraft:killed_by" in stats else {}, "kb-")
		custom = stats_to_commands(stats["minecraft:custom"] if "minecraft:custom" in stats else {}, "z-")

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
	commands = commands.split("\n")
	csv_file = open("csv/out.csv", "w+")
	csv_file.write(str.join("\n", commands))
	csv_file.close()


def stats_to_commands(stats, prefix):
	lines = []
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

			lines.append("%s," + str(stats[i]) + "," + prefix + i[10:])
		except:
			pass

	# Custom dig scoreboards
	if prefix == "m-" and args.dig != None:
		lines.append("%s," + str(dig) + "," + args.dig)
	if prefix == "u-" and args.picks != None:
		lines.append("%s," + str(picks) + "," + args.picks)
	if prefix == "u-" and args.shovels != None:
		lines.append("%s," + str(shovels) + "," + args.shovels)
	if prefix == "u-" and args.axes != None:
		lines.append("%s," + str(axes) + "," + args.axes)

	return lines


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
