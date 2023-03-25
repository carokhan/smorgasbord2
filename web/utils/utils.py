import json
import os
import pandas as pd

def fix_data(entry):
    fixed = {}
    keys = list(entry.keys())
    for l1 in keys:
        if type(entry[l1]) == type({}):
            for l2 in list(entry[l1].keys()):
                fixed[l2] = entry[l1][l2]
        else:
            fixed[l1] = entry[l1]
    return fixed

def load_data(path=os.path.expanduser("~") + "/bluecheese/smorgasbord2/data"):
    data = []
    files = [f for f in os.listdir(path) if f.endswith(".json")]
    for file in files:
        with open(os.path.expanduser("~") + "/bluecheese/smorgasbord2/data/" + file, "r") as f:
            js = json.load(f)    
        for entry in js["root"]:
            data.append(entry)
    
    data = [fix_data(entry) for entry in data]
    return pd.DataFrame(data)

def pointify(df):
    df["cycles"] = df["autoBottomScore"] + df["autoMiddleScore"] + df["autoTopScore"]

    
    