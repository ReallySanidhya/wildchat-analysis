from data_loader import load_wildchat, get_random_conversation, split_and_save
from topic_model import label_topics_ollama
from visualizer import render_conversation_ui

# ── Config ──
DOMAIN    = "medical"   # medical, ticket_booking, legal, finance
MIN_TURNS = 3
OLLAMA_URL = "http://localhost:11434/api/generate"  # or your ngrok URL

# ── Load data ──
df_multi = load_wildchat(n=20000)

# ── Split and save to CSV ──
df_train, df_test = split_and_save(df_multi, domain=DOMAIN, min_turns=MIN_TURNS)

# ── Get random conversation and display ──
convo = get_random_conversation(df_multi, domain=DOMAIN, min_turns=MIN_TURNS)

if convo:
    topics = label_topics_ollama(convo)
    render_conversation_ui(convo, DOMAIN, topics)
