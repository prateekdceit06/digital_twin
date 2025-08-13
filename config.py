from dotenv import load_dotenv

def load_env():
    # Ensure env is loaded early and with override behavior (like your original)
    load_dotenv(override=True)
