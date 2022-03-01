# Leetcode-Ranklist-Parser
It contains a scraper file that parses the entire Leetcode Contest Ranklist.

To execute:

```
     python3 leetcode_scraper.py [Enter your contest] [Enter your users in CSV file format]
```

Example Command:

```
     python3 leetcode_scraper.py weekly-contest-282 leetcode_users.csv
```

Command Line Arguments:

**1. Enter the contest you want: If contest is "Weekly Contest 281", give "weekly-contest-281" (It is not case sensitive, but hyphen is compulsory)**
    
**2. Enter the file of users you want ranklist from (Ensure it is in CSV format). The users must be listed on the first row of the file for reading.
    A preview is attached**

### The output will be written onto a CSV file named based on the contest argument entered.
### If you enter "weekly-contest-200", the CSV file will be weekly-contest-200.csv

### Preview Input:
![alt text](https://github.com/shubham11941140/Leetcode-Ranklist-Parser/blob/main/csvinput.PNG)

### Terminal Execution:
![alt text](https://github.com/shubham11941140/Leetcode-Ranklist-Parser/blob/main/terminaloutput.PNG)

### Output Ranklist on CSV File
![alt text](https://github.com/shubham11941140/Leetcode-Ranklist-Parser/blob/main/outputcsv.PNG)

#### This is very useful if you want to obtain the ranklist of multiple users (40-50) whose username is aldready on a Google Spreadsheet or CSV file.

#### It will give a sorted ranklist of the users in the input CSV file with all the data into another CSV file (Output), useful in college contests or 3rd party competitions.

#### Expected Execution Time: Less than 500 seconds (Approx 8-9 minutes).

## Concept Behind the Script:

Leetcode support CURL Requests which simplyfies the task of extracting the ranklist. You can use Beautiful Soup and Selenium Webdrivers which are efficient Web-Scraping Tools but it will ask you for Leetcode Access/Login Credentials. With this script you do not need anything.

The CURL Requests aldready have all access credentials and you don't need to add anything to the list. We will use HTTP GET requests from "Requests" Library of Python.

With the GET Requests, we can store the result into a JSON File. This file can be parsed and the data can be matched with the ranks that the users want (Specified by the
input CSV file).

We can obtain the results by matching the username of the needed users. With the ranking of all the needed users, we sort them by rank.

This is then written to an output CSV file. We can then verify the results as we please.



