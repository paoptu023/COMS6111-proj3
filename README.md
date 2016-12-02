# COMS6111-proj3

1. Group name: Project 3 Group 23
  Qi Wang (qw2197), Yongjia Huo (yh2796)

2. Submitted files:
    1. main.py -- the main program, implement the a-priori algorithm to extract association rules
    2. clean.py -- the program used to clean the data set
    3. Bus_Breakdown_and_Delays.csv -- the original data set
    4. bus.csv -- the cleaned data set we use to generate rules
    5. READEME.md
    
3. The detailed description of data set
    1. Which NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file:
      We choose the "Bus Breakdown and Delays" data set to generate the INTEGRATED-DATASET file
      
    2. What (high-level) procedure you used to map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file:
      We use the following filters to get the "Bus_Breakdown_and_Delays.csv" from the original data:
        * School_Year: 2016-2017
        * Run_Type: Special Ed AM Run or Special Ed AM Run
        * Number_of_Students_On_the_Bus > 0
        * Has_Contractor_Notified_Schools: Yes
        * Has_Contractor_Notified_Parents: Yes
        * Have_You_Alerted_OPT: Yes
        * Has_Contractor_Notified_Schools: Yes
        * School_Age_or_PreK: School-Age
        
        
      Then we extract the hour part from the "Occurred_On" column and reformat the "How_Long_Delayed" column. And we remove some columns which are unlikely to generate rules, keeping only the following columns in our final data set:
        * Route_Number	
        * Reason	
        * Schools_Serviced	
        * Occurred_On
        * Boro	
        * Bus_Company_Name	 
        * How_Long_Delayed	
        * Number_Of_Students_On_The_Bus	
        * Breakdown_or_Running_Late
        
    3. What makes your choice of INTEGRATED-DATASET file interesting:
    We choose this data set because we want to know when the bus breakdowns and delays happens, which is a good indication of the transportation condition in NYC. We can generate rules to know where and when the accidences occur most often, which routine is more likely to delay and so on. Besides, we can give students' parents suggestions like when should they send children to school to avoid heavy traffic.

    4. Use the following command to run our program:
    
         `python main.py <INTEGRATED-DATASET> <min_supp> <min_conf>`
           
       For example, 
      
         `python main.py bus.csv 0.25 0.8`

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
      
         `python main.py bus.csv 0.25 0.8`

      2. Explanations
          Some interesting rules:
          1. [07 O'Clock, Heavy Traffic] => [Running Late] -- (Conf: 100.0 %  Supp: 51.652354931 %)
             [07 O'Clock] => [Running Late] -- (Conf: 97.4662852472 %  Supp: 62.0608899297 %)
             [07 O'Clock, Running Late] => [Heavy Traffic] -- (Conf: 83.2285115304 %  Supp: 51.652354931 %)
             [07 O'Clock] => [Heavy Traffic] -- (Conf: 81.1197384553 %  Supp: 51.652354931 %)
             
             7 O'Clock is the busiest time in a day and bus delays are more likely to happen at this time
             
          2. [15 MIN] => [Running Late] -- (Conf: 100.0 %  Supp: 25.5009107468 %)
             [20 MIN] => [Running Late] -- (Conf: 100.0 %  Supp: 26.9581056466 %)
             
             most delays are 15-minute or 20-minute late
          
          3. [Bronx] => [Running Late] -- (Conf: 98.7317073171 %  Supp: 26.3335935467 %)
             [Manhattan] => [Running Late] -- (Conf: 97.3487986744 %  Supp: 30.5750715587 %) 
             
             traffic in Bronx and Manhattan is worse than other boroughs.
            
          4. [RELIANT TRANS, INC. , Running Late] => [Heavy Traffic] -- (Conf: 95.1520912548 %  Supp: 26.0473588342 %)
             [RELIANT TRANS, INC. ] => [Running Late] -- (Conf: 93.6776491541 %  Supp: 27.3744470466 %)
             [RELIANT TRANS, INC. ] => [Heavy Traffic] -- (Conf: 89.1362422084 %  Supp: 26.0473588342 %) 
             
             buses from RELIANT TRANS, INC. are more likely to delay because of heavy traffic. From Google reviews we also find that this              company only gets a rating of 2.6, and people complain that they don't come on time. 
    
    7. Additional Information:

