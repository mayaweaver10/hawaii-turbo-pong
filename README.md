# Hawaii Turbo Pong

A tropical, computer-versus-computer Pong game hosted with Streamlit. Watch
the computers play, change the ball speed and AI skill, or restart the match.
The animation runs in your browser; no API keys or external assets are needed.

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
