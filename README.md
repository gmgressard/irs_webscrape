
# Coding Challenge: Find the Forms 


## Technologies Used

- Python 3.8.10
- Additional Modules Installed:
    - requests
    - bs4


## How to install

- Create virtual environment using commands:  
    - *virtualenv* *env*
    - *source* *env/bin/activate*
    - *pip3* *install* *-r* *requirements*


## How to use 

# Challege 1 
- Run *python3* *challenge1.py*
    - Follow prompts in command line 
    - Enter forms in as example:
        *Publ 1,Form W-2* 
- Output: JSON shown in terminal 

# Challenge 2
- Run *python3* *challenge1.py*
    - Follow prompts in command line 
    - Enter form in as example:
        *Publ 1*
    - Enter dates in as example:
        *2012-2020*
- Output: PDFs are downloaded with the title *form name - year* to subdirectory title the *form name* under main directory 