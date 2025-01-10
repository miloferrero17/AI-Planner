import os
class Config:
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  WA_API_KEY = os.getenv("WA_API_KEY")
