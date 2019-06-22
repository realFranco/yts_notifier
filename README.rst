=======================
YTS Notifier
=======================

.. image:: https://img.shields.io/badge/python-3.6%2B-blue.svg?style=for-the-badge&logo=appveyor
   :alt: Supported Python Versions


===========
Description
===========
Script that collect's movies description title/images from the web and if necessary, send notifications by email message, using **AWS Simple Email Service**. This script running  in a automaticly way. Just need **user interaction on the first running**. The rest of the time will run on the user's crontab, managed by the operating system (running constantly with no user interaction).


=============
Requeriments
=============
If you can check that the current system has **gcc**, you can avoid the step 0.

0. Open a terminal and write:
    
    .. code-block:: console
    
        $: gcc --version
        $: # Some text about the gcc version.

    If you check some errors, write the next lines in the current terminal/bash

    .. code-block:: console

        #
        # If you are using a Fedora Linux
        #
        $: sudo yum groupinstall -y 'development tools'
        $: sudo yum install python3-devel
        #
        # If you are using a Ubuntu Linux
        #
        $: sudo apt-get install build-essential
        $: sudo apt-get install python3-dev


The next requirements are include into the **requeriments.txt** file inside of the repository

1. scrapy 1.5.x

2. python-crontab

3. boto3

============
Dependencies
============
Can donwload the dependencies using:

.. code-block:: console

   $: pip install -r requeriments.txt

============
Instructions
============
**Important: This will gonna work only if you have a amazon SES credentials and be able to use this service.**

1. Donwload the repository making a **git clone repo_route_**.

2. Configure **Selenium** on the the operative system. Preferably, UNIX operative system (Linux distributions & MAC).
  
    2.1. Go to https://pypi.org/project/selenium/, read the **Driver** section and follow instructions.

3. Authorize the **Amazon SES service**.  

    3.1 Go to https://aws.amazon.com/ses/getting-started/ for start to use this service.

4. Modified **ses_atributes.json** file. Check bellow.

================================
Configuring Selemiun Web Driver.
================================
1. Go to https://pypi.org/project/selenium/, read the **Driver** section and follow instructions.

=============================
How to modify the .json file?
=============================
1. The project main file (yts_notifier.py) need **Environment Variables of the System**

    1.1 In a UNIX console, edit the .bashrc file:
       
    .. code-block:: console
       
        $: sudo nano ~/.bashrc

    1.2 In the bottom of the file, add a varible, with this syntax:
    
    .. code-block:: console
    
        export VariableName=Value

    1.3 Save & Close the editor and write the next line inside of the current terminal/bash to apply the changes:
    
    .. code-block:: console
    
        $ : source ~/.bashrc

    1.4 To watch the variable, write the next line into the terminal:
  
    .. code-block:: console
   
           $: $VariableName
           $: Value 
   
    1.5 If your variables do not be saved after reboot the system or reopen the terminal. Then, do the manually way in the step 2.

2. **All values are REQUIRED**.

====================================
Example of the email_conf.json file.
====================================

.. code-block:: python

    {
      "Source"        : "me@example.com",
      "TemplateName"  : "Template", 
      "Subject"       : "Example Subject", 
      "HtmlSource"    : "/file.html",
      "Recipents"     : ["recipent1", "recipient2", ..., "recipentN"],
      "ReplyTo"       : "me@example.com",
      "AWSReg"        : ""
    }
