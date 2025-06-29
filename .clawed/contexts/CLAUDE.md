# Contexts

## Claude sessions

### On startup

Read the latest file in `.clawed/contexts/` to learn what we were talking about most recently.

### On shutdown

Write the file `.clawed/contexts/<date>-<app>.md` to include what we talked about in this session
    Include any older context that is still relevant

Where 
 - `<date>` is the current date and time
   - using YYYY-MM-DD-mm-hh
 - `<app>` is the name of the app hosting `Claude`, which is one of
   - `web` when Claude is being accessed via the web
   - `app` when Claude is being accessed via the Mac App
   - `cli` when Claude is being accessed via the command line (aka "Claude Code"
   - `ios` when Claude is being accessed via the iPhone

For example:
  - `.clawed/contexts/2025-03-31-03-30-cli.md` was written early on the 31st of March, from Claude Clode
  - `.clawed/contexts/2025-04-01-12-00-web.md` was written at noon on April Fool's Day, from the WWW UI
  - `.clawed/contexts/2025-04-02-22-22-app.md` was written late at night on the 2nd of April, from the Mac App
