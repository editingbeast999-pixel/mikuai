# ☁️ Miku AI Cloud Deployment Guide

Aapne poocha tha ki **"Local Hosting ki jagah URL kaise banaye"** aur **"PC Band hone par kaise chalaye"**. Iska solution hai **Cloud Hosting**.

Hum is app ko **Render** (Free Cloud Platform) par daalenge. Isse aapko ek URL milega (e.g., `https://miku-ai.onrender.com`) jo duniya mein kahin se bhi chalega, wo bhi **PC Band** hone par bhi!

---

## 🚀 Step 1: GitHub Account Banayein
Deployment ke liye code ko pehle online save karna padta hai.
1.  [GitHub.com](https://github.com/) par account banayein (agar nahi hai).
2.  Apne PC par is folder ko GitHub par upload karein (Repo banayein).
    *   *Note: Agar aapko Git use karna nahi aata, toh aap "GitHub Desktop" app download karke drag-drop kar sakte hain.*

## ☁️ Step 2: Render par Account Banayein
1.  [Render.com](https://render.com/) par jayein.
2.  "Get Started for Free" click karein.
3.  GitHub se login karein.

## 🔗 Step 3: Web Service Create Karein
Render dashboard mein:
1.  **"New +"** button dabayein -> select **"Web Service"**.
2.  Apni GitHub repository select karein (jo Step 1 mein banayi thi).
3.  **Settings:**
    *   **Name:** `miku-voice-assistant` (ya jo aap chahein)
    *   **Region:** Singapore (India ke paas)
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn --worker-class eventlet -w 1 main:app`
4.  **Environment Variables (Bahut Zaroori):**
    *   Niche scroll karein aur "Advanced" ya "Environment Variables" dhundhein.
    *   Add Variable:
        *   Key: `GEMINI_API_KEY`
        *   Value: `AIzaSyARIdPFP1Xp30J0nTUxH7pqEcZeSIIojQU` (Aapki Key)
5.  **"Create Web Service"** dabayein.

## ⏳ Step 4: Wait & Enjoy
Render ab aapka app build karega (2-3 minute lagenge).
Jab complete ho jayega, wo aapko upar ek URL dega (e.g., `https://miku-voice.onrender.com`).

**Yeh URL ab aap Phone, Laptop, kahin bhi chala sakte hain, bhale hi aapka PC band ho!** 🎉

---

### 💡 Shortcut (Fast URL - PC ON Only)
Agar aap cloud setup nahi karna chahte aur bas abhi ke liye fast URL chahiye:
1.  [Ngrok](https://ngrok.com/download) download karein.
2.  Terminal mein likhein: `ngrok http 5000`
3.  Wo aapko ek `https://...` link dega.
4.  Yeh link phone pe chalega aur Mic bhi badhiya kaam karega!
    *   *Condition: Iske liye PC ON rehna chahiye.*
