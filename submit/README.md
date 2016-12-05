# COMS6111-proj3

1. Group name: Project 3 Group 23
  Qi Wang (qw2197), Yongjia Huo (yh2796)

2. Submitted files:
    1. main.py -- the main program, implement the a-priori algorithm to extract association rules
    2. clean.py -- the program used to clean the data set
    3. INTEGRATED-DATASET.csv -- the cleaned data set we use to generate rules
    4. READEME.md
    
3. The detailed description of data set
    1. Which NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file:
      We choose the "Bus Breakdown and Delays" data set to generate the INTEGRATED-DATASET file
      
    2. What (high-level) procedure you used to map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file:
      We use the following filters when downloading data:
        * School_Year: 2016-2017
        * Number_of_Students_On_the_Bus > 0
        * Has_Contractor_Notified_Schools: Yes
        * Has_Contractor_Notified_Parents: Yes
        * Have_You_Alerted_OPT: Yes
        * School_Age_or_PreK: School-Age
        
        
      Then we extract the hour part from the "Occurred_On" column and reformat the "How_Long_Delayed" column. And we remove some columns which are unlikely to generate rules, keeping only the following columns in our final data set:
        * Route_Number	
        * Reason	
        * Occurred_On
        * Boro	
        * Bus_Company_Name	 
        * How_Long_Delayed	
        * Number_Of_Students_On_The_Bus	
        * Breakdown_or_Running_Late
      
      Note:
      There are some empty columns within the original file, we fill the empty slot in "Boro" column with "Others" and fill the
      empty slot in "How_Long_Delayed" columns with "-1" to indicate the data is unavailable.

    3. What makes your choice of INTEGRATED-DATASET file interesting:
    We choose this data set because we want to know when the bus breakdowns and delays happens, which is a good indication of the transportation condition in NYC. We can generate rules to know where and when the accidences occur most often, which routine is more likely to delay and so on. Besides, we can give students' parents suggestions like when should they send children to school to avoid heavy traffic.

    4. Use the following command to run our program:
    
         python main.py <INTEGRATED-DATASET> <min_supp> <min_conf>
           
       For example, 
      
         python main.py INTEGRATED-DATASET.csv 0.25 0.8

    5. Description of Internal Design:
    We follow exactly the implementation of a-priori algorithm described in Section 2.1 of the Agrawal and Srikant paper in VLDB 1994. The main steps are:
       1. Counts item occurrences to determine the large 1-itemsets.  
       2. Iteratively generate the large k-itemsets(denoted as L_k) from the large (k-1)-itemsets until (k-1)-itemsets is empty.
          * join L_k-1 with L_k-1 to return the set of all large k-itemsets, denoted as Ck
          * prune Ck to delete those itemsets not in L_k-1 
          * scan the database and count the support of candidates in Ck
          * L_k is the itemsets in Ck whose support is larger than the required minimum support 
    
    6. An interesting sample run
      1. The command line specification
      
         python main.py INTEGRATED-DATASET.csv 0.25 0.8

      2. Explanations
          Some interesting rules:
          1. [07 O'Clock, Heavy Traffic] => [Running Late] -- (Conf: 100.0 %  Supp: 49.3277927157 %)
             [07 O'Clock] => [Running Late] -- (Conf: 97.5080385852 %  Supp: 59.3009044243 %)
             [07 O'Clock, Running Late] => [Heavy Traffic] -- (Conf: 83.1821929101 %  Supp: 49.3277927157 %)
             [07 O'Clock] => [Heavy Traffic] -- (Conf: 81.1093247588 %  Supp: 49.3277927157 %)
             
             7 O'Clock is the busiest time in a day and bus delays are more likely to happen at this time
             
          2. [20 MIN] => [Running Late] -- (Conf: 100.0 %  Supp: 26.5949645563 %)
             
             most delays are 20-minute late
          
          3. [Bronx] => [Running Late] -- (Conf: 97.9981801638 %  Supp: 26.3260816426 %)
             [Manhattan] => [Running Late] -- (Conf: 96.4511041009 %  Supp: 29.8948912246 %)
             
             traffic in Bronx and Manhattan is worse than other boroughs.
            
          4. [RELIANT TRANS, INC. , Running Late] => [Heavy Traffic] -- (Conf: 95.0184501845 %  Supp: 25.177218284 %)
             [RELIANT TRANS, INC. ] => [Running Late] -- (Conf: 91.1690496215 %  Supp: 26.4971889514 %)
             [RELIANT TRANS, INC. ] => [Heavy Traffic] -- (Conf: 86.6274179983 %  Supp: 25.177218284 %)
             
             buses from RELIANT TRANS, INC. are more likely to delay because of heavy traffic. From Google reviews we also find that this company only gets a rating of 2.6, and people complain that they don't come on time. 

