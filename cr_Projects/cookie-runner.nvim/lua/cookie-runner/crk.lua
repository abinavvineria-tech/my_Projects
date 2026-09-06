-- cookie-runner.nvim CRK integration: validate cookie names from Neovim
local M = {}

-- Load the cookie set from the Python script's data (embedded for speed)
-- Source: crk_cookie_check.py - all 189+ playable cookie names
M.CRK_COOKIES = {
  -- Common
  "Beet Cookie", "Wizard Cookie", "Muscle Cookie", "Angel Cookie",
  "Ninja Cookie", "Strawberry Cookie", "GingerBrave",
  -- Rare
  "Gumball Cookie", "Blackberry Cookie", "Adventurer Cookie",
  "Alchemist Cookie", "Cherry Cookie", "Knight Cookie", "Princess Cookie",
  -- Special
  "Zoey Cookie", "Mira Cookie", "Rumi Cookie", "Glinda Cookie",
  "Elphaba Cookie", "Marshmallow Bunny Cookie", "Cream Ferret Cookie",
  "Icicle Yeti Cookie", "Snapdragon Cookie",
  -- BTS Collab
  "RM Cookie", "Jin Cookie", "SUGA Cookie", "j-hope Cookie", "Jimin Cookie", "V Cookie", "Jung Kook Cookie",
  -- Sonic Collab
  "Tails Cookie", "Sonic Cookie",
  -- Epic
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
  -- Super Epic
  "Povidone-Iodine Cookie", "Venom Dough Cookie", "Doughael",
  "Camellia Cookie", "Elder Faerie Cookie", "Crimson Coral Cookie",
  "Shining Glitter Cookie", "Capsaicin Cookie", "Stardust Cookie",
  "Sherbet Cookie", "Oyster Cookie", "Clotted Cream Cookie",
  -- Dragon
  "Ananas Dragon Cookie", "Pitaya Dragon Cookie",
  -- Legendary
  "Timekeeper Cookie", "Sugar Swan Cookie", "Millennial Tree Cookie",
  "Fire Spirit Cookie", "Wind Archer Cookie", "Stormbringer Cookie",
  "Moonlight Cookie", "Black Pearl Cookie", "Frost Queen Cookie", "Sea Fairy Cookie",
  -- Ancient
  "White Lily Cookie", "Golden Cheese Cookie", "Dark Cacao Cookie",
  "Hollyberry Cookie", "Pure Vanilla Cookie",
  -- Awakened Ancients
  "White Lily Cookie (Dawnbringer)", "Hollyberry Cookie (Aegis)",
  "Pure Vanilla Cookie (Compassionate)", "Golden Cheese Cookie (Immortal)",
  "Dark Cacao Cookie (Dragon Lord)",
  -- Beast
  "Silent Salt Cookie", "Eternal Sugar Cookie", "Shadow Milk Cookie",
  "Burning Spice Cookie", "Mystic Flour Cookie",
  -- Witch
  "Dark Enchantress Cookie",
}

-- Build a fast lookup table
local cookie_set = {}
for _, v in ipairs(M.CRK_COOKIES) do cookie_set[v] = true end
M._set = cookie_set

--- Validate a cookie name (case-sensitive, exact match)
--- @param name string
--- @return boolean
function M.is_valid(name)
  if type(name) ~= "string" or name == "" then return false end
  return M._set[name] == true
end

--- Fuzzy search: return all cookies containing the query (case-insensitive)
--- @param query string
--- @return string[]
function M.search(query)
  if type(query) ~= "string" or query == "" then return {} end
  query = query:lower()
  local results = {}
  for _, name in ipairs(M.CRK_COOKIES) do
    if name:lower():find(query, 1, true) then
      table.insert(results, name)
    end
  end
  return results
end

--- Show validation result in a vim notify or print
--- @param name string
function M.check(name)
  if M.is_valid(name) then
    vim.notify("CRK: " .. name .. " is a valid Cookie Run: Kingdom cookie!",
      vim.log.levels.INFO, { title = "Cookie Runner" })
  else
    vim.notify("CRK: '" .. name .. "' is NOT a recognized CRK cookie.",
      vim.log.levels.WARN, { title = "Cookie Runner" })
  end
end

--- Fuzzy-search and show results in a vim.notify (truncated list)
--- @param query string
function M.find(query)
  local results = M.search(query)
  if #results == 0 then
    vim.notify("CRK: No cookies found matching '" .. query .. "'",
      vim.log.levels.WARN, { title = "Cookie Runner" })
  else
    local preview = table.concat(results, ", ", 1, math.min(10, #results))
    if #results > 10 then preview = preview .. ", ..." end
    vim.notify("CRK: Found " .. #results .. " cookie(s): " .. preview,
      vim.log.levels.INFO, { title = "Cookie Runner" })
  end
end

return M
