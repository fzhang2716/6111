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
        a_priori.py
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
            and mean to reperesent numerical value. And we combine four dataframes (one from each csv) to first create cleaned_data.csv.
            Further, each dataset above includes many properties and lots of terminologies, which makes easy for the code to run out of memory and slow to process. Thus, for all columns in cleaned_data.csv, we only take the most representative properties from them. More detailedly, they are:
	- Collisions_CONTRIBUTING FACTOR VEHICLE 1, we only take the first contributing factor because it is most well-recorded
	- Collisions_VEHICLE TYPE CODE 1, we only take the first vehicle type because it is most well-recorded
	- Arrests_PD_DESC, because it records the most detailed reason of arrests compared to other similar columns (i.e. those recording the origins of the issues)
	- Arrests_AGE_GROUP, Arrests_PERP_RACE, which record the basic information of people who are involved in the arrests
	- Complaint_PD_DESC, because  it records the most detailed reason of complaints compared to other similar columns (i.e. those recording the origins of the issues)
	- Complaint_PREM_TYP_DESC, which records where the complaints happened
	- Complaint_SUSP_AGE_GROUP, Complaint_SUSP_RACE, Complaint_SUSP_SEX, Complaint_VIC_AGE_GROUP, Complaint_VIC_RACE, Complaint_VIC_SEX, which record the basic information of people who are involved in the complaints
	- Shooting_LOCATION_DESC, Shooting_STATISTICAL_MURDER_FLAG, which record the location, and whether people are killed in the issues
	- Shooting_SUSP_AGE_GROUP, Shooting_SUSP_RACE, Shooting_SUSP_SEX, Shooting_VIC_AGE_GROUP,Shooting_VIC_SEX, Shooting_VIC_RACE, which record the basic information of people who are involved in the shootings
            And other columns are dropped from the cleaned data. After that, for columns that contain similar properties or properties that are too brief, we add prefixes based on the header information for them for better illustration. In this way, we create the ultimate INTEGRATED-DATASET.CSV through the above process. If you want to reproduce the INTEGRATED-DATASET.csv, put all four NYC open datasets csv and datamining.py into a same folder and execute "python3 datamining.py".
        c.
            The reason we chose these four datasets is that we want to find some asscociation rules in the Public safety.
            It comes to our attention that location is a great index to combine public safety datasets because they all typically have a record of laititude and longtitude of an event. 
            Therefore, by combining these datasets, we want to discover some interesting asscociation rules between arrest, traffic, shooting, and complain records. And more specifically, as we extract all the background information (age group and race) of humans involved in such records, we want to see whether there are some similarites among them. 
      	
    e. The implemented a-priori algorithm strictly follows the algorithm in the reference paper, except that for the subset generation, instead of using a hash table, we directly extract every possible (k-1)-subset using the combination function in the itertools package. More detailedly, the rule extraction process is:
	- First, we follow the apriori algorithm to first generate the support set, and all the frequent item sets with respect to k. For each loop, we first generate a candidate set, then remove candidates whose (k-1) itemset is not in the previous large k-itemset and obtain the set of large (k-1)-itemsets. After that, we compute supports for each item in the current large k-itemset by directly counting the times which item is a subset of a sample in the whole dataset.
	- The above process ends when the current large k-itemset is empty. After that, we forward all the large k-itemsets and the support statistics to obtain association rules. This process is motivated by the computation of the confidence score: to get the numerator, we simply address each item in all large k-item sets; and for the denominator, this need us to obtain every subset of the corresponding item in all large k-item sets. Here we use the combination function again for a similar purpose.
	- We then evaluate whether the confidence score exceeds the threshold and output those which satisfies the given parameters. 
    f. Please use this line to run the code: 
	python a_priori.py INTEGRATED-DATASET.csv 0.25 0.5
        The results are compelling because we use min_sup=0.25 and min_conf=0.5. This means at least the items in the frequent set appear in more than 1/4 samples, and the rules appear in half of the samples that include the LHS of the rules, which means they are quite common in the dataset. 
   g.  We found some very interesting conclusions from the above extracted rules:
	- In every sector, 95% arrested perpetrator are male, and most of them are around 25-44 years old.
	- In every sector, most collisions happen because of driver inattention, which is up to about 86% percent. Besides, almost all such collisions  occured because of male perpetrator.
	- sectors in 2000< sector_no <=2500 have the highest crime rate.

	

