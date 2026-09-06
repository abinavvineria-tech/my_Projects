The Missing Piece Studio (TMPS)
Tagline: Every project has a missing piece. Let Hermes find it.

Real Hermes Agent adapter - no mocks.

CLI:
  ./tmps doctor   - check Hermes + system
  ./tmps missing  - Hermes analyzes current project
  ./tmps agent    - Hermes status
  ./tmps status   - studio status
  ./tmps run      - dev server
  ./tmps test     - run tests
  ./tmps help

Adapter: src/core/hermes/adapter.py - calls real `hermes` CLI
