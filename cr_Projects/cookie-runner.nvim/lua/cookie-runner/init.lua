-- cookie-runner.nvim: Cookie Run: Kingdom themed Neovim plugin
-- https://github.com/cookie-run/cookie-runner.nvim
local M = {}

-- Lazy-load submodules for faster startup
M._loaded = {}

local function lazy_require(name)
  if M._loaded[name] then return M._loaded[name] end
  M._loaded[name] = require(name)
  return M._loaded[name]
end

--- Setup cookie-runner.nvim
--- @param opts table|nil  { colorscheme = { variant = 'auto'|'dark'|'light' }, crk = { enabled = true } }
function M.setup(opts)
  opts = opts or {}
  opts.colorscheme = opts.colorscheme or {}
  opts.crk = opts.crk or {}

  -- Colorscheme
  if opts.colorscheme.enabled ~= false then
    local ok, cs = pcall(require, "cookie-runner.colorscheme")
    if ok then
      cs.setup(opts.colorscheme)
    else
      vim.notify("[cookie-runner] colorscheme failed to load: " .. vim.inspect(cs),
        vim.log.levels.WARN, { title = "Cookie Runner" })
    end
  end

  -- CRK commands
  if opts.crk.enabled ~= false then
    local ok_cr, crk = pcall(require, "cookie-runner.crk")
    if ok_cr then
      M._loaded["cookie-runner.crk"] = crk
      M.crk = crk
    end
  end

  -- Telescope integration: pick CRK cookie as fuzzy search
  M.setup_commands()
end

function M.setup_commands()
  -- :CRKCheck <cookie-name>  — validate a cookie name
  vim.api.nvim_create_user_command("CRKCheck", function(ctx)
    local crk = lazy_require("cookie-runner.crk")
    local name = ctx.args
    if name == "" then
      -- fall back to word under cursor
      local word = vim.fn.expand("<cword>")
      if word == "" then
        vim.notify("CRK: Provide a cookie name, e.g. :CRKCheck Pure Vanilla Cookie",
          vim.log.levels.WARN, { title = "Cookie Runner" })
        return
      end
      name = word
    end
    crk.check(name)
  end, { nargs = "?", complete = function(arg)
    local crk = lazy_require("cookie-runner.crk")
    local matches = crk.search(arg)
    return matches
  end, desc = "Check if a cookie name is valid in Cookie Run: Kingdom" })

  -- :CRKFind <query>  — fuzzy search cookies
  vim.api.nvim_create_user_command("CRKFind", function(ctx)
    local crk = lazy_require("cookie-runner.crk")
    local query = ctx.args or ""
    crk.find(query)
  end, { nargs = "?", desc = "Fuzzy-search Cookie Run: Kingdom cookies" })

  -- :CRKList  — list all 189+ cookies (paged)
  vim.api.nvim_create_user_command("CRKList", function()
    local crk = lazy_require("cookie-runner.crk")
    local lines = { "Cookie Run: Kingdom — Full Roster (" .. #crk.CRK_COOKIES .. " cookies)", "" }
    for _, name in ipairs(crk.CRK_COOKIES) do
      table.insert(lines, "  " .. name)
    end
    vim.fn.setqflist({}, " ", { title = "CRK Cookies", lines = lines })
    vim.cmd("botright cwindow | resize 20")
    vim.notify("CRK: Loaded " .. #crk.CRK_COOKIES .. " cookies into quickfix",
      vim.log.levels.INFO, { title = "Cookie Runner" })
  end, { desc = "List all Cookie Run: Kingdom cookies in quickfix" })

  -- :CRKRandom  — pick a random cookie
  vim.api.nvim_create_user_command("CRKRandom", function()
    local crk = lazy_require("cookie-runner.crk")
    local idx = math.random(1, #crk.CRK_COOKIES)
    local cookie = crk.CRK_COOKIES[idx]
    vim.notify("CRK Random: " .. cookie .. " (#" .. idx .. " of " .. #crk.CRK_COOKIES .. ")",
      vim.log.levels.INFO, { title = "Cookie Runner" })
  end, { desc = "Pick a random Cookie Run: Kingdom cookie" })

  -- :CRKColor <dark|light|auto>  — switch cookie-kingdom variant
  vim.api.nvim_create_user_command("CRKColor", function(ctx)
    local cs = lazy_require("cookie-runner.colorscheme")
    local variant = ctx.args ~= "" and ctx.args or "auto"
    cs.setup({ variant = variant })
  end, { nargs = "?", complete = function()
    return { "dark", "light", "auto" }
  end, desc = "Switch Cookie Kingdom colorscheme variant" })
end

-- Auto-detect lazy-loading (after treesitter loads, reload colorscheme to apply TS highlights)
vim.api.nvim_create_autocmd("User", {
  pattern = "LazyDone",
  callback = function()
    local cs_ok, cs = pcall(require, "cookie-runner.colorscheme")
    if cs_ok then
      cs.setup()
    end
  end,
})

return M
