# npm/react-scripts Build Debugging — session 2026-09-05
Bare scaffolds missing `public/index.html` + `src/index.js` cause `react-scripts build` failure. Fix: `mkdir -p public` + minimal index.html; scaffold index.js/App.js if `find src` empty. Deprecated warnings non-blocking.
