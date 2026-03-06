# 🌍 Savanna Booking Project — Teammate Setup Guide

## Step 1 — What You Need First
Before anything else, make sure you have these installed:

**Windows:**
- [Python 3.10+](https://python.org/downloads) — ✅ check **Add to PATH** during install
- [Git](https://git-scm.com/download/win)
- [VSCode](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/)

**Linux Mint:**
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv git -y
```

---

## Step 2 — Create a GitHub Account
If you don't have one go to **https://github.com** and sign up.

Once done, **send your GitHub username to [YOUR NAME]** so you can be added to the team.

---

## Step 3 — Accept the Organization Invite
You'll get an email from GitHub inviting you to join **savanna-soul-team**.
Click **Join savanna-soul-team** in the email.

---

## Step 4 — Fork the Repo
1. Go to **https://github.com/savanna-soul-team/savanna-booking-project**
2. Click the **Fork** button (top right)
3. Under **Owner** select **your own GitHub account**
4. Click **Create fork**

You now have your own copy at:
```
https://github.com/YOUR_USERNAME/savanna-booking-project
```

---

## Step 5 — Clone Your Fork

**Windows (PowerShell):**
```powershell
cd Desktop
git clone https://github.com/YOUR_USERNAME/savanna-booking-project.git
cd savanna-booking-project
code .
```

**Linux Mint:**
```bash
cd Desktop
git clone https://github.com/YOUR_USERNAME/savanna-booking-project.git
cd savanna-booking-project
code .
```

---

## Step 6 — Add the Team Repo as Upstream
This keeps your fork connected to the main project:
```bash
git remote add upstream https://github.com/savanna-soul-team/savanna-booking-project.git
git remote -v
```

You should see both `origin` (your fork) and `upstream` (team repo).

---

## Step 7 — Set Up Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```
> If you get a permissions error run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Linux Mint:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## Step 8 — Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Step 9 — Set Up Environment Variables

**Windows:**
```powershell
copy .env.example .env
```

**Linux Mint:**
```bash
cp .env.example .env
```

Open `.env` and fill in:
```env
SECRET_KEY=ask-team-lead-for-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MPESA_CONSUMER_KEY=get-from-developer.safaricom.co.ke
MPESA_CONSUMER_SECRET=get-from-developer.safaricom.co.ke
MPESA_SHORTCODE=174379
MPESA_PASSKEY=get-from-developer.safaricom.co.ke
MPESA_ENV=sandbox
MPESA_CALLBACK_URL=https://REPLACE_WITH_YOUR_NGROK_URL/mpesa/callback/
```

> **Note:** Each person needs their own Daraja sandbox keys from
> **https://developer.safaricom.co.ke** — it's free to register.

---

## Step 10 — Run Migrations & Create Admin Account
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Step 11 — Seed the Database with Tours
```bash
python manage.py shell
```

Then paste this entire block:
```python
from core.models import Tour

tours = [
    {"title":"Maasai Mara Safari","location":"Nairobi, Kenya","country":"kenya","category":"safari","description":"Witness the Great Migration across golden savanna plains with expert Maasai guides.","price_usd":1850,"duration":"5 days","rating":4.9,"badge":"Best Seller","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Kilimanjaro Trek","location":"Tanzania","country":"tanzania","category":"adventure","description":"Summit Africa's highest peak through cloud forests and glacial valleys.","price_usd":2400,"duration":"8 days","rating":4.8,"badge":"Adventure","image_url":"https://images.unsplash.com/photo-1609198093458-e6f5b3a3adca?w=600&q=80"},
    {"title":"Sahara Desert Journey","location":"Morocco","country":"morocco","category":"cultural","description":"Sleep under a billion stars and ride camels through ancient golden dunes.","price_usd":980,"duration":"3 days","rating":4.9,"badge":"Iconic","image_url":"https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=600&q=80"},
    {"title":"Cape Winelands & Coast","location":"South Africa","country":"southafrica","category":"cultural","description":"Explore world-class vineyards, whale-watching coast and Cape Town's vibrant culture.","price_usd":1200,"duration":"4 days","rating":4.7,"badge":"Cultural","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Gorilla Trekking","location":"Uganda","country":"uganda","category":"adventure","description":"A face-to-face encounter with mountain gorillas in Bwindi Impenetrable Forest.","price_usd":3100,"duration":"3 days","rating":5.0,"badge":"Rare","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Serengeti Hot Air Balloon","location":"Tanzania","country":"tanzania","category":"safari","description":"Float above the Serengeti at sunrise — lions, elephants, and endless plains below.","price_usd":650,"duration":"1 day","rating":5.0,"badge":"Luxury","image_url":"https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=600&q=80"},
    {"title":"Zanzibar Spice & Sea","location":"Tanzania","country":"tanzania","category":"cultural","description":"Explore spice plantations, Stone Town's ancient alleys, and turquoise waters.","price_usd":790,"duration":"3 days","rating":4.8,"badge":"Relaxation","image_url":"https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=600&q=80"},
    {"title":"Kruger Park Safari","location":"South Africa","country":"southafrica","category":"safari","description":"Spot the Big Five on private game reserves in one of Africa's finest parks.","price_usd":1650,"duration":"4 days","rating":4.9,"badge":"Wildlife","image_url":"https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80"},
]

for t in tours:
    Tour.objects.get_or_create(title=t['title'], defaults=t)

print(f"Done. {Tour.objects.count()} tours in database.")
```

Then:
```python
exit()
```

---

## Step 12 — Run the Server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser. 🎉

---

## Step 13 — PyCharm Users Only
1. File → Open → select the `savanna-booking-project` folder
2. File → Settings → Project → Python Interpreter → Add → Existing → point to `venv`
3. File → Settings → Languages & Frameworks → Django → Enable → set `savanna_booking/settings.py`
4. File → Settings → Plugins → search `EnvFile` → Install
5. Run → Edit Configurations → Django Server → EnvFile tab → add `.env`

---

## Daily Git Workflow

```bash
# 1. Sync with team before starting work
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 2. Create a branch for your feature
git checkout -b feature/your-feature-name

# 3. Work, then commit
git add .
git commit -m "feat: describe what you did"
git push origin feature/your-feature-name

# 4. Go to GitHub → your fork → Contribute → Open Pull Request
```

---

## Getting Daraja Sandbox Keys (for M-Pesa testing)
1. Go to **https://developer.safaricom.co.ke** and create a free account
2. Create a new App → select **Lipa Na M-Pesa Sandbox**
3. Copy **Consumer Key** and **Consumer Secret** → paste into your `.env`
4. Go to **APIs → Lipa Na M-Pesa** to get your **Passkey**
5. Sandbox shortcode is always `174379`
6. Test phone number: `254708374149` · Test PIN: `1234`

---

## Need ngrok for M-Pesa callbacks?
1. Download from **https://ngrok.com/download**
2. In a second terminal run: `ngrok http 8000`
3. Copy the `https://xxxx.ngrok.io` URL
4. Paste it into your `.env` as `MPESA_CALLBACK_URL=https://xxxx.ngrok.io/mpesa/callback/`
5. Restart the Django server

---

## Questions?
Contact anyone in the group for info or open an issue on the repo.