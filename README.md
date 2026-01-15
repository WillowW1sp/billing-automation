# Billing-Automation
Python script to compare a pdf of billing notices to a csv file of returned mail
and remove the duplicates from the pdf file


How to use:

>Install dependencies

```pip install -r requirements.txt```

>put necessary file in the same directory as the script 

```
billing.pdf 
billing.csv 
```
> billing.csv needs 
"First", 
"Last", 
and "Address" row titles to function 

>Run the script 

```python ./main.py```
