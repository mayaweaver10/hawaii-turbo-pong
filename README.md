# Hawaii Turbo Pong

A tropical Pong game hosted with Streamlit. You control the left paddle and
play against the computer on the right. Change the ball speed and computer
skill, or restart the match.
The animation runs in your browser; no API keys or external assets are needed.

## How to play

- Select **Start game** when you are ready.
- **Keyboard:** click the court, then hold **W/S** or the **up/down arrows**.
- **Mouse:** move the pointer up and down over the court.
- **Touch:** drag your finger up and down on the court.
- Select **Restart** to reset both scores and begin a new match.

## Run locally

Use Python 3.12:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Save `app.py` and `requirements.txt` in the root of this GitHub repository.
2. Sign in at https://share.streamlit.io/ and select **Create app**.
3. Choose repository `mayaweaver10/hawaii-turbo-pong`, branch `main`, and
   main file path `app.py`.
4. In advanced settings, select Python 3.12 if a Python version is requested.
5. Click **Deploy**. Streamlit installs the requirements and gives you a
   shareable website address.

Each visitor has their own match. Refreshing the page starts a new game.
