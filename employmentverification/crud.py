from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

def fetch_company_details(email: str):
    return {
        "company_name": "CloudKaptan Consultancy Service Pvt. Limited",
        "result": "Success",
        "current_term": "4"
    }
