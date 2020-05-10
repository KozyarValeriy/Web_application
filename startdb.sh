sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS testdb;"
mysql -uroot -e "CREATE USER 'kozyar'@'localhost' IDENTIFIED BY 'qwerty';"
mysql -uroot -e "GRANT ALL ON testdb.* TO 'kozyar'@'localhost';"
python3 ask/manage.py migrate