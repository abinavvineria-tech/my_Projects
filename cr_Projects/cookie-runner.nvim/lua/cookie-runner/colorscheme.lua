local M = {}
local palette = {}

function M.get()
  return palette
end

function M.setup(opts)
  opts = opts or {}
  local v = opts.variant
  if v == 'auto' or v == nil then
    v = (vim.o.background == 'light') and 'light' or 'dark'
  end
  local mod = (v == 'light') and 'cookie-runner.colorscheme.cookie-kingdom-light'
                       or 'cookie-runner.colorscheme.cookie-kingdom'
  local ok, res = pcall(require, mod)
  if not ok then
    error('cookie-runner colorscheme: failed to load ' .. mod .. ': ' .. tostring(res))
  end
  palette = res.palette or {}
  vim.g.colors_name = (v == 'light') and 'cookie-kingdom-light' or 'cookie-kingdom'
  if res.setup then res.setup() end
  if res.apply then res.apply() end
  _G.CRKColors = palette
end

function M.dark() M.setup({variant='dark'}) end
function M.light() M.setup({variant='light'}) end

return M
