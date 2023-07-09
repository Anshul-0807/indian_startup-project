import pandas as pd
from sqlalchemy import create_engine



df = pd.read_csv("olympics_cleaned_v4.csv")

engine = create_engine("mysql+pymysql://root:Anshul_123@127.0.0.1/new_database")
df.to_sql("olympics_cleaned_v4", con=engine)

# this is the code of upload large dataset in mysql workbench through python
# you need to do only one thing
# 1. make the app.py file ,upload dataset in pycharm, paste this code, and in mysql make database for this