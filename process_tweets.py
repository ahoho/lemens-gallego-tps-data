#%%
import pandas as pd
from pathlib import Path

# %%
data_dir = Path("./tweets")
tweets = pd.read_csv(data_dir / "test_set_tweet_info.csv")
tweet_labels = pd.read_csv(data_dir / "USTLR1_human_positions.csv")

# %%
# aggregate the labels--- create a list "label_set" and a mean "label"
labels_agg = tweet_labels.groupby("id", as_index=False).agg(
    label_set=("pos_human", lambda x: x.dropna().tolist()),
    label_mean=("pos_human", "mean"),
    label_std=("pos_human", "std"),
    n_annotators=("pos_human", "count"),
)

# join
tweets = tweets.merge(labels_agg, how="left", on="id")
tweets = tweets.dropna(subset=["label_mean"])

#%% make a 1-9 scale
tweets["label_ordinal"] = (tweets["label_mean"] / 10).round().astype(int)

#%% store
tweets.to_json(data_dir / "processed/tweets.jsonl", orient="records", lines=True)
# %%
