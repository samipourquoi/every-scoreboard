description = """
Creates a datapack which will add every scoreboard in the game.
By samipourquoi
"""

pack = """{
    "pack": {
        "description": "Every scoreboard, for Minecraft %s!",
        "pack_format": 5
    }
}
"""

import argparse
import minecraft_data
import json
import os

# Arguments
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-mc", "--mcversion", help="set the Minecraft version the scoreboards will be for")
args = parser.parse_args()


def main():
    minecraft_version = args.mcversion
    # noinspection PyCallingNonCallable
    data = minecraft_data(minecraft_version)

    # Creates the objective names from the registries
    mined = make(data.blocks, "m", "minecraft.mined", "%s Mined")
    used = make(data.items, "u", "minecraft.used", "%s Used")
    broken = make(data.items, "b", "minecraft.broken", "%s Broken")
    dropped = make(data.items, "d", "minecraft.dropped", "%s Dropped")
    picked_up = make(data.items, "p", "minecraft.picked_up", "%s Picked up")
    killed = make(data.mobs, "k", "minecraft.killed", "%s Killed")
    killed_by = make(data.mobs, "kb", "minecraft.killed_by", "Killed by %s")

    # Creates the required folders
    os.makedirs("./dictionary/", exist_ok=True)
    os.makedirs("./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/", exist_ok=True)

    # Creates the pack.mcmeta file
    pack_mcmeta = open("./datapacks/every-scoreboard-" + minecraft_version + "/pack.mcmeta", "w+")
    pack_mcmeta.write(pack % minecraft_version)
    pack_mcmeta.close()

    # Creates the json file
    dictionary = open("./dictionary/dictionnary-" + minecraft_version + ".json", "w+")
    dictionary.write(json.dumps(mined["dictionary"]))
    dictionary.close()

    # Creates the commands, which will register the objectives
    fin_create_commands = create_commands(mined) + create_commands(used) + create_commands(broken) + create_commands(dropped) + create_commands(picked_up) + create_commands(killed) + create_commands(killed_by)
    fin_delete_commands = delete_commands(mined) + delete_commands(used) + delete_commands(broken) + delete_commands(dropped) + delete_commands(picked_up) + delete_commands(killed) + delete_commands(killed_by)

    # Writes to a file
    create_mcfunction = open(
        "./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/create.mcfunction",
        "w+")
    create_mcfunction.write("\n".join(fin_create_commands))
    create_mcfunction.close()

    # Writes the remove commands
    delete_mcfunction = open(
        "./datapacks/every-scoreboard-" + minecraft_version + "/data/every-scoreboard/functions/delete.mcfunction",
        "w+")
    delete_mcfunction.write("\n".join(fin_delete_commands))
    delete_mcfunction.close()


def make(registry, prefix, criterion_namespace, lang):
    dictionary = {}
    criteria = {}
    display_names = {}
    for i in registry:
        full_name = prefix + "-" + registry[i]["name"]
        truncated_name = full_name
        if len(full_name) > 16:
            index = "+" + gen_id(full_name)
            truncated_name = full_name[:16-len(index)] + index

        dictionary[full_name] = truncated_name
        criteria[full_name] = criterion_namespace + ":" + "minecraft." + registry[i]["name"]
        display_names[full_name] = lang % registry[i]["displayName"]

    return {
        "dictionary": dictionary,
        "criteria": criteria,
        "display_names": display_names
    }


def create_commands(data):
    commands = []
    for i in data["dictionary"]:
        commands.append("scoreboard objectives add " +
                        data["dictionary"][i] + " " +
                        data["criteria"][i] + " " +
                        "\"" +  data["display_names"][i] + "\"")

    return commands


def delete_commands(data):
    commands = []
    for i in data["dictionary"]:
        commands.append("scoreboard objectives remove " + data["dictionary"][i])

    return commands


def gen_id(string):
    sum = 0
    for i in string:
        sum = sum + (ord(i) & 0xF)
    return str(sum)


if __name__ == "__main__":
    main()
