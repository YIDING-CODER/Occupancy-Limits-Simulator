import pandas as pd
import sys



try:
    time_stamp=input("Please type the timestamp folder name:")
    df=pd.read_csv("data/{}/{}.csv".format(time_stamp,time_stamp))
except:
    print("File does not exist")
    

while True:
    start_scenario=int(input("From Senario #:"))
    end_scenario=int(input("To Scenario #:"))

    df[df["senario"]==start_scenario]["acc_real_area"]
    df[df["senario"]==end_scenario]["acc_real_area"]

    column_name="acc_real_area"

    start_value=df[df["senario"]==start_scenario]["acc_real_area"].values[0]
    end_value=df[df["senario"]==end_scenario]["acc_real_area"].values[0]
    print("Senario {} : {} = {}".format(start_scenario, column_name,start_value))
    print("Senario {} : {} = {}".format(end_scenario, column_name,end_value))
    print("{} differences = {}".format(column_name,end_value-start_value))
    print("===================================================")

