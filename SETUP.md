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
    # --- KENYA (10) ---
    {"title":"Maasai Mara Safari","location":"Maasai Mara","country":"kenya","category":"safari","description":"Witness the Great Migration with expert Maasai guides.","price_usd":1850,"duration":"5 days","rating":4.9,"badge":"Best Seller","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Amboseli Elephant Watch","location":"Amboseli","country":"kenya","category":"safari","description":"Huge elephant herds with the backdrop of Mt. Kilimanjaro.","price_usd":1200,"duration":"3 days","rating":4.8,"badge":"Nature","image_url":"https://images.unsplash.com/photo-1534190239940-9ba8944ea261?w=600&q=80"},
    {"title":"Diani Beach Escape","location":"Ukunda","country":"kenya","category":"cultural","description":"Turquoise waters and white sands on Kenya's south coast.","price_usd":850,"duration":"4 days","rating":4.7,"badge":"Relaxation","image_url":"https://images.unsplash.com/photo-1589979485637-f98c0c45d1ca?w=600&q=80"},
    {"title":"Lamu Island Cultural Tour","location":"Lamu","country":"kenya","category":"cultural","description":"Step back in time in this ancient Swahili stone town.","price_usd":700,"duration":"3 days","rating":4.6,"badge":"History","image_url":"https://images.unsplash.com/photo-1523301343968-6a6ebf63c672?w=600&q=80"},
    {"title":"Mount Kenya Climbing","location":"Nanyuki","country":"kenya","category":"adventure","description":"Trek to Point Lenana on Africa's second highest peak.","price_usd":1100,"duration":"5 days","rating":4.7,"badge":"Adventure","image_url":"https://images.unsplash.com/photo-1548391350-968f58dedaed?w=600&q=80"},
    {"title":"Hell's Gate Cycling Safari","location":"Naivasha","country":"kenya","category":"adventure","description":"Cycle among zebras and giraffes in a dramatic volcanic gorge.","price_usd":150,"duration":"1 day","rating":4.5,"badge":"Active","image_url":"https://images.unsplash.com/photo-1544198365-f5d60b6d8190?w=600&q=80"},
    {"title":"Samburu Unique Five","location":"Samburu","country":"kenya","category":"safari","description":"Spot the Grevy’s zebra and reticulated giraffe.","price_usd":1400,"duration":"4 days","rating":4.8,"badge":"Wildlife","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Tsavo Red Elephant Expedition","location":"Tsavo","country":"kenya","category":"safari","description":"Explore one of the largest national parks in the world.","price_usd":1300,"duration":"4 days","rating":4.6,"badge":"Expedition","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Nairobi National Park Tour","location":"Nairobi","country":"kenya","category":"safari","description":"The only park in the world within a city capital.","price_usd":120,"duration":"1 day","rating":4.4,"badge":"Urban Safari","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Watamu Marine Snorkeling","location":"Watamu","country":"kenya","category":"adventure","description":"Discover coral reefs and sea turtles in a protected park.","price_usd":300,"duration":"1 day","rating":4.7,"badge":"Water Sports","image_url":"https://images.unsplash.com/photo-1544551763-47a0159f92ad?w=600&q=80"},

    # --- TANZANIA (10) ---
    {"title":"Serengeti Balloon Safari","location":"Serengeti","country":"tanzania","category":"safari","description":"Sunrise views of the endless plains.","price_usd":650,"duration":"1 day","rating":5.0,"badge":"Luxury","image_url":"https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=600&q=80"},
    {"title":"Kilimanjaro Marangu Route","location":"Moshi","country":"tanzania","category":"adventure","description":"The classic 'Coca-Cola' route to Uhuru Peak.","price_usd":2200,"duration":"6 days","rating":4.8,"badge":"Adventure","image_url":"https://images.unsplash.com/photo-1609198093458-e6f5b3a3adca?w=600&q=80"},
    {"title":"Ngorongoro Crater Tour","location":"Ngorongoro","country":"tanzania","category":"safari","description":"Descend into a volcanic caldera teeming with life.","price_usd":950,"duration":"2 days","rating":4.9,"badge":"Natural Wonder","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Zanzibar Spice Island","location":"Stone Town","country":"tanzania","category":"cultural","description":"A sensory journey through cloves, nutmeg, and history.","price_usd":790,"duration":"3 days","rating":4.8,"badge":"Relaxation","image_url":"https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=600&q=80"},
    {"title":"Tarangire Baobab Safari","location":"Tarangire","country":"tanzania","category":"safari","description":"Ancient trees and massive elephant families.","price_usd":800,"duration":"2 days","rating":4.7,"badge":"Photography","image_url":"https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80"},
    {"title":"Selous Boat Safari","location":"Selous","country":"tanzania","category":"safari","description":"Observe hippos and crocs from the water.","price_usd":1400,"duration":"4 days","rating":4.6,"badge":"Off-Path","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Pemba Island Diving","location":"Pemba","country":"tanzania","category":"adventure","description":"World-class reef diving in pristine waters.","price_usd":1500,"duration":"5 days","rating":4.9,"badge":"Pro-Diver","image_url":"https://images.unsplash.com/photo-1544551763-47a0159f92ad?w=600&q=80"},
    {"title":"Lake Manyara Pink Flamingos","location":"Manyara","country":"tanzania","category":"safari","description":"See thousands of flamingos and tree-climbing lions.","price_usd":450,"duration":"1 day","rating":4.5,"badge":"Birding","image_url":"https://images.unsplash.com/photo-1520117009570-f1c548483952?w=600&q=80"},
    {"title":"Maasai Village Cultural Immersion","location":"Arusha","country":"tanzania","category":"cultural","description":"Learn traditional hunting and medicine.","price_usd":200,"duration":"1 day","rating":4.8,"badge":"Authentic","image_url":"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80"},
    {"title":"Mahale Chimpanzee Trek","location":"Kigoma","country":"tanzania","category":"adventure","description":"Trek deep into forests to find wild chimps.","price_usd":3500,"duration":"4 days","rating":5.0,"badge":"Remote","image_url":"https://images.unsplash.com/photo-1540492649367-c8565a571e4b?w=600&q=80"},

    # --- SOUTH AFRICA (10) ---
    {"title":"Kruger Big Five Safari","location":"Nelspruit","country":"southafrica","category":"safari","description":"Premier wildlife viewing in luxury lodges.","price_usd":1650,"duration":"4 days","rating":4.9,"badge":"Wildlife","image_url":"https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80"},
    {"title":"Table Mountain Hike","location":"Cape Town","country":"southafrica","category":"adventure","description":"The best views in the southern hemisphere.","price_usd":100,"duration":"1 day","rating":4.9,"badge":"Views","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Garden Route Drive","location":"Knysna","country":"southafrica","category":"adventure","description":"The most beautiful road trip in Africa.","price_usd":1200,"duration":"6 days","rating":4.8,"badge":"Road Trip","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Robben Island History","location":"Cape Town","country":"southafrica","category":"cultural","description":"Visit the cell of Nelson Mandela.","price_usd":150,"duration":"1 day","rating":4.7,"badge":"History","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Shark Cage Diving","location":"Gansbaai","country":"southafrica","category":"adventure","description":"Get close to Great Whites.","price_usd":350,"duration":"1 day","rating":4.6,"badge":"Adrenaline","image_url":"https://images.unsplash.com/photo-1544551763-47a0159f92ad?w=600&q=80"},
    {"title":"Stellenbosch Wine Tour","location":"Stellenbosch","country":"southafrica","category":"cultural","description":"Sample world-famous Chenin Blanc.","price_usd":250,"duration":"1 day","rating":4.9,"badge":"Gourmet","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Blyde River Canyon","location":"Mpumalanga","country":"southafrica","category":"adventure","description":"Explore the world's third largest canyon.","price_usd":400,"duration":"2 days","rating":4.8,"badge":"Scenic","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Drakensberg Peak Hike","location":"KwaZulu-Natal","country":"southafrica","category":"adventure","description":"Dramatic basalt cliffs and San rock art.","price_usd":600,"duration":"3 days","rating":4.7,"badge":"Hiking","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Soweto Heritage Tour","location":"Johannesburg","country":"southafrica","category":"cultural","description":"The heart of South Africa's struggle.","price_usd":120,"duration":"1 day","rating":4.8,"badge":"Cultural","image_url":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80"},
    {"title":"Addo Elephant Safari","location":"Port Elizabeth","country":"southafrica","category":"safari","description":"Safe and family-friendly wildlife viewing.","price_usd":500,"duration":"2 days","rating":4.6,"badge":"Family","image_url":"https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80"},

    # --- MOROCCO (10) ---
    {"title":"Marrakesh Medina Tour","location":"Marrakesh","country":"morocco","category":"cultural","description":"Wander through spice souks and Jemaa el-Fnaa.","price_usd":150,"duration":"1 day","rating":4.8,"badge":"Classic","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Sahara Overnight Camp","location":"Merzouga","country":"morocco","category":"cultural","description":"Camel trek and luxury tent under the stars.","price_usd":980,"duration":"3 days","rating":4.9,"badge":"Iconic","image_url":"https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=600&q=80"},
    {"title":"Chefchaouen Blue City","location":"Chefchaouen","country":"morocco","category":"cultural","description":"Explore the most Instagrammable streets in Africa.","price_usd":400,"duration":"2 days","rating":4.7,"badge":"Scenic","image_url":"https://images.unsplash.com/photo-1548013146-72479768bbaa?w=600&q=80"},
    {"title":"Atlas Mountain Trek","location":"Imlil","country":"morocco","category":"adventure","description":"Hike to Berber villages in the High Atlas.","price_usd":500,"duration":"3 days","rating":4.6,"badge":"Active","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Fez Ancient Tanneries","location":"Fez","country":"morocco","category":"cultural","description":"Visit the world's oldest medieval leather tanneries.","price_usd":120,"duration":"1 day","rating":4.7,"badge":"Historic","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Essaouira Coastal Escape","location":"Essaouira","country":"morocco","category":"cultural","description":"Windy ramparts and fresh seafood in an artist haven.","price_usd":200,"duration":"1 day","rating":4.8,"badge":"Relaxation","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Ouarzazate Film Studio","location":"Ouarzazate","country":"morocco","category":"cultural","description":"Visit the 'Hollywood of Africa' where Gladiator was filmed.","price_usd":300,"duration":"1 day","rating":4.5,"badge":"Movie Buff","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Ait Ben Haddou Tour","location":"Kasbah","country":"morocco","category":"cultural","description":"UNESCO mud-brick palace architecture.","price_usd":180,"duration":"1 day","rating":4.9,"badge":"Heritage","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Hot Air Balloon over Atlas","location":"Marrakesh","country":"morocco","category":"adventure","description":"Soar over mountain foothills at dawn.","price_usd":350,"duration":"1 day","rating":4.8,"badge":"Luxury","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},
    {"title":"Cooking Class Marrakesh","location":"Marrakesh","country":"morocco","category":"cultural","description":"Master the art of the tagine.","price_usd":80,"duration":"1 day","rating":5.0,"badge":"Gourmet","image_url":"https://images.unsplash.com/photo-1509233725247-49e657c54213?w=600&q=80"},

    # --- EGYPT (10) ---
    {"title":"Great Pyramids Giza","location":"Cairo","country":"egypt","category":"cultural","description":"The last standing Ancient Wonder of the World.","price_usd":150,"duration":"1 day","rating":5.0,"badge":"Bucket List","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Nile Felucca Cruise","location":"Aswan","country":"egypt","category":"cultural","description":"Sail the Nile on a traditional wooden boat.","price_usd":600,"duration":"4 days","rating":4.8,"badge":"Traditional","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Valley of the Kings","location":"Luxor","country":"egypt","category":"cultural","description":"The tomb of Tutankhamun and other pharaohs.","price_usd":250,"duration":"1 day","rating":4.9,"badge":"History","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Red Sea Scuba Diving","location":"Sharm El Sheikh","country":"egypt","category":"adventure","description":"Crystal clear reefs and WWII shipwrecks.","price_usd":800,"duration":"3 days","rating":4.8,"badge":"Diving","image_url":"https://images.unsplash.com/photo-1544551763-47a0159f92ad?w=600&q=80"},
    {"title":"Abu Simbel Temple Tour","location":"Abu Simbel","country":"egypt","category":"cultural","description":"Massive sun temples built by Ramses II.","price_usd":300,"duration":"1 day","rating":4.9,"badge":"Monumental","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"White Desert Camping","location":"Farafra","country":"egypt","category":"adventure","description":"Snow-white chalk formations in the deep desert.","price_usd":450,"duration":"2 days","rating":4.7,"badge":"Otherworldy","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Alexandria Library Tour","location":"Alexandria","country":"egypt","category":"cultural","description":"The intellectual capital of the Mediterranean.","price_usd":100,"duration":"1 day","rating":4.5,"badge":"Modern","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Mount Sinai Pilgrimage","location":"Sinai","country":"egypt","category":"adventure","description":"Sunrise hike to the peak of the Ten Commandments.","price_usd":200,"duration":"1 day","rating":4.6,"badge":"Spirituality","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Egyptian Museum Tour","location":"Cairo","country":"egypt","category":"cultural","description":"The world's largest collection of pharaonic artifacts.","price_usd":80,"duration":"1 day","rating":4.7,"badge":"Museum","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},
    {"title":"Dahab Bedouin Dinner","location":"Dahab","country":"egypt","category":"cultural","description":"Traditional feast in the Sinai mountains.","price_usd":150,"duration":"1 day","rating":4.8,"badge":"Gourmet","image_url":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=600&q=80"},

    # --- BOTSWANA (10) ---
    {"title":"Okavango Delta Mokoro","location":"Maun","country":"botswana","category":"safari","description":"Navigate the delta by traditional dugout canoe.","price_usd":1400,"duration":"3 days","rating":5.0,"badge":"Iconic","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Chobe River Cruise","location":"Kasane","country":"botswana","category":"safari","description":"See thousands of elephants drink at sunset.","price_usd":400,"duration":"2 days","rating":4.9,"badge":"Wildlife","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Makgadikgadi Salt Pans","location":"Nata","country":"botswana","category":"adventure","description":"Stark white landscapes and meerkats.","price_usd":800,"duration":"3 days","rating":4.7,"badge":"Desert","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Khwai Private Reserve","location":"Khwai","country":"botswana","category":"safari","description":"Night drives and high leopard density.","price_usd":2200,"duration":"4 days","rating":4.9,"badge":"Luxury","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Central Kalahari Safari","location":"Kalahari","country":"botswana","category":"safari","description":"Desert-adapted lions and San culture.","price_usd":1800,"duration":"5 days","rating":4.6,"badge":"Remote","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Moremi Game Track","location":"Moremi","country":"botswana","category":"safari","description":"The most diverse wildlife habitat in Africa.","price_usd":1500,"duration":"3 days","rating":4.8,"badge":"Wildlife","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Savuti Bull Elephants","location":"Chobe","country":"botswana","category":"safari","description":"Known for aggressive elephant encounters.","price_usd":2500,"duration":"4 days","rating":4.7,"badge":"Adrenaline","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Linyanti Walking Safari","location":"Linyanti","country":"botswana","category":"adventure","description":"Track game on foot in a private concession.","price_usd":3000,"duration":"4 days","rating":4.9,"badge":"Walking","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Nxai Pan Zebra Migration","location":"Nxai Pan","country":"botswana","category":"safari","description":"Watch the second largest zebra migration.","price_usd":1000,"duration":"3 days","rating":4.5,"badge":"Seasonal","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},
    {"title":"Tsodilo Hills San Art","location":"Tsodilo","country":"botswana","category":"cultural","description":"The 'Louvre of the Desert' ancient rock art.","price_usd":500,"duration":"2 days","rating":4.8,"badge":"Ancient","image_url":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80"},

    # --- RWANDA (10) ---
    {"title":"Gorilla Trekking Volcanoes","location":"Musanze","country":"rwanda","category":"adventure","description":"The world's premium gorilla tracking experience.","price_usd":3100,"duration":"3 days","rating":5.0,"badge":"Rare","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Kigali City Tour","location":"Kigali","country":"rwanda","category":"cultural","description":"Visit the Genocide Memorial and vibrant markets.","price_usd":100,"duration":"1 day","rating":4.9,"badge":"Cleanest City","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Akagera Big Five","location":"Akagera","country":"rwanda","category":"safari","description":"Rwanda's only savanna national park.","price_usd":450,"duration":"2 days","rating":4.6,"badge":"Conservation","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Nyungwe Canopy Walk","location":"Nyungwe","country":"rwanda","category":"adventure","description":"Walk 60m above a prehistoric rainforest.","price_usd":300,"duration":"1 day","rating":4.8,"badge":"Nature","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Lake Kivu Kayaking","location":"Gisenyi","country":"rwanda","category":"adventure","description":"Paddle on Africa's beautiful deep water lake.","price_usd":200,"duration":"1 day","rating":4.7,"badge":"Relaxation","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Chimpanzee Tracking","location":"Cyamudongo","country":"rwanda","category":"adventure","description":"Observe our closest relatives in the wild.","price_usd":600,"duration":"2 days","rating":4.8,"badge":"Primate","image_url":"https://images.unsplash.com/photo-1540492649367-c8565a571e4b?w=600&q=80"},
    {"title":"Golden Monkey Trek","location":"Volcanoes Park","country":"rwanda","category":"adventure","description":"Spot the endangered golden primates.","price_usd":400,"duration":"1 day","rating":4.5,"badge":"Cute","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Musanze Cave Tour","location":"Musanze","country":"rwanda","category":"adventure","description":"Explore 2km of ancient volcanic tunnels.","price_usd":150,"duration":"1 day","rating":4.4,"badge":"Hidden","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Rwanda Coffee Journey","location":"Gisenyi","country":"rwanda","category":"cultural","description":"Pick, roast, and taste high-altitude beans.","price_usd":100,"duration":"1 day","rating":4.9,"badge":"Gourmet","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
    {"title":"Mount Bisoke Climb","location":"Volcanoes Park","country":"rwanda","category":"adventure","description":"Hike to a stunning crater lake summit.","price_usd":350,"duration":"1 day","rating":4.7,"badge":"Challenging","image_url":"https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80"},
]

# Run the update
for t in tours:
    Tour.objects.get_or_create(title=t['title'], defaults=t)

print(f"Update complete. {Tour.objects.count()} total tours in database.")
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