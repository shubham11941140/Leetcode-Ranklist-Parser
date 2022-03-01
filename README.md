# Leetcode-Ranklist-Parser
It contains a scraper file that parses the entire Leetcode Contest Ranklist.

To execute:

```
    python3 leetcode_scraper.py weekly-contest-282 leetcode_users.csv
```

Command Line Arguments:


    1. Enter the contest you want: If contest is "Weekly Contest 281", give "weekly-contest-281" (It is not case sensitive, but hyphen is compulsory)
    
    2. Enter the file of users you want ranklist from (Ensure it is in CSV format). The users must be listed on the first row of the file for reading.
    A preview is attached


#### This is very useful if you want to obtain the ranklist of multiple users (40-50) whose username is aldready on a Google Spreadsheet or CSV file.

#### It will give a sorted ranklist of the users in the input CSV file with all the data into another CSV file (Output), useful in college contests or 3rd party competitions.

#### Expected Execution Time: Less than 500 seconds.
