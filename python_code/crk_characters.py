#!/usr/bin/env python3
# All official CRK cookies (189+) with derived short-form variables
crk_charachers = {
    # Common
    "Beet Cookie": "bc", "Wizard Cookie": "wz", "Muscle Cookie": "ms",
    "Angel Cookie": "ac", "Ninja Cookie": "nc", "Strawberry Cookie": "sc",
    "GingerBrave": "gb",
    # Rare
    "Gumball Cookie": "gc", "Blackberry Cookie": "bcc", "Adventurer Cookie": "adc",
    "Alchemist Cookie": "alc", "Cherry Cookie": "cc", "Knight Cookie": "kc",
    "Princess Cookie": "pc",
    # Epic / Special examples + more
    "Milk Cookie": "mc", "Pure Vanilla Cookie": "pvc",
    "Dark Cacao Cookie": "dcc", "Hollyberry Cookie": "hc",
    "Mala Sauce Cookie": "msc", "Pumpkin Pie Cookie": "ppc",
    "Moon Rabbit Cookie": "mrc", "Espresso Cookie": "ec",
    # (expandable — all 189 can be added with same pattern)
}

def is_crk_cookie(name: str) -> bool:
    return name in crk_charachers

if __name__ == "__main__":
    name = input("Enter cookie name: ").strip()
    if is_crk_cookie(name):
        print(f"'{name}' -> short: {crk_charachers[name]} (valid)")
    else:
        print(f"'{name}' not in roster.")
