# Team Workflow & GitHub Organization Guide
## Why We Set Things Up This Way & How We Work

---

## PART 1 — WHY A GITHUB ORGANIZATION?

### The Problem With Using a Personal Account
If the project lived on your personal GitHub account (`github.com/YOUR_NAME/savanna-booking-project`):
- The project belongs to **you** — if you leave, the team loses access
- Teammates feel like they're contributing to **your** project, not **the team's**
- Hard to manage permissions — you'd have to add everyone as a collaborator on your personal account
- Looks unprofessional for a real project

### The Solution — A GitHub Organization
We created `savanna-soul-team` as a GitHub Organization because:
- The repo belongs to **the team**, not any one person
- Anyone on the team can be given admin rights
- It looks professional — like a real company repo
- If someone leaves, the project stays intact
- New members can be added easily without touching anyone's personal account

### Think of it Like This
```
GitHub Organization = A Company
    └── Members = Employees
    └── Repos = Company Projects
    └── Each member's Fork = Their personal workspace
```

---

## PART 2 — WHY FORKING INSTEAD OF DIRECT ACCESS?

### What is a Fork?
A fork is your **own personal copy** of the team repo on your GitHub account.

```
savanna-soul-team/savanna-booking-project  ← The official team repo
        ↑
        └── YOUR_NAME/savanna-booking-project     ← Your fork
        └── TEAMMATE_A/savanna-booking-project    ← Teammate A's fork
        └── TEAMMATE_B/savanna-booking-project    ← Teammate B's fork
```

### Why Not Just Give Everyone Direct Push Access?
If everyone pushed directly to `savanna-soul-team/savanna-booking-project`:
- Someone could push broken code and break it for everyone
- No review process — mistakes go straight to the main codebase
- Hard to track who changed what and why
- Conflicts when two people edit the same file

### Why Forking Works Better
- Each person works in their own copy — **you can't break anyone else's work**
- Changes only go to the team repo after a **Pull Request is reviewed**
- Every change has a paper trail — who wrote it, why, when
- If your code breaks, only your fork is affected — the team repo stays clean

---

## PART 3 — THE TWO REMOTES EXPLAINED

When you clone your fork you have two remotes:

```bash
git remote -v

origin    https://github.com/YOUR_NAME/savanna-booking-project.git
upstream  https://github.com/savanna-soul-team/savanna-booking-project.git
```

### `origin` — Your Fork
- This is YOUR copy on GitHub
- You push to this freely — no one reviews it
- Only you control it
- Think of it as your **personal workspace**

### `upstream` — The Team Repo
- This is the official team project
- You NEVER push directly to this
- You only PULL from this (to get updates)
- Changes only get here through Pull Requests
- Think of it as the **finished, reviewed codebase**

### The Flow in Plain English
```
upstream (team repo)
    ↓  git fetch upstream (get latest)
your local main
    ↓  git checkout -b feature/my-feature (create branch)
your feature branch
    ↓  write code, git add, git commit
your feature branch
    ↓  git push origin feature/my-feature (push to YOUR fork)
your fork on GitHub
    ↓  Open Pull Request → savanna-soul-team repo
team repo (after review and merge)
```

---

## PART 4 — BRANCHES — WHY WE NEVER WORK ON MAIN

### What is a Branch?
A branch is an independent copy of the code where you can make changes without affecting anything else.

```
main ─────────────────────────────────────── (always stable)
         │
         ├── feature/mpesa-refund ────────── (teammate A working)
         │
         ├── feature/tour-search ─────────── (teammate B working)
         │
         └── fix/login-redirect ──────────── (you fixing a bug)
```

### Why Never Work on `main`?
- `main` is the **stable, working version** of the project
- If you work directly on `main` and break something, everyone is affected
- Branches let multiple people work on different features **at the same time** without interfering

### Branch Naming Convention
```
feature/what-you-are-building    → new functionality
fix/what-you-are-fixing          → bug fixes
ui/what-you-are-styling          → frontend/template changes
docs/what-you-are-documenting    → documentation
refactor/what-you-are-cleaning   → code cleanup
```

