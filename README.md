# Every Scoreboard

A tool to create datapacks which will include all the scoreboard objectives available in Minecraft. 
All of them, for ~~any~~ most versions.

# How to use

You can find 'pre-made' datapacks over [here](https://github.com/samipourquoi/every-scoreboard/tags).
If you don't find what you need, read the following section; you can skip it otherwise.

## 'Compiling'

First of all, clone the repository: 
```shell script
$ git clone https://github.com/samipourquoi/every-scoreboard.git
$ cd every-scoreboard
```

Install the dependencies with this command; 
make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed. 
```shell script
$ pip install -r requirements.txt
```

To 'compile' the datapacks, run the following:
```shell script
# For 1.16.2
$ python3 scripts/create.py --mcversion="1.16.2" -c

# For 1.15.2
$ python3 scripts/create.py --mcversion="1.15.2"
```
The `-c` flag will add the [custom objectives](https://minecraft.gamepedia.com/Statistics#List_of_custom_statistic_names)
to the datapack. Be careful however! It is made for the latest version(s) of the game only.
You will probably need to modify the resulting `mcfunction` files at the end if you
do it for an older version of Minecraft.

The resulting files will end up at `datapacks/every-scoreboard-<version>` and `dictionaries/dictionary-<version>.json`.
We will come back to the second file later on.

## Running the datapack

Once you have the datapack ready, move it over your world's datapacks folder. Log on to your world and enter the following commands:
```
/reload
/function every-scoreboard:create
```

And here you're all set! If you wish to get rid of all of these objectives, run:
```
/function every-scoreboard:delete
```

See the naming convention over [here](). 

Note that the scoreboard names won't change between versions of the game.
That means you can have your world in 1.15.2 with that datapack, then updates your world to 1.16.2, run the datapack
for that version again, and you will keep your scoreboards from 1.15.2, with the new ones. 

## Naming convention

The scoreboards are name accordingly:
- `m-<block>` Mined blocks
- `u-<item>` Used items
- `c-<item>` Crafted items
- `b-<item>` Broken tools
- `p-<item>` Picked up items
- `d-<item>` Dropped items
- `k-<mob>` Killed mobs
- `kb-<mob>` Killed by mob
- `z-<stats>` Custom (find all the possible `stats` over [here](https://minecraft.gamepedia.com/Statistics#List_of_custom_statistic_names))

### ⚠️ Important note ⚠️

Scoreboards name can't be longed than 16 characters! To solve that issue, the program truncates the names which are too
long, and replace their end with a series of number. 

If you wish to create your own tool solving that issue, you can find
a JSON of key-value's (fullname to truncated name) in the generated `dictionaries/dictionary-<version>.json` file.

I have programmed a linking bot between a Discord chat and a Minecraft server, with other utilities, that handles that
issue. You can find the code over [here](https://github.com/samipourquoi/endbot) if you wish to set it up.

# Credits
Contact me on Discord `samipourquoi#9267` or via the Endtech discord: https://discord.gg/t7UwaDc.

Feel free to create an issue if you need any help 😀
