import pandas as pd
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import logging
from mylib.lib import (
    data_split_to_feature_outcome,
    model_execution,
    rank_teams_produce_top_68,
    postseason_result,
    post_season_mapping,
)

logging.basicConfig(
    filename="data_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Loading training and testing datasets.")
cbb = pd.read_csv("../Final_Project_DE/train_data.csv")
cbb24 = pd.read_csv("../Final_Project_DE/test_data.csv")

features = [
    "ADJOE",
    "ADJDE",
    "BARTHAG",
    "EFG_O",
    "EFG_D",
    "TOR",
    "TORD",
    "ORB",
    "DRB",
    "FTR",
    "FTRD",
    "ADJ_T",
    "WAB",
]
outcome = "SEED"
X, y = data_split_to_feature_outcome(cbb, outcome, features)

# Extract the features from cbb24 for prediction
cbb24_seedless = cbb24[features]

cbb24["predicted_seed_score"] = model_execution(cbb24_seedless, X, y)

cbb24 = rank_teams_produce_top_68(cbb24, "predicted_seed_score")


current_data = pd.read_csv("../Final_Project_DE/current_cbb_live_data.csv")

logging.info(
    "Execute model on our current dataset i.e. current_cbb_live_data to get the seeds for 2024-2025 season"
)

current_data_seedless = current_data[features]

current_data["predicted_seed_score"] = model_execution(current_data_seedless, X, y)

current_data = rank_teams_produce_top_68(current_data, "predicted_seed_score")

current_date = datetime.now().strftime("%Y%m%d")
file_name = f"seeding_2025_{current_date}.csv"
current_data[["TEAM", "predicted_seed_with_update"]].sort_values(
    "predicted_seed_with_update"
).dropna(subset=["predicted_seed_with_update"]).to_csv(file_name)

# Preprocess the POSTSEASON column in cbb
cbb = cbb[cbb["POSTSEASON"].notnull()]  # Filter rows with POSTSEASON values
label_encoder = LabelEncoder()
cbb["POSTSEASON_LABEL"] = label_encoder.fit_transform(
    cbb["POSTSEASON"]
)  # Encode POSTSEASON

# Select features for modeling
postseason_features = [
    "ADJOE",
    "ADJDE",
    "BARTHAG",
    "EFG_O",
    "EFG_D",
    "TOR",
    "TORD",
    "ORB",
    "DRB",
    "FTR",
    "FTRD",
    "ADJ_T",
    "WAB",
]

logging.info(
    "Run model to obtain predictions on who will be winning march madness for the 2024-25 season"
)

# Define X and y for training
X_postseason = cbb[postseason_features]
y_postseason = cbb["POSTSEASON_LABEL"]

current_data_seeded = current_data.dropna(subset=["predicted_seed_with_update"])
current_data_seeded["predicted_postseason_label"] = postseason_result(
    X_postseason,
    y_postseason,
    label_encoder,
    current_data,
    "predicted_seed_with_update",
    postseason_features,
)

current_data_seeded["predicted_postseason_description"] = post_season_mapping(
    current_data_seeded, "predicted_postseason_label"
)
current_data_seeded.sort_values("predicted_postseason_label").head(16)

current_date = datetime.now().strftime("%Y%m%d")
file_name = f"cbb25_seeded_{current_date}.csv"
current_data_seeded.to_csv(file_name, index=False)
