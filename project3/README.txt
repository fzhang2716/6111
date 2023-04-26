A README file including the following information:
    a. Ruineng Li : rl3315, Frank Zhang : hz2716
    b. list of file we are submiting:
        README.txt
        cleaned_data.csv
        Motor_Vehicle_Collisions_-_Crashes.csv
        NYPD_Arrests_Data__Historic_.csv
        NYPD_Complaint_Data_Current__Year_To_Date_.csv
        NYPD_Shooting_Incident_Data__Historic_.csv
        datamining.py
        [add more files]
    c. In order to run program, use:

            python3 main.py INTEGRATED-DATASET.csv 0.01 0.5

        If want to reproduce the cleaned_data.csv from Motor_Vehicle_Collisions_-_Crashes.csv , NYPD_Arrests_Data__Historic_.csv, 
        NYPD_Complaint_Data_Current__Year_To_Date_.csv ,NYPD_Shooting_Incident_Data__Historic_.csv, use:

            python3 datamining.py
        
        might need to install pandas package by:
            pip3 install pandas
        
        [if you need more memory, please indicate so clearly in the README file and specify what configuration we should use for your Google Cloud VM. Provide all commands necessary to install the required software and dependencies for your program.]
        
    d. 
        a. There are 4 data set we used in the project:
            Motor_Vehicle_Collisions_-_Crashes.csv
            https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

            NYPD_Arrests_Data__Historic_.csv
            https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u

            NYPD_Complaint_Data_Current__Year_To_Date_.csv
            https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243

            NYPD_Shooting_Incident_Data__Historic_.csv
            https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8
        b. The data we selected in these datasets are between 01/01/2012 - 12/31/2021. Given all datasets have laititude and longtitude, we decide to 
            divid new york city into 75*75 sectors according to laititude and longtitude. For each dataset, we combine entroes by their laititude and longtitude. 
            If many entries fall into a same sector, we will first put them into a dataframe. And for each row in the dataframe, we use the mode to repersent the string value
            and mean to reperesent numerical value. And we combiend four dataframes (one from each csv) to create cleaned_data.csv.
            If want to reproduce the cleaned_data.csv, put all four NYC open datasets csv and datamining.py into a same folder and execute "python3 datamining.py".
        c.
            The reason we chose these four datasets is that we want to find some asscociation rules in the Public safety.
            It comes to our attention that location is a great index to combine public safety datasets because they all typically have a record of laititude and longtitude of an event. 
            Therefore, by combining these datasets, we want to discover some interesting asscociation rules between arrest, traffic, shooting, and complain records.
            [Some other ideas?]
    e.
        [please add some]
    f. 
        [please add some]
    g.  [add if needed]