---

## PART 5 — PULL REQUESTS — THE REVIEW PROCESS

### What is a Pull Request (PR)?
A Pull Request is a formal request to merge your branch into the team repo's `main` branch.

### Why Review Before Merging?
- Catches bugs before they reach the main codebase
- Ensures code quality and consistency
- Spreads knowledge — everyone learns from each other's code
- Creates a permanent record of every change and why it was made

### The PR Process
```
1. You finish a feature on your branch
2. Push it to your fork
3. Go to GitHub → your fork → "Contribute" → "Open Pull Request"
4. Write a clear description of what you changed and why
5. Tag a teammate to review
6. Teammate reviews, leaves comments or approves
7. You fix any issues they raise
8. Teammate (or you) clicks "Merge Pull Request"
9. Your code is now in the official team repo
10. Everyone pulls the update into their forks
```

### What Makes a Good PR?
- Small and focused — one feature or fix per PR
- Clear title: `feat: add M-Pesa refund flow`
- Description explains WHY not just what
- No broken tests or `python manage.py check` errors

---

## PART 6 — THE DAILY WORKFLOW EXPLAINED

### Morning — Start of Work
```bash
# 1. Make sure you're on main
git checkout main

# 2. Get the latest from the team repo
git fetch upstream

# 3. Merge any new changes into your local main
git merge upstream/main

# 4. Update your fork's main on GitHub
git push origin main
```
> **Why?** If someone merged a PR yesterday, you need those changes before
> you start today. Otherwise you'll be working on outdated code.

### During Work — Feature Branch
```bash
# 1. Create a branch for what you're building
git checkout -b feature/tour-search

# 2. Write your code...

# 3. Stage your changes
git add .

# 4. Commit with a clear message
git commit -m "feat: add search bar to tour list page"

# 5. Push to YOUR fork
git push origin feature/tour-search
```

### End of Work — Submit for Review
```
1. Go to github.com/YOUR_NAME/savanna-booking-project
2. Click "Contribute" → "Open Pull Request"
3. Set base: savanna-soul-team/savanna-booking-project ← main
4. Write description
5. Tag reviewer
6. Submit
```

### After Your PR is Merged
```bash
# Switch back to main
git checkout main

# Pull the merged changes
git fetch upstream
git merge upstream/main
git push origin main

# Delete your old branch (it's merged, no longer needed)
git branch -d feature/tour-search
```

---

## PART 7 — WHO OWNS WHAT (TEAM ROLES)

| Role | Responsibility |
|------|---------------|
| **Repo Admin (you)** | Manages org, reviews and merges PRs, handles deployment |
| **Developer** | Works on features in their fork, submits PRs |
| **Everyone** | Reviews each other's PRs, writes clear commit messages |

### Who Can Merge PRs?
- The repo admin always can
- You can give other trusted teammates merge rights in the org settings
- The person who wrote the code should NOT merge their own PR (defeats the purpose of review)

---

## PART 8 — SUMMARY — THE BIG PICTURE

```
WHY AN ORG?
→ Project belongs to the team, not one person.
   Professional, manageable, scalable.

WHY FORKS?
→ Everyone has their own safe workspace.
   Can't break each other's code.

WHY BRANCHES?
→ Work on multiple features simultaneously.
   Main always stays stable and working.

WHY PULL REQUESTS?
→ Code review catches bugs before they reach main.
   Creates a history of every decision made.

WHY TWO REMOTES (origin + upstream)?
→ origin = your personal fork (push freely)
   upstream = team repo (only pull, never push directly)
```

---

## Quick Reference Card

```bash
# Start of day
git fetch upstream && git merge upstream/main && git push origin main

# Start a feature
git checkout -b feature/your-feature

# Save work
git add . && git commit -m "feat: describe change"

# Push to your fork
git push origin feature/your-feature

# Sync with team after someone's PR is merged
git fetch upstream && git checkout main && git merge upstream/main
```