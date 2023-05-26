import os

# Goal: Write Datapack that sets up all display items
DIR_OUTPUT = "./output/"
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


x_off = 1
y_off = 0
z_off = -1
commands = []


def getPos(x, y, z):
    return f"~{x} ~{y} ~{z}"


def getItem(type, element, material=None, trim=None):
    # {id:"minecraft:leather_helmet", Count: 1b, tag: {Damage: 0, Trim: {material: "minecraft:iron", pattern: "minecraft:sentry"}}}
    retValue = "{"
    retValue += f'id: "minecraft:{type}_{element}", Count:1b'
    if trim != None:
        retValue += ", tag: { Trim: "
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


if not os.path.exists(DIR_OUTPUT):
    os.mkdir(DIR_OUTPUT)

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
    with open(f"{DIR_OUTPUT}load_{trim}.mcfunction", "w") as file:
        for cmd in trim_commands:
            file.write(cmd + "\n")
# print(commands)


with open(f"{DIR_OUTPUT}load_all.mcfunction", "w") as file:
    for cmd in commands:
        file.write(cmd + "\n")
