# amazon_price_tracker
An automated Python-based tracker that monitors Amazon product prices and sends email notifications when prices drop below your set target.
Built with **Selenium**, **SQLite**, and scheduled using **cron** for continuous background execution.


**Folder contains:**
	– .env (variables to be edited by user)
    – cron_job_schedule_format.png (picture detailing the format of a cron job)
    – requirements.txt (to install required dependencies)
    – scrap_amzn.py (the main program to track prices)
    – setup_db.py (first program to run that will create the database)


**Requirements**
	– Python 3.9+
	– Google Chrome, Microsoft Edge, or Safari (with remote automation allowed)
	– Environment variables (.env file)


**How to set up environment variable**
    **Note**: this will not work unless you have Multi-Factor Authentication (MFA) enabled for your account
    – In this project, we use the same email address as both the sender and the receiver
    – Log into your Google account and navigate to the Security Tab
    – In the Search bar, type "app" and click on "App passwords". You may need to enter your password
    – Give a name to your app and click "Create". A 16-character unique password will be generated
    – Copy the generated password and paste it into the .env file as the EMAIL_PASSWORD variable
	– Add your email address in the .env file as the EMAIL_ADDRESS variable


**Command-line installation**
1. Create a virtual environment
    – Windows: python.exe -m venv .venv
    – Linux/UNIX: python3 -m venv .venv

2. Activate the virtual environment
    – Windows: .venv\Scripts\activate
    – Linux/UNIX: source .venv/bin/activate
    
3. Install dependencies
    – Windows: python.exe -m pip install -r requirements.txt
    – Linux/UNIX: python3 -m pip install -r requirements.txt


**Set up the database**
1. Run setup_db.py and input the URL of your product, your target price, and a nickname for your product 
    – Windows: python.exe setup_db.py
    – Linux/UNIX: python3 setup_db.py
    **Note**: You can set the target price higher than the current price, just to verify the code works as intended
    
2. Next, run the scrap_amzn.py


**Setting up a cron job on a Linux environment with a shell script**
1. First, make sure the project is on the Linux machine and a virtual environment is set

2. Create a shell script file. e.g., `touch track.sh`

3. Open the script in your file editor: `nano track.sh` OR `vim track.sh`

4. Add the following lines to the file.
    #!/bin/bash
    source /full/path/to/project_directory/.venv/bin/activate
    python3 /full/path/to/project_directory/scrap_amzn.py

5. Save and exit the file. Then, add executable permission to the file. e.g, `chmod +x track.sh`

6. Make sure **crond** is enabled. Run `sudo systemstl status cron`
   – If it is not active, run `sudo systemctl enable cron` && `sudo systemctl start cron`.

7. Now, run `crontab -e` and add a new cron job with this format:
    e.g., 00 12 * * * /full/path/to/your/tracker.sh
    The script will be executed at 12PM every day of the month, every month, every day of the week

8. Check the cron job image file for more details.
