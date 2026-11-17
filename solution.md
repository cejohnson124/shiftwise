# The solution

## In one sentence
Employees enter their own conflicts in an app so they don't get bad schedules, and the app builds the schedule around those conflicts so managers save time.

## What someone does with it

### Employee (entering a conflict)
1. Opens the app on their phone and logs in with their company login. The manager has to add them first.
2. Goes to the area for next week's conflicts.
3. Fills in the conflict: date, start and end time (or whole day), whether it repeats (with an optional end date), and a reason.
4. Taps submit and sees a "submitted" message.
5. Gets asked whether they want to submit another conflict. If yes, it returns to the form. If no, they're done.
6. Before the deadline (the day before the schedule is made), gets a reminder to enter conflicts.
7. When the schedule is published, gets a notification and can see it in the app.

### Manager (making the schedule)
1. Each week, enters the shifts: times, and how many people each shift needs.
2. Adds any new employees and sets each employee's needed hours (and extra hours wanted, if any).
3. After the conflict deadline, receives all of the conflicts and reviews them.
4. Taps **Generate schedule**. The app builds a draft following the rules in problem.md.
5. Checks the flag list at the top (late conflicts and unfilled spots), which is also emailed to them.
6. Drags names between time slots to make changes.
7. Publishes the schedule. Employees get notified and can see it in the app and by email.

## The screens

### Employee screens
- **Home / Schedule:** shows the current week's schedule for the whole team, plus the area to submit next week's conflicts, so everything is in one place.
- **Add conflict form:** date, start time, end time, a whole-day option, a repeats option with an optional end date, and a reason. Tapping **Submit** shows a "submitted" message, then asks "Submit another conflict?"
- **My conflicts tab:** a list of the employee's own conflicts. Tapping one lets them **edit** or **delete** it.

### Manager screens
- **Employees:** add employees (who then log in with their company login) and set each one's needed hours and extra hours wanted.
- **Shifts setup:** enter each shift's times and how many people it needs. Done every week.
- **Conflict review:** all submitted conflicts for the week. New repeating conflicts need approval once. After that they apply automatically every week until their end date. Tapping **Generate schedule** builds the draft.
- **Schedule editor:** the draft schedule with a **flag list at the top** showing late conflicts and unfilled spots. The manager drags names between time slots to make changes, then taps **Publish**.

## What it does not do
- Show employees their coworkers' conflicts. Employees can see coworkers' *shifts*, just not their conflicts.
- Shift swaps between employees.
- Call-outs after the schedule is published.

## Where the information comes from

**The employee types in:**
- Their conflicts: date, times or whole day, whether it repeats, an end date, and a reason.

**The manager types in:**
- Employees and their needed hours (and extra hours wanted).
- Each week's shifts and how many people each needs.
- Edits to the draft schedule.

**The app already knows:**
- Repeating conflicts. Once entered and approved, they apply automatically every week until their end date, so the employee doesn't re-enter them.
- The conflict deadline. Anything submitted after it gets flagged for the manager instead of being used to build the schedule.
- Employee logins, through the company login.

## Open questions
- Can the manager reject a one-time conflict during review? If so, does the employee get told?
- Who enters the extra hours an employee wants: the manager (assumed for now) or the employee?
