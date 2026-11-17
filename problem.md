# The problem
Making schedules for many employees is difficult and time consuming for managers, and it's a task that doesn't need their main expertise. The app is meant for any business with hourly shift workers. A pizza delivery store (based on my experience at Papa John's) is the main example used here. There, the manager has to juggle everyone's availability, keep every shift covered with the right roles, and give people the hours they need, all from conflicts that come in by word of mouth or email.

## Who has it
- **The manager** who makes the schedule. They're the main user.
- **Employees** (insiders, drivers and shift leads) who get bad schedules or the wrong hours when the manager misses something.

## What it costs them
- **Manager:** 3-5 extra hours a week, plus time taken from other managers they have to talk with. That's roughly $100-250 in opportunity cost, plus the stress of keeping track of many people's schedules.
- **Employees:** missed family events or other important things, and not getting the hours they want or need.

## How they handle it today
- Employees tell the manager their conflicts in person or by email. Conflicts can be a standing pattern (for example, "never Tuesdays") or a one-time request (common for part-time employees).
- "Prefer not to" times exist, but in practice they become yes or no: the person either works or doesn't.
- The manager builds the schedule on a spreadsheet or in company software, then sends it out by email. Some stores also print it and post it.

## Why that falls short
- Conflicts arrive in scattered places (conversations, emails, notes), so the manager can miss one.
- An employee can get scheduled during a conflict and miss a family event or something important.
- Employees may not get the hours they want or need because a manager missed an email or note from them.

## How the app works
1. **Employees log in and enter their own conflicts**, either standing patterns or one-time requests. Each conflict is a hard "can't work."
2. **Deadline:** conflicts are due the day before the schedule is made. Late requests aren't used to build the schedule. The app flags them so the manager can handle them personally, outside the app.
3. **The app drafts the schedule** using these rules, in priority order:
   1. Never schedule anyone during a conflict entered on time.
   2. Every employee appears on the schedule at least once.
   3. Each shift is fully staffed (pizza store example: usually 4-5 people, up to about 10 on busy weekends).
   4. Give everyone the hours they need.
   5. Then give extra hours to employees who asked for them.

   Role rules like these are specific to the pizza store example and aren't part of the first test:
   - Every shift has a shift lead.
   - Insiders can't fill driver spots. Some drivers can fill insider spots.
4. **If a shift can't be filled without breaking a rule,** the app leaves the spot empty and flags it for the manager. It never schedules over a conflict to fill a gap.
5. **The manager always has final say.** They can edit the draft before publishing it.
6. **Employees see the final schedule** in the app and by email, with a printable version for stores that post one.

## How they would know it is solved
- Employees know their conflicts are on record with the company and that they won't be scheduled during them.
- No published schedule puts anyone on a shift during a conflict they entered.
- Every employee appears on the schedule at least once, and every open spot is either filled or flagged.
- Late conflicts are flagged for the manager, not silently ignored.
- The manager spends less time building the schedule than the current 3-5 hours a week.

## Open questions
- About how many employees does a typical store schedule?
- Who sets how many people each shift needs, and is that entered every week or once?
- How does an employee say how many hours they *need* versus extra hours they *want*?
- Are role rules (shift lead, driver/insider) a setting each business can turn on, or left out entirely?
