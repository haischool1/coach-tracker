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

## 0b. Refresh training knowledge (quietly, every time)

Do this on every "update my tracker" or "update me", even when the tracker itself is already up to date. Also do it alone when they say "refresh my training knowledge". It is quiet by default: most clients only see the app update, and their plan changes when they ask for a change.

1. From the `version.json` you already fetched, read `knowledge` (like "1.1") and `knowledgeNotes`. Compare `knowledge` with the `knowledge-version` line in the client's `tracker-notes.md`. If that line is missing, treat GitHub's as newer.
2. If GitHub's is not newer, say nothing about it and move on.
3. If it is newer, fetch these three files and use them as your reference for every plan change and exercise suggestion from now on, then save the new `knowledge-version` line in `tracker-notes.md`:
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/coach-knowledge/planning-playbook.md
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/coach-knowledge/recommendation-guide.md
   - https://raw.githubusercontent.com/haischool1/coach-tracker/main/coach-knowledge/exercise-a-to-z.md

   The exercise list is a set of extras that work certain muscles well. It is not a limit. Use any exercise that fits the client's needs, equipment and level.
4. Say nothing about the knowledge and do not mention their plan, unless `knowledge-review: on` is in their `tracker-notes.md` or they ask "review my plan". If they say "turn on plan review", add `knowledge-review: on` to `tracker-notes.md`. "Turn off plan review" removes it.
5. With plan review on (or asked): tell them in 2 or 3 plain lines what is new (from `knowledgeNotes`), compare their current plan with the playbook, list anything that would help (for example a better deload range or a missing hamstring exercise) and ask "Want me to update your plan?" Never change their plan, targets or exercise names without a yes. Logged history keeps its exercise names.
6. If they say yes, save the changed plan as a new dated version, keep the old one, and add a changelog line to `tracker-notes.md`.
7. If you can't reach GitHub, say so in one line and use any copy already saved.
8. Health-check rules still apply to every plan change (pregnancy, postpartum, breastfeeding, medical conditions, injuries).

## 1. See what they have

1. Find their tracker URL in `tracker-notes.md` or `coach-playbook.md`.
2. Read it with the Artifact tool (`action: "read"`) and note where the full page was saved.
3. Run `python3 scripts/check_tracker.py <saved page>` (the script is in this skill's folder). It says which kit version the page is, and whether the page was changed after setup.
4. If it's already the latest version and unchanged, tell them the tracker is up to date and stop (step 0b above still applies).
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

**From kit 3.2.1 (or 3.2, 3.1) to 3.3** (also do the earlier steps below for older trackers)

- Nothing has to change. Every field keeps its meaning. The page writes a few new optional settings on its own: `settings.seenVersion` (the What's new card), `settings.liftOrder` (a saved lift order per plan day), `settings.accent` (the color they pick behind the gear), and `pin` / `chip` flags on `config/foods` items.
- Make sure `config/main.profile` has `name`, `phase`, `phaseStart` (YYYY-MM-DD) and `projectName` (the name of their coach project): Home and the coach read them. Set `label` on `config/baseline` and `config/weightHistory` if they have imported history (what the old app was called).
- Their saved custom features: the page's screens are new, so rebuild each "Custom:" feature on the new layout (see `customizing.md`). Check-in forms, charts, milestones and My Plan now live behind the gear on Progress.

**From kit 3.0 to 3.1**

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

1. Open it with the Artifact tool (`action: "open"`) and check it loads with their data: Home should show their name's page title, the phase and day count under the date, and today's workout card.
2. Update `tracker-notes.md`: the new kit version and today's date, a changelog line "Updated to kit <version>", and their "Custom:" lines (reworded if a feature changed). Update the logging rules in `coach-playbook.md` from `coaching-rules.md` (meal tags, combos, the one rule book).
3. Tell them in 3 lines what changed and one thing to try first, for example: "Tap Start on the Home card. The Workout screen walks you through one set at a time and times your rest."

## What's new in 3.3

- **Home is one card:** today's workout with each lift's target and a Start button, a protein tile, the weigh-in tile, what's due and your streaks. Nothing else.
- **Workout is the focus screen:** one lift and one set at a time, big boxes, set dots, Log set, then a rest clock that keeps running on every tab and buzzes at zero. A trophy and one short cheer for a new best, a finish card at the end. "All lifts" shows the whole session (Full, 45 or 30 minutes, drag to reorder, tap to jump). Tap the day name to swap days; it warns when two hard days for one muscle land back to back.
- **Food is one box:** type, talk or snap a label or meal, then Save. The chips are the foods you log most, by time of day; hold one to pin it.
- **Progress is three numbers** (7-day weight, pace, workouts), the weight trend since your phase started, your main lifts, sets by muscle and your photos. Everything else is behind the gear: plan, targets, check-in forms, full charts, milestones, session length, the accent color.
- **New look:** midnight blue, your own accent color, white cards by day and deep navy at night, flat line icons. The page is 40 percent smaller and loads faster.
- A first-run screen for a brand-new tracker, and a one-time "What's new" card after each update.

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
