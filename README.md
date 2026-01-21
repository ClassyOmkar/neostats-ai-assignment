# NeoStats AI Booking Agent

So, here's the deal: this isn't just another chatbot. It's a full-stack booking assistant I built to handle appointments without the usual headache of manual scheduling.

It does two main things really well:
1.  **Reads your docs**: You drop a PDF (like your clinic's price list), and it actually *reads* it to answer customer questions. It's not just keyword matching; I set it up to compare facts across multiple files so it doesn't get confused by conflicting info.
2.  **Books the slot**: Once the customer is happy, it locks in the appointment, saves it to a local database, and sends a confirmation email.

### How to Run It

You don't need a complicated Docker setup. I kept it simple so you can spin it up in two minutes.

**1. Get the requirements**
Make sure you're in the project folder and run:
```bash
pip install -r requirements.txt
```

**2. The Secret Sauce**
You'll need a `.env` file for the API keys. Just create one and add your Groq key:
```
GROQ_API_KEY=your_key_here
```

**3. Launch**
Fire it up with Streamlit:
```bash
streamlit run app/main.py
```

### What's Inside?

*   **The Brain**: Uses Llama-3 (via Groq) for the reasoning. It's fast and handles the conversation context without getting lost.
*   **The Memory**: I used FAISS for the vector search. It's running locally, so it's snappy.
*   **The "Guardrails"**: I spent a lot of time breaking this thing. If you upload a blank PDF? It won't crash. If you ask for a price that isn't listed? It won't lie to you. It handles edge cases like a champ.

### Admin Stuff
I built a quick dashboard so you can actually see the bookings.
*   **URL**: Same as the app, just switch the radio button on the left to "Admin Dashboard".
*   **Password**: `admin123` (Hardcoded for this demo, obviously wouldn't do this in prod, but hey, it works for now).

---
*Built for the NeoStats AI Engineer Task.*
