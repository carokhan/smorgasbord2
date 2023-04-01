import json
import os
import pandas as pd

def flatten_data(entry):
    fixed = {}
    keys = list(entry.keys())
    for l1 in keys:
        if type(entry[l1]) == type({}):
            for l2 in list(entry[l1].keys()):
                fixed[l2] = entry[l1][l2]
        else:
            fixed[l1] = entry[l1]
    return fixed

def clean_data(df):
    temp = df.columns

    for col in temp:
        df = df[df[col].astype(bool)]

        try:
            df[col] = df[col].astype(type(1086))
        except ValueError:
            pass

    return df


def load_data(path="./data"):

    data = []
    files = [f for f in os.listdir(path) if f.endswith(".json")]
    for file in files:
        with open("./data/" + file, "r") as f:
            js = json.load(f)    
        for entry in js["root"]:
            data.append(entry)
    
    data = [flatten_data(entry) for entry in data]

    df = pd.DataFrame(data)

    df = clean_data(df)
    df = pointify(df)

    return df


def pointify(df):
    df["cycles"] = df.apply((lambda row: cycles(row)), axis=1)
    df["autoPoints"] = df.apply((lambda row: autoScore(row)), axis=1)
    df["telePoints"] =  df.apply((lambda row: teleScore(row)), axis=1)
    df["chargePoints"] = df.apply((lambda row: stationLevel(row)), axis=1)

    df["totalPoints"] = df["autoPoints"] + df["telePoints"]

    df["tipped"] = df["tipped"].map({'false': 0, 'true': 1})
    df["autoMove"] = df["autoMove"].map({'false': 0, 'true': 1})

    df["autoDockedState"] = df["autoDockedState"].map({'neither': 0, 'on platform': 1, 'balance platform': 2})
    df["teleopDockState"] = df["teleopDockState"].map({'neither': 0, 'in community': 1, 'on platform': 2, 'balance platform': 3})

    return df

def cycles(entry):
    return int(entry["autoBottomScore"]) + int(entry["autoMiddleScore"]) + int(entry["autoTopScore"]) + int(entry["teleopBottomScore"]) + int(entry["teleopMiddleScore"]) + int(entry["teleopTopScore"])

def autoScore(entry):
    total = 0

    if entry["autoMove"] == "true":
        total += 3

    total += int(entry["autoBottomScore"]) * 3
    total += int(entry["autoMiddleScore"]) * 4
    total += int(entry["autoTopScore"]) * 6

    match entry["autoDockedState"]:
        case "on platform": 
            total += 8
        case "balance platform":
            total += 12

    return total

def teleScore(entry):
    total = 0
    
    total += int(entry["teleopBottomScore"]) * 2
    total += int(entry["teleopMiddleScore"]) * 3
    total += int(entry["teleopTopScore"]) * 5

    match entry["teleopDockState"]:
        case "in community":
            total += 2
        case "on platform":
            total += 6
        case "balance platform":
            total += 10 

    return total

def stationLevel(entry):
    total = 0

    match entry["autoDockedState"]:
        case "on platform": 
            total += 8
        case "balance platform":
            total += 12

    match entry["teleopDockState"]:
        case "in community":
            total += 2
        case "on platform":
            total += 6
        case "balance platform":
            total += 10 

    return total
    