# crash data set (traffic) 2012-2023 has longtitude and leititude
# https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95


# policy complain 1961-2022
# https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243

# NYPD shooting 2006-2021
# https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8

# nypd arrest 2006-2021
# https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u
import sys
import csv
import pandas as pd
import os
from datetime import datetime

def process_data(raw_filename):

    import math

    data = pd.read_csv(raw_filename)
    sector_indexes = data["sector index"]
    for i, idx in enumerate(sector_indexes):
        idx_floor = int(idx/500) * 500
        idx_ceil = (int(idx/500) + 1) * 500
        new_idx = str(idx_floor) +"< sector_no <=" + str(idx_ceil)
        data["sector index"][i] = new_idx

    arrest_age_group = data["Arrests_AGE_GROUP"]
    for i, item in enumerate(arrest_age_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "arrested age:" + str(item)
            data["Arrests_AGE_GROUP"][i] = new_item

    arrest_sex = data["Arrests_PERP_SEX"]
    for i, item in enumerate(arrest_sex):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "arrested gender:" + str(item)
            data["Arrests_PERP_SEX"][i] = new_item
    
    arrest_race = data["Arrests_PERP_RACE"]
    for i, item in enumerate(arrest_race):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "arrested race:" + str(item)
            data["Arrests_PERP_RACE"][i] = new_item
    
    complaint_susp_age_group = data["Complaint_SUSP_AGE_GROUP"]
    for i, item in enumerate(complaint_susp_age_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Suspect's Age:" + str(item)
            data["Complaint_SUSP_AGE_GROUP"][i] = new_item
    
    complaint_susp_race_group = data["Complaint_SUSP_RACE"]
    for i, item in enumerate(complaint_susp_race_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Suspect's Race:" + str(item)
            data["Complaint_SUSP_RACE"][i] = new_item

    complaint_susp_sex_group = data["Complaint_SUSP_SEX"]
    for i, item in enumerate(complaint_susp_sex_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Suspect's Sex:" + str(item)
            data["Complaint_SUSP_SEX"][i] = new_item
    
    complaint_vic_age_group = data["Complaint_VIC_AGE_GROUP"]
    for i, item in enumerate(complaint_vic_age_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Victim's Age:" + str(item)
            data["Complaint_VIC_AGE_GROUP"][i] = new_item
    
    complaint_vic_race_group = data["Complaint_VIC_RACE"]
    for i, item in enumerate(complaint_vic_race_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Victim's Race:" + str(item)
            data["Complaint_VIC_RACE"][i] = new_item

    complaint_vic_sex_group = data["Complaint_VIC_SEX"]
    for i, item in enumerate(complaint_vic_sex_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Complaint Victim's Sex:" + str(item)
            data["Complaint_VIC_SEX"][i] = new_item
    

    ## shooting data
    shooting_perp_age_group = data["Shooting_PERP_AGE_GROUP"]
    for i, item in enumerate(shooting_perp_age_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Perpetrator's Age:" + str(item)
            data["Shooting_PERP_AGE_GROUP"][i] = new_item
    
    shooting_perp_race_group = data["Shooting_PERP_RACE"]
    for i, item in enumerate(shooting_perp_race_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Perpetrator's Race:" + str(item)
            data["Shooting_PERP_RACE"][i] = new_item

    shooting_perp_sex_group = data["Shooting_PERP_SEX"]
    for i, item in enumerate(shooting_perp_sex_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "shooting Perpetrator's Sex:" + str(item)
            data["Shooting_PERP_SEX"][i] = new_item
    
    shooting_vic_age_group = data["Shooting_VIC_AGE_GROUP"]
    for i, item in enumerate(shooting_vic_age_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Victim's Age:" + str(item)
            data["Shooting_VIC_AGE_GROUP"][i] = new_item
    
    shooting_vic_race_group = data["Shooting_VIC_RACE"]
    for i, item in enumerate(shooting_vic_race_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Victim's Race:" + str(item)
            data["Shooting_VIC_RACE"][i] = new_item

    shooting_vic_sex_group = data["Shooting_VIC_SEX"]
    for i, item in enumerate(shooting_vic_sex_group):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Victim's Sex:" + str(item)
            data["Shooting_VIC_SEX"][i] = new_item

    shooting_murder_flag = data["Shooting_STATISTICAL_MURDER_FLAG"]
    for i, item in enumerate(shooting_murder_flag):
        if isinstance(item, str) or isinstance(item, bool) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting murdered:" + str(item)
            data["Shooting_STATISTICAL_MURDER_FLAG"][i] = new_item
    
    shooting_location = data["Shooting_LOCATION_DESC"]
    for i, item in enumerate(shooting_location):
        if isinstance(item, str) or (isinstance(item, float) and not math.isnan(item)):
            new_item = "Shooting Location:" + str(item)
            data["Shooting_LOCATION_DESC"][i] = new_item

    data.to_csv("INTEGRATED-DATASET.csv")


def findMode(series,keyWord):
    if len(series) == 0:
        return None
    elif len(series) == 1:
        return series.index[0]
    
    if series.index[0] == keyWord:
        return series.index[1]
    else:
        return series.index[0]

def findSector(laitude,longtitude):
    return(max(i for i in lai_list if i < laitude),max(i for i in long_list if i < longtitude))


if __name__ == "__main__":
    lai_min = 40.492423
    lai_max = 40.918213
    long_min = -74.259052
    long_max = -73.700809
    start_date = datetime.strptime("01/01/2012", '%m/%d/%Y')
    end_date = datetime.strptime("12/31/2021", '%m/%d/%Y')

    #create sector 
    long_list = []
    long_cell =  (long_max - long_min)/75
    for i in range(0,75):
        long_list.append(long_min+long_cell*i)

    lai_list = []
    lai_cell =  abs((lai_max - lai_min)/75)
    for i in range(0,75):
        lai_list.append(lai_min+lai_cell*i)

    # Motor_Vehicle_Collisions_Crashes data clean
    Motor_Vehicle_Collisions_Crashes_df = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv',low_memory=False)
    
    Motor_Vehicle_Collisions_Crashes_map = {}
    for i in lai_list:
        for j in long_list:
            Motor_Vehicle_Collisions_Crashes_map[(i,j)] = []
    
    for idx, row in Motor_Vehicle_Collisions_Crashes_df.iterrows():
        curr_date = datetime.strptime(row["CRASH DATE"], '%m/%d/%Y')
        if curr_date >= start_date and curr_date <= end_date:
            if pd.isnull(row["LATITUDE"]) == False and pd.isnull(row["LONGITUDE"]) == False and lai_min <= row["LATITUDE"] <= lai_max and long_min <= row["LONGITUDE"] <= long_max:
                curr_sector = findSector(row["LATITUDE"],row["LONGITUDE"])
                if curr_sector in Motor_Vehicle_Collisions_Crashes_map:
                    Motor_Vehicle_Collisions_Crashes_map[curr_sector].append([row["NUMBER OF PERSONS INJURED"],
                                                                            row["NUMBER OF PERSONS KILLED"],
                                                                            row["NUMBER OF PEDESTRIANS INJURED"],
                                                                            row["NUMBER OF PEDESTRIANS KILLED"],
                                                                            row["NUMBER OF CYCLIST INJURED"],
                                                                            row["NUMBER OF CYCLIST KILLED"],
                                                                            row["NUMBER OF MOTORIST INJURED"],
                                                                            row["NUMBER OF MOTORIST KILLED"],
                                                                            row["CONTRIBUTING FACTOR VEHICLE 1"],
                                                                            row["CONTRIBUTING FACTOR VEHICLE 2"],
                                                                            row["CONTRIBUTING FACTOR VEHICLE 3"],
                                                                            row["CONTRIBUTING FACTOR VEHICLE 4"],
                                                                            row["CONTRIBUTING FACTOR VEHICLE 5"],
                                                                            row["VEHICLE TYPE CODE 1"],
                                                                            row["VEHICLE TYPE CODE 2"],
                                                                            row["VEHICLE TYPE CODE 3"],
                                                                            row["VEHICLE TYPE CODE 4"],
                                                                            row["VEHICLE TYPE CODE 5"]])
    averaged_Motor_Vehicle_Collisions_Crashes_data = []
    for i in Motor_Vehicle_Collisions_Crashes_map:
        if len(Motor_Vehicle_Collisions_Crashes_map[i]) >= 1:
            curr_sector_df = pd.DataFrame(Motor_Vehicle_Collisions_Crashes_map[i], columns=["NUMBER OF PERSONS INJURED",
                                                                                            "NUMBER OF PERSONS KILLED",
                                                                                            "NUMBER OF PEDESTRIANS INJURED",
                                                                                            "NUMBER OF PEDESTRIANS KILLED",
                                                                                            "NUMBER OF CYCLIST INJURED",
                                                                                            "NUMBER OF CYCLIST KILLED",
                                                                                            "NUMBER OF MOTORIST INJURED",
                                                                                            "NUMBER OF MOTORIST KILLED",
                                                                                            "CONTRIBUTING FACTOR VEHICLE 1",
                                                                                            "CONTRIBUTING FACTOR VEHICLE 2",
                                                                                            "CONTRIBUTING FACTOR VEHICLE 3",
                                                                                            "CONTRIBUTING FACTOR VEHICLE 4",
                                                                                            "CONTRIBUTING FACTOR VEHICLE 5",
                                                                                            "VEHICLE TYPE CODE 1",
                                                                                            "VEHICLE TYPE CODE 2",
                                                                                            "VEHICLE TYPE CODE 3",
                                                                                            "VEHICLE TYPE CODE 4",
                                                                                            "VEHICLE TYPE CODE 5"])

            curr_data = [i[0],
                        i[1],
                        curr_sector_df["NUMBER OF PERSONS INJURED"].mean(),
                        curr_sector_df["NUMBER OF PERSONS KILLED"].mean(),
                        curr_sector_df["NUMBER OF PEDESTRIANS INJURED"].mean(),
                        curr_sector_df["NUMBER OF PEDESTRIANS KILLED"].mean(),
                        curr_sector_df["NUMBER OF CYCLIST INJURED"].mean(),
                        curr_sector_df["NUMBER OF CYCLIST KILLED"].mean(),
                        curr_sector_df["NUMBER OF MOTORIST INJURED"].mean(),
                        curr_sector_df["NUMBER OF MOTORIST KILLED"].mean(),
                        findMode(curr_sector_df["CONTRIBUTING FACTOR VEHICLE 1"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["CONTRIBUTING FACTOR VEHICLE 2"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["CONTRIBUTING FACTOR VEHICLE 3"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["CONTRIBUTING FACTOR VEHICLE 4"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["CONTRIBUTING FACTOR VEHICLE 5"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["VEHICLE TYPE CODE 1"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["VEHICLE TYPE CODE 2"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["VEHICLE TYPE CODE 3"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["VEHICLE TYPE CODE 4"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["VEHICLE TYPE CODE 5"].value_counts().nlargest(2), None)]

            
            averaged_Motor_Vehicle_Collisions_Crashes_data.append(curr_data)

    averaged_Motor_Vehicle_Collisions_Crashes_data_df = pd.DataFrame(averaged_Motor_Vehicle_Collisions_Crashes_data, columns=["sector laitude",
                                                                                                                          "sector longtitude",
                                                                                                                          "Collisions_NUMBER OF PERSONS INJURED",
                                                                                                                          "Collisions_NUMBER OF PERSONS KILLED",
                                                                                                                          "Collisions_NUMBER OF PEDESTRIANS INJURED",
                                                                                                                          "Collisions_NUMBER OF PEDESTRIANS KILLED",
                                                                                                                          "Collisions_NUMBER OF CYCLIST INJURED",
                                                                                                                          "Collisions_NUMBER OF CYCLIST KILLED",
                                                                                                                          "Collisions_NUMBER OF MOTORIST INJURED",
                                                                                                                          "Collisions_NUMBER OF MOTORIST KILLED",
                                                                                                                          "Collisions_CONTRIBUTING FACTOR VEHICLE 1",
                                                                                                                          "Collisions_CONTRIBUTING FACTOR VEHICLE 2",
                                                                                                                          "Collisions_CONTRIBUTING FACTOR VEHICLE 3",
                                                                                                                          "Collisions_CONTRIBUTING FACTOR VEHICLE 4",
                                                                                                                          "Collisions_CONTRIBUTING FACTOR VEHICLE 5",
                                                                                                                          "Collisions_VEHICLE TYPE CODE 1",
                                                                                                                          "Collisions_VEHICLE TYPE CODE 2",
                                                                                                                          "Collisions_VEHICLE TYPE CODE 3",
                                                                                                                          "Collisions_VEHICLE TYPE CODE 4",
                                                                                                                          "Collisions_VEHICLE TYPE CODE 5"])
    averaged_Motor_Vehicle_Collisions_Crashes_data_df.to_csv('sector_Motor_Vehicle_Collisions_Crashes_data.csv')

    # NYPD_Arrests_Data__Historic_ data clean
    NYPD_Arrests_Data__Historic_df = pd.read_csv('NYPD_Arrests_Data__Historic_.csv')
    NYPD_Arrests_Data__Historic_map = {}
    for i in lai_list:
        for j in long_list:
            NYPD_Arrests_Data__Historic_map[(i,j)] = []
    
    
    for idx, row in NYPD_Arrests_Data__Historic_df.iterrows():
        curr_date = datetime.strptime(row["ARREST_DATE"], '%m/%d/%Y')
        if curr_date >= start_date and curr_date <= end_date:
            if pd.isnull(row["Latitude"]) == False and pd.isnull(row["Longitude"]) == False and lai_min <= row["Latitude"] <= lai_max and long_min <= row["Longitude"] <= long_max:
                curr_sector = findSector(row["Latitude"], row["Longitude"])
                if curr_sector in NYPD_Arrests_Data__Historic_map:
                    NYPD_Arrests_Data__Historic_map[curr_sector].append([row["PD_CD"],
                                                                        row["PD_DESC"],
                                                                        row["OFNS_DESC"],
                                                                        row["LAW_CODE"],
                                                                        row["LAW_CAT_CD"],
                                                                        row["ARREST_PRECINCT"],
                                                                        row["JURISDICTION_CODE"],
                                                                        row["AGE_GROUP"],
                                                                        row["PERP_SEX"],
                                                                        row["PERP_RACE"]])

    averaged_NYPD_Arrests_Data__Historic = []

    for i in NYPD_Arrests_Data__Historic_map:
        if len(NYPD_Arrests_Data__Historic_map[i]) >= 1:

            curr_sector_df = pd.DataFrame(NYPD_Arrests_Data__Historic_map[i], columns=["PD_CD",
                                                                                    "PD_DESC",
                                                                                    "OFNS_DESC",
                                                                                    "LAW_CODE",
                                                                                    "LAW_CAT_CD",
                                                                                    "ARREST_PRECINCT",
                                                                                    "JURISDICTION_CODE",
                                                                                    "AGE_GROUP",
                                                                                    "PERP_SEX",
                                                                                    "PERP_RACE"])

            curr_data = [i[0],
                        i[1],
                        findMode(curr_sector_df["PD_CD"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["PD_DESC"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["OFNS_DESC"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["LAW_CODE"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["LAW_CAT_CD"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["ARREST_PRECINCT"].value_counts(
                        ).nlargest(2), "Unspecified"),
                        findMode(curr_sector_df["JURISDICTION_CODE"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["AGE_GROUP"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["PERP_SEX"].value_counts().nlargest(
                            2), None),
                        findMode(curr_sector_df["PERP_RACE"].value_counts().nlargest(
                            2), None)]


            averaged_NYPD_Arrests_Data__Historic.append(curr_data)
    
    averaged_NYPD_Arrests_Data__Historic_df = pd.DataFrame(averaged_NYPD_Arrests_Data__Historic, columns=["sector laitude",
                                                                                                      "sector longtitude",
                                                                                                      "Arrests_PD_CD",
                                                                                                      "Arrests_PD_DESC",
                                                                                                      "Arrests_OFNS_DESC",
                                                                                                      "Arrests_LAW_CODE",
                                                                                                      "Arrests_LAW_CAT_CD",
                                                                                                      "Arrests_ARREST_PRECINCT",
                                                                                                      "Arrests_JURISDICTION_CODE",
                                                                                                      "Arrests_AGE_GROUP",
                                                                                                      "Arrests_PERP_SEX",
                                                                                                      "Arrests_PERP_RACE"])
    averaged_NYPD_Arrests_Data__Historic_df.to_csv('sector_NYPD_Arrests_Data__Historic.csv')


    # NYPD_Complaint data clean
    NYPD_Complaint_Data_Current__Year_To_Date_df = pd.read_csv('NYPD_Complaint_Data_Current__Year_To_Date_.csv')
    NYPD_Complaint_Data_Current__Year_To_Date_map = {}
    for i in lai_list:
        for j in long_list:
            NYPD_Complaint_Data_Current__Year_To_Date_map[(i, j)] = []


    for idx, row in NYPD_Complaint_Data_Current__Year_To_Date_df.iterrows():
        curr_date = datetime.strptime(row["CMPLNT_FR_DT"], '%m/%d/%Y')

        if curr_date >= start_date and curr_date <= end_date:
            if pd.isnull(row["Latitude"]) == False and pd.isnull(row["Longitude"]) == False and lai_min <= row["Latitude"] <= lai_max and long_min <= row["Longitude"] <= long_max:
                curr_sector = findSector(row["Latitude"], row["Longitude"])
                if curr_sector in NYPD_Complaint_Data_Current__Year_To_Date_map:
                    NYPD_Complaint_Data_Current__Year_To_Date_map[curr_sector].append([row["ADDR_PCT_CD"],
                                                                                    row["CRM_ATPT_CPTD_CD"],
                                                                                    row["JURIS_DESC"],
                                                                                    row["KY_CD"],
                                                                                    row["LAW_CAT_CD"],
                                                                                    row["LOC_OF_OCCUR_DESC"],
                                                                                    row["OFNS_DESC"],
                                                                                    row["PD_CD"],
                                                                                    row["PD_DESC"],
                                                                                    row["PREM_TYP_DESC"],
                                                                                    row["SUSP_AGE_GROUP"],
                                                                                    row["SUSP_RACE"],
                                                                                    row["SUSP_SEX"],
                                                                                    row["VIC_AGE_GROUP"],
                                                                                    row["VIC_RACE"],
                                                                                    row["VIC_SEX"]])
                    
    averaged_NYPD_Complaint_Data_Current__Year_To_Date = []

    for i in NYPD_Complaint_Data_Current__Year_To_Date_map:
        if len(NYPD_Complaint_Data_Current__Year_To_Date_map[i]) >= 1:

            curr_sector_df = pd.DataFrame(NYPD_Complaint_Data_Current__Year_To_Date_map[i], columns=["ADDR_PCT_CD",
                                                                                                    "CRM_ATPT_CPTD_CD",
                                                                                                    "JURIS_DESC",
                                                                                                    "KY_CD",
                                                                                                    "LAW_CAT_CD",
                                                                                                    "LOC_OF_OCCUR_DESC",
                                                                                                    "OFNS_DESC",
                                                                                                    "PD_CD",
                                                                                                    "PD_DESC",
                                                                                                    "PREM_TYP_DESC",
                                                                                                    "SUSP_AGE_GROUP",
                                                                                                    "SUSP_RACE",
                                                                                                    "SUSP_SEX",
                                                                                                    "VIC_AGE_GROUP",
                                                                                                    "VIC_RACE",
                                                                                                    "VIC_SEX"])

            #this data contians unknown and null, removed null 
            curr_data = [i[0],
                        i[1],
                        findMode(curr_sector_df["ADDR_PCT_CD"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["CRM_ATPT_CPTD_CD"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["JURIS_DESC"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["KY_CD"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["LAW_CAT_CD"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["LOC_OF_OCCUR_DESC"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["OFNS_DESC"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["PD_CD"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["PD_DESC"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["PREM_TYP_DESC"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["SUSP_AGE_GROUP"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["SUSP_RACE"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["SUSP_SEX"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["VIC_AGE_GROUP"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["VIC_RACE"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["VIC_SEX"].value_counts().nlargest(
                            2), "(null)")]


            averaged_NYPD_Complaint_Data_Current__Year_To_Date.append(curr_data)
    

    averaged_NYPD_Complaint_Data_Current__Year_To_Date_df = pd.DataFrame(averaged_NYPD_Complaint_Data_Current__Year_To_Date, columns=["sector laitude",
                                                                                                                                  "sector longtitude",
                                                                                                                                  "Complaint_ADDR_PCT_CD",
                                                                                                                                  "Complaint_CRM_ATPT_CPTD_CD",
                                                                                                                                  "Complaint_JURIS_DESC",
                                                                                                                                  "Complaint_KY_CD",
                                                                                                                                  "Complaint_LAW_CAT_CD",
                                                                                                                                  "Complaint_LOC_OF_OCCUR_DESC",
                                                                                                                                  "Complaint_OFNS_DESC",
                                                                                                                                  "Complaint_PD_CD",
                                                                                                                                  "Complaint_PD_DESC",
                                                                                                                                  "Complaint_PREM_TYP_DESC",
                                                                                                                                  "Complaint_SUSP_AGE_GROUP",
                                                                                                                                  "Complaint_SUSP_RACE",
                                                                                                                                  "Complaint_SUSP_SEX",
                                                                                                                                  "Complaint_VIC_AGE_GROUP",
                                                                                                                                  "Complaint_VIC_RACE",
                                                                                                                                  "Complaint_VIC_SEX"])
    averaged_NYPD_Complaint_Data_Current__Year_To_Date_df.to_csv('sector_NYPD_Complaint_Data_Current__Year_To_Date.csv')

    # NYPD shooting data clean
    NYPD_Shooting_Incident_Data__Historic_df = pd.read_csv('NYPD_Shooting_Incident_Data__Historic_.csv')
    NYPD_Shooting_Incident_Data__Historic_map = {}
    for i in lai_list:
        for j in long_list:
            NYPD_Shooting_Incident_Data__Historic_map[(i, j)] = []


    for idx, row in NYPD_Shooting_Incident_Data__Historic_df.iterrows():
        curr_date = datetime.strptime(row["OCCUR_DATE"], '%m/%d/%Y')

        if curr_date >= start_date and curr_date <= end_date:
            if pd.isnull(row["Latitude"]) == False and pd.isnull(row["Longitude"]) == False and lai_min <= row["Latitude"] <= lai_max and long_min <= row["Longitude"] <= long_max:
                curr_sector = findSector(row["Latitude"], row["Longitude"])
                if curr_sector in NYPD_Shooting_Incident_Data__Historic_map:
                    NYPD_Shooting_Incident_Data__Historic_map[curr_sector].append([row["PRECINCT"],
                                                                                    row["JURISDICTION_CODE"],
                                                                                    row["LOCATION_DESC"],
                                                                                    row["STATISTICAL_MURDER_FLAG"],
                                                                                    row["PERP_AGE_GROUP"],
                                                                                    row["PERP_SEX"],
                                                                                    row["PERP_RACE"],
                                                                                    row["VIC_AGE_GROUP"],
                                                                                    row["VIC_SEX"],
                                                                                    row["VIC_RACE"]])

    averaged_NYPD_Shooting_Incident_Data__Historic = []

    for i in NYPD_Shooting_Incident_Data__Historic_map:
        if len(NYPD_Shooting_Incident_Data__Historic_map[i]) >= 1:
            curr_sector_df = pd.DataFrame(NYPD_Shooting_Incident_Data__Historic_map[i], columns=["PRECINCT",
                                                                                                "JURISDICTION_CODE",
                                                                                                "LOCATION_DESC",
                                                                                                "STATISTICAL_MURDER_FLAG",
                                                                                                "PERP_AGE_GROUP",
                                                                                                "PERP_SEX",
                                                                                                "PERP_RACE",
                                                                                                "VIC_AGE_GROUP",
                                                                                                "VIC_SEX",
                                                                                                "VIC_RACE"])

            # this data contians unknown and null, removed null
            curr_data = [i[0],
                        i[1],
                        findMode(curr_sector_df["PRECINCT"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["JURISDICTION_CODE"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["LOCATION_DESC"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["STATISTICAL_MURDER_FLAG"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["PERP_AGE_GROUP"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["PERP_SEX"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["PERP_RACE"].value_counts(
                        ).nlargest(2), "(null)"),
                        findMode(curr_sector_df["VIC_AGE_GROUP"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["VIC_SEX"].value_counts().nlargest(
                            2), "(null)"),
                        findMode(curr_sector_df["VIC_RACE"].value_counts().nlargest(
                            2), "(null)")]


            averaged_NYPD_Shooting_Incident_Data__Historic.append(curr_data)

    averaged_NYPD_Shooting_Incident_Data__Historic_df = pd.DataFrame(averaged_NYPD_Shooting_Incident_Data__Historic, columns=["sector laitude",
                                                                                                                            "sector longtitude",
                                                                                                                            "Shooting_PRECINCT",
                                                                                                                            "Shooting_JURISDICTION_CODE",
                                                                                                                            "Shooting_LOCATION_DESC",
                                                                                                                            "Shooting_STATISTICAL_MURDER_FLAG",
                                                                                                                            "Shooting_PERP_AGE_GROUP",
                                                                                                                            "Shooting_PERP_SEX",
                                                                                                                            "Shooting_PERP_RACE",
                                                                                                                            "Shooting_VIC_AGE_GROUP",
                                                                                                                            "Shooting_VIC_SEX",
                                                                                                                            "Shooting_VIC_RACE"])

    averaged_NYPD_Shooting_Incident_Data__Historic_df.to_csv('sector_NYPD_Shooting_Incident_Data__Historic.csv')

    # join all datasets
    sector_list = []
    for i in lai_list:
        for j in long_list:
            sector_list.append([i,j])

    sector_df = pd.DataFrame(sector_list, columns=["sector laitude","sector longtitude"])

    combined_df = pd.merge(averaged_Motor_Vehicle_Collisions_Crashes_data_df,averaged_NYPD_Arrests_Data__Historic_df, on=['sector laitude','sector longtitude'], how='outer')
    combined_df = pd.merge(combined_df,averaged_NYPD_Complaint_Data_Current__Year_To_Date_df, on=['sector laitude','sector longtitude'], how='outer')
    combined_df = pd.merge(combined_df,averaged_NYPD_Shooting_Incident_Data__Historic_df, on=['sector laitude','sector longtitude'], how='outer')
    print(combined_df.shape[0])

    index_map = {}
    count = 0
    for i in lai_list:
        for j in long_list:
            index_map[(i, j)] = count
            count = count + 1

    index_list = []
    for ind, row in combined_df.iterrows():
        index_list.append(index_map[(row["sector laitude"],row["sector longtitude"])])

    combined_df["sector index"] = index_list
    combined_df.to_csv('cleaned_data.csv')
    process_data('ccleaned_data.csv')
