import pandas as pd
import sys
from glob import glob




try:
    while True:
        print("Control + Z to exit the program")
        print("Available folders are:")
        folders=glob("data/*")
        folder_list=[folder.split("/")[1] for folder in folders]
        for folder in folder_list:
            print(folder)
        time_stamp=input("Please type the timestamp folder name:")
        df=pd.read_csv("data/{}/{}.csv".format(time_stamp,time_stamp))
        
        print("Valid Senario Range: {} to {}".format(0,len(df)-1))
        
        start_scenario=int(input("From Senario #:"))
        end_scenario=int(input("To Scenario #:"))
        file_name=str("data/{}/{}_to_{}.csv".format(time_stamp,str(start_scenario),str(end_scenario)))
        df[start_scenario:end_scenario+1].to_csv(file_name,index=None)
        print("File exported to {}".format(file_name))
        print("----------------------")
        print("")
        
except:
    print("File does not exist or Senario range is incorrect")
    


