import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from pygam import LinearGAM, s
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import boto3
from io import StringIO
import pandas as pd
import requests
from bs4 import BeautifulSoup



logging.basicConfig(
    filename='data_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def data_split_to_feature_outcome (df, outcome, features):

    logging.info("Filtering rows with non-null SEED values.")
    df_model = df[df[outcome].notnull()]
    df_model[outcome] = df_model[outcome].astype(int)

    logging.info(f"Selected features: {features}.")
    X = df_model[features]
    y = df_model[outcome]
    return X, y

def model_execution(df, X, y):

    logging.info("Splitting data into training and testing sets.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logging.info("Scaling features using StandardScaler.")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    df_scaled = scaler.transform(df)

    logging.info("Fitting the GAM model.")
    gam = LinearGAM(s(0) + s(1) + s(2) + s(3) + s(4) + s(5) + s(6) + 
                    s(7) + s(8) + s(9) + s(10) + s(11) + s(12)).fit(X_train, y_train)

    logging.info("Predicting on test data.")
    gam.gridsearch(X_train, y_train, progress=True)
    y_pred = gam.predict(X_test)
    y_pred_rounded = np.round(y_pred).clip(1, 16)  # Clip predictions to valid seed range
    mae = mean_absolute_error(y_test, y_pred_rounded)
    print(f"Mean Absolute Error (MAE): {mae}")

    logging.info("Predicting seeds for cbb24.")
    df_predictions = gam.predict(df_scaled)
    return df_predictions

def rank_teams_produce_top_68(df, score):
     #Rank teams based on predicted seed scores
    df['rank'] = df[score].rank(method='min', ascending=True)

    # Assign seeds to top 68 teams
    df['predicted_seed_with_update'] = np.nan  # Initialize with NaN
    top_68 = df.nsmallest(68, score)  # Select top 68 teams

    # Create seed values for 68 teams
    seed_values = []
    for seed in range(1, 17):
        if seed == 11 or seed == 16:
            seed_values.extend([seed] * 6)  # 6 teams for seeds 11 and 16
        else:
            seed_values.extend([seed] * 4)  # 4 teams for other seeds

    logging.info("Updating seed assignments in the main DataFrame.")
    top_68['predicted_seed_with_update'] = seed_values

    # Update the main DataFrame with the seeded teams
    df.update(top_68) 
    return df.sort_values(by='predicted_seed_with_update')    

def postseason_result (X,y,label_encoder, df, col, features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logging.info("Training Random Forest Classifier.")
    rf_classifier = RandomForestClassifier(random_state=42, n_estimators=100)
    rf_classifier.fit(X_train, y_train)

    logging.info("Evaluating model performance on the test set.")
    y_pred = rf_classifier.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    logging.info("Applying the model to current data.")
    df_seeded = df.dropna(subset=[col])

    X_current_data = df_seeded[features]
    postseason_probs = rf_classifier.predict_proba(X_current_data)

    # Define the number of teams per label
    label_counts = {
        'Champion': 1,
        'Runner-Up': 1,
        'Final Four': 2,
        'Elite Eight': 4,
        'Sweet Sixteen': 8,
        'Round of 32': 16,
        'Round of 64': 32
    }

    logging.info("Assigning labels systematically.")
    num_labels = len(label_counts)
    assigned_labels = np.full(len(df_seeded), num_labels - 1)  # Default to lowest label
    remaining_teams = list(range(len(df_seeded)))

    # Loop through each label, starting with the highest rank (Champion)
    for label_idx, (label, count) in enumerate(label_counts.items()):
        # Select top teams based on probabilities for the current label
        if len(remaining_teams) == 0:
            break
        label_probs = postseason_probs[remaining_teams, label_idx]
        top_indices = np.argsort(label_probs)[-count:]  # Get indices of top `count` teams
        top_team_indices = [remaining_teams[i] for i in top_indices]  # Map back to original indices
        for i in top_team_indices:
            assigned_labels[i] = label_idx
        remaining_teams = [team for team in remaining_teams if team not in top_team_indices]

    return assigned_labels

def post_season_mapping (df, col) :
    postseason_mapping = {
        0: 'Winner',
        1: 'Runner-Up',
        2: 'Final Four',
        3: 'Elite Eight',
        4: 'Sweet Sixteen',
        5: 'Round of 32',
        6: 'Round of 64'
    }
    logging.info("Mapping assigned labels back to POSTSEASON names.")
    return df[col].map(postseason_mapping)

# S3 Configuration
s3 = boto3.client("s3")
bucket_name = "cbb-data-engg"
input_prefix = "Final_Project_DE/archive/"
output_prefix = "Final_Project_DE/"


def upload_to_s3(local_path, bucket, s3_key):
    """Upload a local file to S3."""
    try:
        s3.upload_file(local_path, bucket, s3_key)
        logging.info(f"Uploaded {local_path} to S3 as {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading {local_path} to S3: {e}")
        raise e

def read_s3_csv(bucket, key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))
    except Exception as e:
        logging.error(f"Error reading {key} from S3: {e}")
        raise

def write_s3_csv(df, bucket, key):
    """Write a Pandas DataFrame to S3 as a CSV file."""
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    except Exception as e:
        logging.error(f"Error writing {key} to S3: {e}")
        raise

def extract_bart_torvik_data():
    """Extract, transform, and upload Bart Torvik data to S3."""
    logging.info("Extracting data from Bart Torvik.")
    url = "https://www.barttorvik.com/"
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    # Convert to DataFrame and transform
    df = pd.DataFrame(data)
    df = df.dropna(how="all").reset_index(drop=True)

    df.columns = [
        "RK",
        "TEAM",
        "CONF",
        "G",
        "REC",
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
        "2P_O",
        "2P_D",
        "3P_O",
        "3P_D",
        "3PR",
        "3PRD",
        "ADJ_T",
        "WAB",
    ]
    df = df[
        [
            "TEAM",
            "CONF",
            "G",
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
            "2P_O",
            "2P_D",
            "3P_O",
            "3P_D",
            "ADJ_T",
            "WAB",
        ]
    ]
    return df

    
