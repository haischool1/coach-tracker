# Update my tracker

Use this when they say "update my tracker", or when they add a new version of this kit. Their tracker gets the new version at the **same link**, and keeps every bit of data and every custom change.

## 0. Get the newest version from GitHub

New versions are posted to a public GitHub folder: https://github.com/haischool1/coach-tracker

1. Fetch https://raw.githubusercontent.com/haischool1/coach-tracker/main/version.json. It has `version` (like "3.1"), `date` and `notes` (what's new, in plain words).
2. Compare `version` with the `byoc-version` line near the top of this skill's `tracker-template.html`. If GitHub's is newer, use GitHub's files for every step below instead of this skill's copies:
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/tracker-template.html
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/updating.md (the newest version of these steps; follow it instead of this file)
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/check_tracker.py
3. If you can't reach GitHub (no web access, or the fetch fails), say so in one line and use this skill's copies. If they say they have a newer kit file, ask them to add it to the chat.

## 1. See what they have

1. Find their tracker URL in `tracker-notes.md` or `coach-playbook.md`.
2. Read it with the Artifact tool (`action: "read"`) and note where the full page was saved.
3. Run `python3 scripts/check_tracker.py <saved page>` (the script is in this skill's folder). It says which kit version the page is, and whether the page was changed after setup.
4. If it's already the latest version and unchanged, tell them they're up to date and stop.
5. List every changelog line in `tracker-notes.md` that starts with "Custom:". Those are the features to carry over.
6. If the checker says the page was changed but there are no "Custom:" lines, ask them what they had added. If nobody knows, look through the saved page for anything the new template doesn't have, and describe it to them in plain words.

## 2. Tell them and get a yes

In 3 to 5 short lines: the best of what's new (see "What's new" below), that all their data stays, which of their own features you'll carry over, and anything that will look different. Then ask "Want me to update it?"

## 3. Keep a backup

Save their current page to the project files as `tracker-backup-YYYY-MM-DD.html` (or give it to them as a file). If anything goes wrong, publishing that file to the same link puts the old page back, with their data untouched.

## 4. Build the new page

1. Copy `tracker-template.html` from this skill's folder and change the first line to `<title><First name>'s Training Log</title>`.
2. Rebuild each "Custom:" feature on the new page, following "Bigger changes" in `customizing.md`. Use the same data fields as before so their saved data for those features still shows.

## 5. Publish to the same link

Publish with `url` set to their tracker's URL. Don't pass capabilities; the tracker keeps the ones it has. Never publish it as a new artifact: a new one starts with an empty database.

## 6. Data touch-ups

Do only the steps for the version they came from. Always `get` a doc, change it, and `set` it back with `if_version`, keeping everything else.

**From kit 3.0 to 3.1** (also do this after the kit 2 steps below)

- `settings.week`: the Workout tab now shows a real week, Sunday to Saturday. Ask which days they lift and which are rest days, then save `settings.week` in `config/main` as 7 plan day ids, Sunday first, with `"rest"` for rest days (for example `["d6","d1","rest","d2","rest","d4","d5"]`). Without it the tracker guesses: Day 1 on Monday, in rotation order.
- Meals: from now on, save a clock time on every food (`time`, like "7:45 AM"). The tracker sorts food into Breakfast (4 to 10:59 am), Lunch (11 am to 2:59 pm), Snacks (3 to 4:59 pm), Dinner (5 to 8:59 pm) and Snacks (later). A `meal` tag still wins over the clock.
- Women see Hips instead of Chest in measurements (from `profile.sex`, or cycle notes on). Nothing to change; old chest readings still show.

**From kit 2 to 3.0**

- `profile.foodDefaults` and `profile.coachNotes` in `config/main`: if either is one long piece of text, split it into a list of short sentences, one fact or rule each. Keep all of it.
- `settings.rotation`: ask which days they train and save their week with rest days (see "Rest days" in `targets-and-plan.md`). If they have no plan day named "Rest day ...", add one (rename an optional core day if they have one, keeping its id). Renumber the lifting days' names by their spot in the week, keeping every id and exercise name.
- `settings.weeklyRate`: set it from `profile.weeklyGoal` in lb a week as `[low, high]`, negative to lose (see `targets-and-plan.md`).
- Their usual meals: if they have a usual breakfast saved, add `"when": "morning"`. Offer to turn their usual meals and recipes (like a shake) into combos with `parts` (see `tracker-data.md`).
- Nothing else needs changing. Old food lines without a meal tag show as a plain list; new ones get grouped by meal.

## 7. Check it and tell them

1. Open it with the Artifact tool (`action: "open"`) and check it loads with their data: the Dashboard should show their name, phase and day count.
2. Update `tracker-notes.md`: the new kit version and today's date, a changelog line "Updated to kit <version>", and their "Custom:" lines (reworded if a feature changed). Update the logging rules in `coach-playbook.md` from `coaching-rules.md` (meal tags, combos, the one rule book).
3. Tell them in 3 lines what changed and one thing to try first, for example: "Open the Dashboard in the morning. It lists today's to-dos and ticks them off as you go."

## What's new in 3.1

- **Your week on the Workout tab:** Sunday to Saturday, with done, missed and rest days. Drag a day onto another to move it; it becomes your usual week. Missed a workout? A catch-up note shows the best day to make it up.
- **Done or not:** each workout shows how many lifts you've logged, with a Finish button.
- **Clearer sets:** small tags show what improved (+5 lb, +2 reps), gold for a new best, orange when reps fall under your range.
- **This week** is three simple bar charts (calories, protein, added sugar) with your goal as a green band.
- **New look:** 3D icons on the menu, a gold-sparkle Coach button, meals in color by time of day, a calendar when you tap the date, and the page reopens where you left off.

## What's new in 3.0

- **Dashboard** is the home tab: the morning weigh-in, a Today list that ticks itself off (weigh-in, workout, protein, check-ins), and today's workout and food at a glance.
- **Coach button** in the middle of the tab bar, from any tab. It can save new foods, combos and food rules too.
- **Food:** one-tap foods sorted by what you eat most, combos (one tap logs a whole usual breakfast), meals grouped into breakfast, lunch, dinner and snacks, and tap any food to change the amount or delete it (with undo).
- **Workout:** a go up, stay or drop target for every lift, one lift open at a time, trophies for new personal records, sets that save as you type, and a small rest timer.
- **Rest days** sit in your week in order ("Day 2 Rest"), with an easy-walk tip and a "Rest day done" check-off. The rest timer starts on its own when you enter reps, with − and + buttons for 10 seconds less or more.
- **Progress:** a progress check against your weekly weight goal (for a bulk, a cut or maintaining), the week at a glance, what's coming up, one measurements chart with a picker, and photos with a side-by-side compare.
- **One rule book:** your food rules live in the tracker, so the tracker's coach and every project chat follow the same rules.
