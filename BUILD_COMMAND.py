import os
import json
import zipfile

# Goal: Write Datapack that sets up all display items
VERSION = (1, 0, 0) # Major, Minor, Fix per semantic versioning v2 https://semver.org/
MC_PACK_VERSION = 41
DIR_OUTPUT = "./output"
DIR_DATA = f"{DIR_OUTPUT}/data"
DIR_PACK = f"{DIR_DATA}/summon-stands"
DIR_FUNC = f"{DIR_PACK}/functions"
OUTPUT_FILE = f"summon-stands_{MC_PACK_VERSION}_{VERSION[0]}.{VERSION[1]}.{VERSION[2]}.zip"
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

def main():

    x_off = 1
    y_off = 0
    z_off = -1
    commands = []

    if not os.path.exists(DIR_OUTPUT):
        os.mkdir(DIR_OUTPUT)
    
    if not os.path.exists(DIR_DATA):
        os.mkdir(DIR_DATA)

    if not os.path.exists(DIR_PACK):
        os.mkdir(DIR_PACK)

    if not os.path.exists(DIR_FUNC):
        os.mkdir(DIR_FUNC)

    trim_x_off = 1
    trim_commands = []
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


    with open(f"{DIR_FUNC}/load_all.mcfunction", "w") as file:
        for cmd in commands:
            file.write(cmd + "\n")

    # Add the load.mcfunction file
    with open(f"{DIR_FUNC}/load.mcfunction", "w") as file:
        file.write("# Load all functions")

    with open(f"{DIR_OUTPUT}/pack.mcmeta", "w") as file:
        print("Writing Pack meta data")
        mcmeta = {
            "pack": {
                "pack_format": MC_PACK_VERSION,
                "description": "Summon armor stands with all trims in all armor types."
            }
        }
        json.dump(mcmeta, file, indent=4)

    # Create ZIP
    final_output = zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED)
    final_output.write(DIR_OUTPUT)
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zfile:
        for folder, subs, files in os.walk(DIR_OUTPUT):
            for file in files:
                p = os.path.join(folder, file)
                zfile.write(p, arcname=os.path.relpath(p, DIR_OUTPUT))


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