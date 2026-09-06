-- Cookie Run: Kingdom Dark Colorscheme
-- Warm, cozy, cookie-like palette
local M = {}

local function set_highlights()
  local colors = {
    bg = '#1A0F0A', bg_alt = '#2D1810', bg_float = '#3D2518',
    bg_gutter = '#1A0F0A', bg_visual = '#3D2518',
    fg = '#F5D7A1', fg_alt = '#C4A882', fg_gutter = '#8B5E3C',
    fg_line_nr = '#C8834A', fg_cursor_nr = '#F5C16C',
    border = '#8B5E3C',
    accent1 = '#F5C16C', accent2 = '#7DD3FC', accent3 = '#6B4FA0',
    accent4 = '#7CB342', accent5 = '#E05A45', accent6 = '#F8BBD9',
    diag_error = '#EF4444', diag_warn = '#F59E0B',
    diag_info = '#60A5FA', diag_hint = '#34D399',
  }
  local h = vim.api.nvim_set_hl

  -- Base
  h(0, 'Normal',        { bg = colors.bg, fg = colors.fg })
  h(0, 'NormalFloat',   { bg = colors.bg_float, fg = colors.fg })
  h(0, 'FloatBorder',   { bg = colors.bg_float, fg = colors.border })
  h(0, 'Cursor',        { fg = '#1A0F0A', bg = colors.accent1 })
  h(0, 'CursorLine',    { bg = colors.bg_visual })
  h(0, 'CursorLineNr',  { fg = colors.fg_cursor_nr, bg = colors.bg })
  h(0, 'LineNr',        { fg = colors.fg_line_nr, bg = colors.bg_gutter })
  h(0, 'SignColumn',    { bg = colors.bg_gutter })
  h(0, 'EndOfBuffer',   { fg = colors.bg })
  h(0, 'NonText',       { fg = colors.fg_gutter })

  -- Search / selection
  h(0, 'Search',        { bg = colors.accent5, fg = colors.fg })
  h(0, 'IncSearch',     { bg = colors.accent1, fg = colors.bg })
  h(0, 'Visual',        { bg = colors.bg_visual })
  h(0, 'VisualNOS',     { bg = colors.bg_visual })
  h(0, 'MatchParen',    { bg = colors.accent2, fg = colors.bg })

  -- Status / tab / win
  h(0, 'StatusLine',    { bg = colors.bg_alt, fg = colors.fg })
  h(0, 'StatusLineNC',  { bg = colors.bg, fg = colors.fg_gutter })
  h(0, 'TabLine',       { bg = colors.bg_float, fg = colors.fg_alt })
  h(0, 'TabLineFill',   { bg = colors.bg })
  h(0, 'TabLineSel',    { bg = colors.accent1, fg = colors.bg })
  h(0, 'WinSeparator',  { fg = colors.border })
  h(0, 'VertSplit',     { fg = colors.border })

  -- Popup menu
  h(0, 'Pmenu',         { bg = colors.bg_float, fg = colors.fg })
  h(0, 'PmenuSel',      { bg = colors.accent1, fg = colors.bg })
  h(0, 'PmenuSbar',     { bg = colors.bg_float })
  h(0, 'PmenuThumb',    { bg = colors.accent1 })

  -- Fold / diff
  h(0, 'Folded',        { bg = colors.bg_alt, fg = colors.fg_alt })
  h(0, 'FoldColumn',    { fg = colors.accent1 })
  h(0, 'DiffAdd',       { bg = colors.accent4 })
  h(0, 'DiffChange',    { bg = colors.accent2 })
  h(0, 'DiffDelete',    { bg = colors.accent5 })
  h(0, 'DiffText',      { bg = colors.accent1 })

  -- Messages
  h(0, 'ErrorMsg',      { fg = colors.diag_error })
  h(0, 'WarningMsg',    { fg = colors.diag_warn })
  h(0, 'ModeMsg',       { fg = colors.accent1 })
  h(0, 'MoreMsg',       { fg = colors.accent4 })
  h(0, 'Question',      { fg = colors.accent3 })

  -- Syntax base
  h(0, 'Comment',       { fg = colors.fg_gutter, italic = true })
  h(0, 'Constant',      { fg = colors.accent6 })
  h(0, 'String',        { fg = colors.accent4 })
  h(0, 'Character',     { fg = colors.accent4 })
  h(0, 'Number',        { fg = colors.accent1 })
  h(0, 'Float',         { fg = colors.accent1 })
  h(0, 'Boolean',       { fg = colors.accent3 })

  -- Keywords / functions
  h(0, 'Identifier',    { fg = colors.fg })
  h(0, 'Function',      { fg = colors.accent4 })
  h(0, 'Statement',     { fg = colors.accent3 })
  h(0, 'Conditional',   { fg = colors.accent3 })
  h(0, 'Repeat',        { fg = colors.accent3 })
  h(0, 'Operator',      { fg = colors.accent2 })
  h(0, 'PreProc',       { fg = colors.accent6 })
  h(0, 'Type',          { fg = colors.accent2 })
  h(0, 'StorageClass',  { fg = colors.accent3 })
  h(0, 'Structure',     { fg = colors.accent2 })

  -- Special keywords
  h(0, 'Special',       { fg = colors.accent1 })
  h(0, 'SpecialChar',   { fg = colors.accent5 })
  h(0, 'Tag',           { fg = colors.accent1 })
  h(0, 'Delimiter',     { fg = colors.fg_alt })
  h(0, 'SpecialComment',{ fg = colors.accent6 })
  h(0, 'Todo',          { fg = colors.accent3, bold = true })

  -- Diagnostic / git
  h(0, 'DiagnosticError',      { fg = colors.diag_error })
  h(0, 'DiagnosticWarn',       { fg = colors.diag_warn })
  h(0, 'DiagnosticInfo',       { fg = colors.diag_info })
  h(0, 'DiagnosticHint',       { fg = colors.diag_hint })
  h(0, 'DiagnosticOk',         { fg = colors.accent4 })
  h(0, 'DiagnosticUnderlineError', { sp = colors.diag_error, undercurl = true })
  h(0, 'DiagnosticUnderlineWarn', { sp = colors.diag_warn, undercurl = true })

  -- Spell
  h(0, 'SpellBad',      { sp = colors.diag_error, undercurl = true })
  h(0, 'SpellCap',      { sp = colors.diag_warn, undercurl = true })
  h(0, 'SpellRare',     { sp = colors.accent3, undercurl = true })
  h(0, 'SpellLocal',    { sp = colors.accent2, undercurl = true })

  -- Completion / info
  h(0, 'Info',          { fg = colors.accent2 })
  h(0, 'Title',         { fg = colors.accent1, bold = true })
  h(0, 'Directory',     { fg = colors.accent4 })
  h(0, 'Underlined',    { fg = colors.accent2, underline = true })
  h(0, 'Ignore',        { fg = colors.bg })
end

set_highlights()
return M
