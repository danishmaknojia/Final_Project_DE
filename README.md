# NCAA Basketball Tournament Prediction Project

## Algorithmic Approach

This repository contains two interconnected projects focused on predicting NCAA basketball tournament outcomes:

1. **Tournament Seed Prediction** - Predicts NCAA tournament seeds using machine learning models trained on historical data and produces live updates.
2. **Postseason Outcome Prediction** - Assigns predicted postseason outcomes (e.g., Champion, Runner-Up) to NCAA teams based on performance metrics.

### **1. NCAA Basketball Tournament Seed Prediction**

#### **Overview**
We initially aim to predict NCAA basketball tournament seeds using historical data and team performance metrics. It dynamically ranks teams and predicts their seeds for our live dataset.

#### **Features**
- **Historical Data Modeling:** Trains a Generalized Additive Model (GAM) on past team metrics and their tournament seeds.
- **Performance Evaluation:** Validates the model using Mean Absolute Error (MAE).
- **Dynamic Team Ranking:** Assigns NCAA tournament seeds to the top 68 teams based on their performance scores.

#### **Data Sources**
- **Historical Data:**
  - `train_data.csv` (for training).
  - `test_data.csv` (for validation).
- **Live Data:** Scraped from Bart Torvik, containing up-to-date team performance metrics.

### How It Works

1. **Prepare the Data:**
   - The first step is to load the datasets. We begin with the `train_data.csv` file, which contains historical team performance data up until the 2023 season. This data includes various metrics like offensive and defensive efficiency (e.g., ADJOE, ADJDE), rebound percentages, turnover rates, and more, that are essential for evaluating team performance.
   - The `test_data.csv` file contains data for the 2023-2024 season. This will serve as the validation dataset to assess how well our model performs on unseen data, simulating how the model will perform for the current and future seasons.

2. **Train the Model:**
   - We use the historical data (`train_data.csv`) to train the Generalized Additive Model (GAM). The GAM learns the relationship between the team performance metrics and the corresponding tournament seeds. 
   - The training data is split into training and validation subsets, and the model is trained using the training data. This enables the model to understand how various features (such as team metrics) influence the seed assignments in the NCAA tournament. 

3. **Validate the Model:**
   - Once the model is trained, we validate it using the `test_data.csv` file, which contains data from the 2023-2024 season. This step is crucial because it provides a way to assess how well the model generalizes to unseen data and makes predictions for new tournament seasons.
   - During validation, the model predicts the NCAA tournament seeds for the teams in the 2023-2024 season. By comparing these predicted seeds with the actual seeds assigned in the 2023-2024 tournament, we can evaluate the accuracy of the model using metrics like Mean Absolute Error (MAE).

4. **Predict Seeds for 2024-2025 Season:**
   - After confirming that the model performs well on the 2023-2024 validation set and is accurate enough, we use the trained and validated model to predict the seeds for the upcoming 2024-2025 season.
   - To do this, we scrape live team performance data for the 2024-2025 season from sources like Bart Torvik. The scraped data includes current metrics such as offensive and defensive ratings, rebound and turnover percentages, etc. These features are used as input for the trained model.
   - The model then generates predictions for the top 68 teams in the 2024-2025 season, assigning them the predicted NCAA tournament seeds based on their performance metrics.

5. **Evaluate Accuracy:**
   - After making predictions for the 2024-2025 season, we evaluate the model's performance by checking how closely the predicted seeds align with actual outcomes (based on ESPN projections).

6. **Dynamic Updates:**
   - In addition to initial predictions, the model can be continuously updated with live data throughout the 2024-2025 season. As new team performance data is scraped, the model can generate updated predictions for the NCAA tournament seeds, allowing real-time forecasting for the ongoing season.

This process ensures that the model first learns from historical data, is validated using recent season data, and is then capable of making accurate predictions for the upcoming season. The model is built to be updated dynamically, providing reliable seed predictions for the 2024-2025 season and beyond.

---

### **2. NCAA Basketball Postseason Outcome Prediction**

#### **Overview**
Once we have obtain the postseason seeds for our teams we decide to work on predicting how march madness will pan out i.e. who will be win it all, which teams will make the final four, elight eight and so on. This element of the project uses a Random Forest Classifier to predict postseason outcomes for NCAA basketball teams based on performance metrics.

### **How It Works**
1. **Data Preprocessing:**
   - **Encoding `POSTSEASON` Outcomes:** The `POSTSEASON` column, which contains categorical values representing teams' outcomes in the NCAA tournament (e.g., Champion, Runner-Up, Final Four), is transformed into numerical labels using `LabelEncoder`. This step allows the model to work with numerical data for machine learning tasks.
   - **Filtering Data:** Only teams that have participated in postseason play are kept, ensuring that the model is trained on relevant data where postseason outcomes are known.
2. **Model Training:**
   - **Feature Selection:** The Random Forest Classifier is trained on a set of important features that reflect team performance, such as offensive efficiency (`ADJOE`), defensive efficiency (`ADJDE`), and other metrics like `TOR` (Turnover Rate) and `EFG_O` (Effective Field Goal Percentage for offense).
   - **Training the Model:** Using these features, the model learns the patterns that link team performance metrics to postseason outcomes (e.g., reaching the Final Four or winning the Championship). The Random Forest algorithm, known for its ability to handle complex data relationships, builds multiple decision trees and aggregates their predictions for improved accuracy.
3. **Outcome Assignment:**
   - **Predicting Probabilities:** Once trained, the model is used to predict the postseason probabilities for teams in the current live dataset. The model outputs a probability distribution across different postseason outcomes (e.g., Champion, Final Four, Sweet Sixteen).
   - **Systematic Label Assignment:** Teams are assigned a postseason outcome based on the predicted probabilities. For example, the model assigns the highest probability label (Champion) to the team with the most likelihood of winning the tournament. The next highest probabilities are assigned to outcomes like Final Four, Elite Eight, etc., following the hierarchical structure of the tournament's progression (Champion > Runner-Up > Final Four > Elite Eight, etc.).
4. **Output Mapping:**
   - **Mapping Numeric Labels to Descriptive Outcomes:** After assigning numerical labels to teams based on predicted postseason rankings, these labels are mapped back to their descriptive postseason outcomes using a dictionary. This ensures the final output is easily interpretable, with teams having a clear classification like "Champion," "Elite Eight," or "Round of 64."

### Conclusion:

Together, these interconnected projects offer a comprehensive tool for predicting both tournament seeding and outcomes, continuously refined with live data to provide real-time insights. This approach not only enhances the accuracy of predictions but also offers a dynamic system capable of adapting to new data and providing updated forecasts throughout the tournament season.

## File Structure

```
FINAL_PROJECT_DE/
├── archive/
├── predictions/
├── seeding/
├── basketball_team_ratings.csv
├── cbb_data.db
├── CBB_to_Database.py
├── current_cbb_live_data.csv
├── data_clense.ipynb
├── final_model.ipynb
├── README.md
├── test_data.csv
└── train_data.csv
```

# TODO

-  Follow this for more clairty on the readme: https://github.com/nogibjj/Final_Project_Stock_Analysis

- Picture on the flow from Code -> DB -> AWS -> App running 

- Photos of the application with instructions of what each page shows 

- Update the file structure above 

- Update some information about flast, rds, lightsail and more 

- talk about our requirements.txt file and what all is needed in specific 
