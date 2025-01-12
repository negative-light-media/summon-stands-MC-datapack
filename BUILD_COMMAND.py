import json
from shutil import make_archive
from pathlib import Path

# Goal: Write Datapack that sets up all display items
VERSION = (1, 0, 1) # Major, Minor, Fix per semantic versioning v2 https://semver.org/
MC_PACK_VERSION = 61
DIR_OUTPUT = "./output/"
BUILD_DIR = "./output/build"
FUNC_DIR_NAME = "function"

DIR_DATA = f"{BUILD_DIR}/data"
DIR_PACK = f"{BUILD_DIR}/summon-stands"
MC_NAMESPACE = f"{BUILD_DIR}/minecraft"
MC_FUNC = f"{MC_NAMESPACE}/tags/{FUNC_DIR_NAME}"
DIR_FUNC = f"{DIR_PACK}/{FUNC_DIR_NAME}"
OUTPUT_FILE = f"{DIR_OUTPUT}/summon-stands_{MC_PACK_VERSION}_{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
armor_elements = ["boots", "leggings", "chestplate", "helmet"]

armor_class = ["leather", "iron", "diamond", "golden", "chainmail", "netherite"]

trims = [
    "sentry",
    "dune",
    "coast",
    "wild",
    "ward",
    "eye",
    "tide",
    "snout",
    "rib",
    "spire",
    "wayfinder",
    "raiser",
    "shaper",
    "host",
    "silence",
    "vex"
]


materials = [
    "iron",
    "copper",
    "gold",
    "lapis",
    "emerald",
    "diamond",
    "netherite",
    "redstone",
    "amethyst",
    "quartz",
]





def getPos(x, y, z):
    return f"~{x} ~{y} ~{z}"


def getItem(type, element, material=None, trim=None):
    # {id:"minecraft:leather_helmet", Count: 1b, tag: {Damage: 0, Trim: {material: "minecraft:iron", pattern: "minecraft:sentry"}}}
    retValue = "{"
    retValue += f'id: "minecraft:{type}_{element}", count: 1'
    if trim != None:
        retValue += ", components: { \"minecraft:trim\":"
        retValue += "{"
        retValue += f'material: "minecraft:{material}", pattern: "minecraft:{trim}"'
        retValue += "}"
        retValue += "}"
    retValue += "}"
    return retValue


def getArmor(type, trim=None, material=None):
    # ARrmorItems Helmet, chestplate, leggings, boots
    retValue = "ArmorItems: ["
    for element in armor_elements:
        retValue += getItem(type, element, trim, material)
        retValue += ","

    retValue = retValue[:-1]

    retValue += "]"
    return retValue


def makeSummon(x, y, z, material, trim, type):
    out = f"summon armor_stand {getPos(x,y,z)} "
    out += "{"
    out += getArmor(type, material, trim)
    out += "}"
    return out

def checkDirectories():
    Path(DIR_FUNC).mkdir(parents=True, exist_ok=True)
    Path(MC_FUNC).mkdir(parents=True, exist_ok=True)


        
def main():

    x_off = 1
    y_off = 0
    z_off = -1
    commands = []
    
    checkDirectories()

    trim_x_off = 1
    trim_commands = []
    print("BUILDING TRIM COMMANDS")
    for trim in trims:
        # Generate Each Trim Type
        for mat in materials:
            # Generate Command
            for armor in armor_class:
                print(f"{mat}-{trim}-{armor}")
                commands.append(f"setblock {getPos(x_off, y_off, z_off )} stone")
                commands.append(makeSummon(x_off, 15, z_off, mat, trim, armor))

                trim_commands.append(f"setblock {getPos(trim_x_off, y_off, z_off )} stone")
                trim_commands.append(makeSummon(trim_x_off, 15, z_off, mat, trim, armor))
                z_off -= 1
                y_off += 2
            x_off += 2
            trim_x_off += 2
            z_off = -1
            y_off = 0
        trim_x_off = 1
        with open(f"{DIR_FUNC}/load_{trim}.mcfunction", "w") as file:
            for cmd in trim_commands:
                file.write(cmd + "\n")
    # print(commands)
    print("#################################################################################")


    with open(f"{DIR_FUNC}/load_all.mcfunction", "w") as file:
        print("WRITING LOAD ALL FUNCTION")
        for cmd in commands:
            file.write(cmd + "\n")

    # Add the load.mcfunction file
    with open(f"{DIR_FUNC}/load.mcfunction", "w") as file:
        print("WRITING PACK LOAD FUNCTION")
        file.write("# Load all functions")

    with open(f"{BUILD_DIR}/pack.mcmeta", "w") as file:
        print("Writing Pack meta data")
        mcmeta = {
            "pack": {
                "pack_format": MC_PACK_VERSION,
                "description": "Summon armor stands with all trims in all armor types."
            }
        }
        json.dump(mcmeta, file, indent=4)
        
    with open(f"{MC_FUNC}/load.json", "w") as file:
        print("Writing Minecraft Load JSON")
        mcload = {
            "values": [
                "summon-stands:load"
            ]
        }
        

    # Create ZIP
    print("WRITING ZIP FILE")
    make_archive(OUTPUT_FILE, "zip", BUILD_DIR)



if __name__ == "__main__":
    main()


    # 41 + component base format for Armor Items
    # This can be retrived by doing `/data get entity <entity id> ArmorItems
    """
    Armor Stand has the following entity data: 
    [
        {}, 
        {}, 
        {}, 
        {
            components: 
            {
                "minecraft:trim": 
                    {
                        material: "minecraft:redstone", 
                        pattern: "minecraft:sentry"
                    }
            }, 
            count: 1, 
            id: "minecraft:iron_helmet"
        }
    ]
    """