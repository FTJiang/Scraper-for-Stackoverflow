# Scraper-for-Stackoverflow
Master Student majored in Computer Engineering, seeking summer intern for 2017.
If you want to hire me or any questions, welcome to contact me by FJgithub@gmail.com

HOW IT WORKS  
The script work by scraping the html file of the question list page and extract question title and link by xpath. The data obtained will be stored in mysql database. When crawling process is finished, the script will make invert index automatically. You can make either one word query or phrase query.

INSTALLATION  
pip and virtualenv
```cmd
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv
```

following package can be installed in virtualenv and do not use sudo command
ntlk
```cmd
$ pip install -U nltk
$ nltk.download(‘maxent_treebank_pos_tagger’)   for pos_tag
$ nltk.download("stopwords")
$ nltk.download('averaged_perceptron_tagger')   for pos_tag
```

mysql
```cmd
$ apt-get update
$ apt-get install mysql-server
$ mysql_secure_installation
$ mysql_install_db
```

create database and table
```cmd
$ mysql -u root -p
$ CREATE DATABASE testdb;
$ CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'test623';
$ USE testdb;
$ GRANT ALL ON testdb.* TO 'testuser'@'localhost';
```

selenium
```cmd
$ pip install selenium
```
beautifulsoup
```cmd
$ pip install beatifulsoup
```

USAGE
You should change the username and password at first in scrapy.py line 30. This project is based on python 2.7.4, you can run command line: ```
python scraper.py```
