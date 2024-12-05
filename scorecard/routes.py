from fastapi import FastAPI, HTTPException, APIRouter
from typing import List
from scorecard.schemas import ScorecardRule,CreditData

router = APIRouter()

# In-memory storage for scorecard rules (this can be a database in production)
scorecard_rules: List[ScorecardRule] = []

@router.post("/admin/rules/")
async def configure_scorecard_rules(rules: List[ScorecardRule]):
    global scorecard_rules
    scorecard_rules = rules  # Store the rules in memory (or a DB)
    return {"message": "Rules configured successfully"}

def evaluate_rules(user_data: dict) -> float:
    score = 0
    
    # Iterate through each configured rule and evaluate against user input
    for rule in scorecard_rules:
        user_value = user_data.get(rule.field)
        
        if user_value is None:
            raise HTTPException(status_code=400, detail=f"Field {rule.field} is missing in user input")
        
        # Compare the user value with the rule value based on the operator
        if rule.operator == ">":
            if user_value > rule.value:
                score += rule.score  # Add the score for the rule
        elif rule.operator == "<":
            if user_value < rule.value:
                score += rule.score  # Add the score for the rule
        elif rule.operator == "=":
            if user_value == rule.value:
                score += rule.score  # Add the score for the rule
    
    return score

@router.post("/")
async def evaluate_score(user_data: CreditData):
    try:
        # Convert user data to dictionary
        user_data_dict = user_data.dict()
        
        # Evaluate the score based on configured rules
        score = evaluate_rules(user_data_dict)
        
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
