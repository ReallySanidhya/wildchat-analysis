import re
import random
import pandas as pd
from datasets import load_dataset

domain_keywords = {
    "ticket_booking": ["ticket", "book", "flight", "train", "seat", "reservation", "cancel"],
    "medical":        ["symptom", "doctor", "diagnosis", "medicine", "pain", "treatment", "hospital"],
    "legal":          ["contract", "lawsuit", "attorney", "court", "legal", "rights", "clause"],
    "finance":        ["loan", "tax", "investment", "bank", "credit", "budget", "insurance"],
}

def load_wildchat(n=20000):
    ds = load_dataset("allenai/WildChat-1M", split="train", streaming=True)
    ds_small = list(ds.take(n))
    df = pd.DataFrame(ds_small)
    df["num_turns"] = df["conversation"].apply(lambda x: len(x) // 2)
    df_multi = df[df["num_turns"] > 2]
    print(f"Loaded {len(df)} rows — {len(df_multi)} multi-turn conversations")
    return df_multi

def is_truly_english(convo):
    text = " ".join(t["content"] for t in convo)
    non_english = re.findall(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', text)
    return len(non_english) / max(len(text), 1) < 0.01

def detect_domain_strict(convo, domain, min_keyword_hits=3):
    text = " ".join(t["content"].lower() for t in convo if t["role"] == "user")
    hits = sum(1 for kw in domain_keywords[domain] if kw in text)
    return hits >= min_keyword_hits

def get_random_conversation(df_multi, domain="medical", min_turns=3):
    matches = []
    for _, row in df_multi.iterrows():
        convo = row["conversation"]
        lang  = row.get("language", "")
        turns = row["num_turns"]
        if lang != "English" or turns < min_turns:
            continue
        if not is_truly_english(convo):
            continue
        if detect_domain_strict(convo, domain, min_keyword_hits=3):
            matches.append(convo)

    print(f"Found {len(matches)} matching conversations for: {domain}")
    if not matches:
        print("No matches — try lowering min_keyword_hits or increasing n")
        return None
    return random.choice(matches)

def split_and_save(df_multi, domain="medical", min_turns=3, test_size=0.2):
    from sklearn.model_selection import train_test_split

    matches = []
    for _, row in df_multi.iterrows():
        convo = row["conversation"]
        lang  = row.get("language", "")
        turns = row["num_turns"]
        if lang != "English" or turns < min_turns:
            continue
        if not is_truly_english(convo):
            continue
        if detect_domain_strict(convo, domain, min_keyword_hits=3):
            matches.append({"conversation": convo, "num_turns": turns, "domain": domain})

    df_domain = pd.DataFrame(matches)

    if df_domain.empty:
        print("No data to split")
        return None, None

    df_train, df_test = train_test_split(df_domain, test_size=test_size, random_state=42)
    df_train.to_csv(f"data/{domain}_train.csv", index=False)
    df_test.to_csv(f"data/{domain}_test.csv",  index=False)

    print(f"Train: {len(df_train)} | Test: {len(df_test)}")
    print(f"Saved to data/{domain}_train.csv and data/{domain}_test.csv")
    return df_train, df_test
