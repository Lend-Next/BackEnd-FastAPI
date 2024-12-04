from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import pandas as pd
import scorecardpy as sc
from sklearn.linear_model import LogisticRegression
from scorecard.schemas import CreditData

router = APIRouter()

# Example training data
data = pd.DataFrame({
    "age": [23, 45, 56, 34, 67],  # Feature column
    "income": [40000, 80000, 120000, 60000, 70000],  # Another feature column
    "y": [0, 1, 0, 1, 0]  # Target column (binary outcome)
})

# Generate WOE bins for features
bins = sc.woebin(data, y="y")

# Apply WOE transformation to data
woe_data = sc.woebin_ply(data, bins)

# Print columns of `woe_data` to check the actual names after WOE transformation
print("WOE Data Columns:", woe_data.columns)  # Debugging step to inspect column names

# Select feature columns for modeling (Ensure columns like 'age_woe', 'income_woe' exist)
xcolumns = ["age_woe", "income_woe"]  # Use the exact names you expect from WOE transformation
X = woe_data[xcolumns]
y = woe_data["y"]

# Train a logistic regression model
model = LogisticRegression()
model.fit(X, y)

# Generate scorecard using the trained model
scorecard = sc.scorecard(bins, model, xcolumns, points0=600, odds0=1/20, pdo=50)


# Scoring endpoint
@router.post("/")
async def score(request: CreditData):
    try:
        # Convert input data to DataFrame
        # Example training data
        data = pd.DataFrame({
            "age": [23, 45, 56, 34, 67],  # Feature column
            "income": [40000, 80000, 120000, 60000, 70000],  # Another feature column
            "y": [0, 1, 0, 1, 0]  # Target column (binary outcome)
        })
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
