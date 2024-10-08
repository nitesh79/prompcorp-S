Download the requirements.txt file into your project folder and run this once you are inside your project folder in cmd. make sure to activate the virtual environment (eg: myenv/scripsts/activate)

-->  pip install -r requirements.txt

*******************************************************************************************************
*******************************************************************************************************

Inorder to run the project, make sure to install xampp cause project uses mysql for database
*******************************************************************************************************
Step 1.
*******************************************************************************************************
Open xampp shell and create following database and user.

1. open mariadb wth root account.
--> # mysql -u root
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 24
Server version: 10.4.32-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

2.check the existing database
--> MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| phpmyadmin         |
| test               |
+--------------------+
5 rows in set (0.001 sec)

3. user mysql which is already present in mariaDB
MariaDB [(none)]> use mysql
Database changed
MariaDB [mysql]>

4. create user and set password
MariaDB [mysql]> CREATE USER padmin@localhost IDENTIFIED BY '12345678';
Query OK, 0 rows affected (0.002 sec)
MariaDB [mysql]> select user from user;
+--------+
| User   |
+--------+
| root   |
| root   |
| padmin |
| pma    |
| root   |
| subash |
+--------+
6 rows in set (0.001 sec)

5. create database for django project
MariaDB [mysql]> CREATE DATABASE prompcorpdb;
Query OK, 1 row affected (0.002 sec)

MariaDB [mysql]>
MariaDB [mysql]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| phpmyadmin         |
| prompcorpdb        |
| test               |
+--------------------+
6 rows in set (0.001 sec)

6. assign all privilege to new database for admin 
MariaDB [mysql]> GRANT ALL PRIVILEGES ON prompcorpdb.* to padmin@localhost;
Query OK, 0 rows affected (0.004 sec)

MariaDB [mysql]>
