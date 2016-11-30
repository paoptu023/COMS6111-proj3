# COMS6111-proj3

1. Group name: Project 3 Group 23
  Qi Wang (qw2197), Yongjia Huo (yh2796)

2. Submitted files:
    1. main.py -- the main program, implement to extract association rules
    2. clean.py -- the program used to clean the data set
    3. Bus_Breakdown_and_Delays.csv -- the original data set
    4. bus.csv -- the cleaned data set
    5. READEME.md
    
3. The detailed description of data set
    1. We choose the "Bus Breakdown and Delays" data set to generate the INTEGRATED-DATASET file
    2. We use the filters as follows the get the "Bus_Breakdown_and_Delays.csv":
        * School_Year: 2016-2017
        * Run_Type: Special Ed AM Run or Special Ed AM Run
        * Number_of_Students_On_the_Bus > 0
        * Has_Contractor_Notified_Schools: Yes
        * Has_Contractor_Notified_Parents: Yes
        * Have_You_Alerted_OPT: Yes
        * Has_Contractor_Notified_Schools: Yes
        * School_Age_or_PreK: School-Age
       After using these filters, we get the data set "Bus_Breakdown_and_Delays.csv", then we only consider hour instead of the exact time 
       regarding to the "Occurred_On" column and reformat the "How_Long_Delayed". Then we delete unrelated columns and only maintain the 
       following columns:
        * Route_Number	
        * Reason	
        * Schools_Serviced	
        * Occurred_On
        * Boro	
        * Bus_Company_Name	 
        * HR	
        * Number_Of_Students_On_The_Bus	
        * Breakdown_or_Running_Late
    3. The reason why we choose this data set is that we want to know when these breakdowns and delays happens, which is a good indication of
    the NYC transportation status, such as which areas the accidences occur most, when the accidences mostly occur, which routine is more likely 
    to delay and so on. Besides, we can give the parents a good suggestion about when to send their children to school, which is very
    important to the parents.
    
4. Use the following command to run our program:
  python main.py <INTEGRATED-DATASET file name> <min_supp> <min_conf>
  For example, 
          python main.py INTEGRATED-DATASET.csv 0.5 0.7

4. Description of Internal Design:
    
    
5. An interesting sample run
    1. The command line specification
        python main.py INTEGRATED-DATASET.csv 0.5 0.7
        
    2. Explanations
    
6. Additional Information:

