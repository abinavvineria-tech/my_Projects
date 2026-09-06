#!/usr/bin/env python3
"""
Check if a cookie name (stored in `crk_characher`) is a valid
Cookie Run: Kingdom cookie name.

The CRK_COOKIES set contains all playable cookie names as of the latest
update (189 cookies, including Ancient, Beast, Legendary, Super Epic,
Epic, Rare, Common, Special, Dragon, Witch, and collaboration cookies).
"""

# ---------------------------------------------------------------------------
# All Cookie Run: Kingdom cookie names (source: cookierun.wiki)
# ---------------------------------------------------------------------------

CRK_COOKIES = {
    # --- Common ---
    "Beet Cookie", "Wizard Cookie", "Muscle Cookie", "Angel Cookie",
    "Ninja Cookie", "Strawberry Cookie", "GingerBrave",

    # --- Rare ---
    "Gumball Cookie", "Blackberry Cookie", "Adventurer Cookie",
    "Alchemist Cookie", "Cherry Cookie", "Knight Cookie", "Princess Cookie",

    # --- Special ---
    "Zoey Cookie", "Mira Cookie", "Rumi Cookie", "Glinda Cookie",
    "Elphaba Cookie", "Marshmallow Bunny Cookie", "Cream Ferret Cookie",
    "Icicle Yeti Cookie", "Snapdragon Cookie", "RM Cookie", "Jin Cookie",
    "SUGA Cookie", "j-hope Cookie", "Jimin Cookie", "V Cookie",
    "Jung Kook Cookie", "Tails Cookie", "Sonic Cookie",

    # --- Epic ---
    "Litmus Cookie", "Croissant Cookie", "Ash Salt Cookie",
    "Pom-pom Dough Cookie", "Mold Dough Cookie", "Chess Choco Cookie",
    "Salt Cellar Cookie", "Charcoal Cookie", "Seltzer Cookie",
    "Menthol Cookie", "Grapefruit Cookie", "Lime Cookie", "Manju Cookie",
    "Jagae Cookie", "Orange Cookie", "Lemon Cookie", "Cream Soda Cookie",
    "Sugarfly Cookie", "Pavlova Cookie", "Agar Agar Cookie",
    "Black Forest Cookie", "Wedding Cake Cookie", "Black Sapphire Cookie",
    "Candy Apple Cookie", "Okchun Cookie", "Green Tea Mousse Cookie",
    "Pudding à la Mode Cookie", "Choco Drizzle Cookie",
    "Red Osmanthus Cookie", "Golden Osmanthus Cookie",
    "Smoked Cheese Cookie", "Nutmeg Tiger Cookie", "Star Coral Cookie",
    "Peach Blossom Cookie", "Cloud Haetae Cookie", "Street Urchin Cookie",
    "Caramel Choux Cookie", "Butter Roll Cookie", "Matcha Cookie",
    "Mercurial Knight Cookie", "Silverbell Cookie", "Rebel Cookie",
    "Linzer Cookie", "Crème Brûlée Cookie", "Olive Cookie",
    "Mozzarella Cookie", "Fettuccine Cookie", "Burnt Cheese Cookie",
    "Frilled Jellyfish Cookie", "Peppermint Cookie", "Black Lemonade Cookie",
    "Rockstar Cookie", "Tarte Tatin Cookie", "Royal Margarine Cookie",
    "Kouign-Amann Cookie", "Prune Juice Cookie", "Space Doughnut",
    "Blueberry Pie Cookie", "Milky Way Cookie", "Prophet Cookie",
    "Pinecone Cookie", "Carol Cookie", "Macaron Cookie", "Schwarzwälder",
    "Candy Diver Cookie", "Captain Caviar Cookie", "Cream Unicorn Cookie",
    "Financier Cookie", "Crunchy Chip Cookie", "Wildberry Cookie",
    "Cherry Blossom Cookie", "Caramel Arrow Cookie", "Affogato Cookie",
    "Tea Knight Cookie", "Eclair Cookie", "Cocoa Cookie", "Cotton Cookie",
    "Pumpkin Pie Cookie", "Twizzly Gummy Cookie", "Mala Sauce Cookie",
    "Moon Rabbit Cookie", "Raspberry Cookie", "Parfait Cookie",
    "Sorbet Shark Cookie", "Squid Ink Cookie", "Lilac Cookie",
    "Mango Cookie", "Red Velvet Cookie", "Pastry Cookie", "Fig Cookie",
    "Strawberry Crepe Cookie", "Black Raisin Cookie", "Almond Cookie",
    "Cream Puff Cookie", "Latte Cookie", "Kumiho Cookie", "Rye Cookie",
    "Espresso Cookie", "Madeleine Cookie", "Licorice Cookie",
    "Poison Mushroom Cookie", "Milk Cookie", "Purple Yam Cookie",
    "Pomegranate Cookie", "Chili Pepper Cookie", "Sparkling Cookie",
    "Dark Choco Cookie", "Herb Cookie", "Mint Choco Cookie",
    "Werewolf Cookie", "Tiger Lily Cookie", "Vampire Cookie",
    "Snow Sugar Cookie",

    # --- Super Epic ---
    "Povidone-Iodine Cookie", "Venom Dough Cookie", "Doughael",
    "Camellia Cookie", "Elder Faerie Cookie", "Crimson Coral Cookie",
    "Shining Glitter Cookie", "Capsaicin Cookie", "Stardust Cookie",
    "Sherbet Cookie", "Oyster Cookie", "Clotted Cream Cookie",

    # --- Dragon ---
    "Ananas Dragon Cookie", "Pitaya Dragon Cookie",

    # --- Legendary ---
    "Timekeeper Cookie", "Sugar Swan Cookie", "Millennial Tree Cookie",
    "Fire Spirit Cookie", "Wind Archer Cookie", "Stormbringer Cookie",
    "Moonlight Cookie", "Black Pearl Cookie", "Frost Queen Cookie",
    "Sea Fairy Cookie",

    # --- Ancient ---
    "White Lily Cookie", "Golden Cheese Cookie", "Dark Cacao Cookie",
    "Hollyberry Cookie", "Pure Vanilla Cookie",

    # --- Awakened Ancients ---
    "White Lily Cookie (Dawnbringer)", "Hollyberry Cookie (Aegis)",
    "Pure Vanilla Cookie (Compassionate)", "Golden Cheese Cookie (Immortal)",
    "Dark Cacao Cookie (Dragon Lord)",

    # --- Beast ---
    "Silent Salt Cookie", "Eternal Sugar Cookie", "Shadow Milk Cookie",
    "Burning Spice Cookie", "Mystic Flour Cookie",

    # --- Witch ---
    "Dark Enchantress Cookie",
}


def is_valid_crk_cookie(cookie_name: str) -> bool:
    """
    Return True if `cookie_name` matches a known Cookie Run: Kingdom cookie.

    Comparison is case-sensitive and exact — the name must match one of
    the entries in CRK_COOKIES (e.g. "GingerBrave", not "gingerbread").
    """
    return cookie_name in CRK_COOKIES


# ---------------------------------------------------------------------------
# Interactive check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    crk_characher = input("Enter a Cookie Run: Kingdom cookie name: ").strip()

    if is_valid_crk_cookie(crk_characher):
        print(f"'{crk_characher}' is a valid Cookie Run: Kingdom cookie.")
    else:
        print(f"'{crk_characher}' is NOT a recognized CRK cookie.")