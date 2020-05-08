sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
#sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
#sudo /etc/init.d/gunicorn restart
gunicorn --bind='0.0.0.0:8080' hello:application &
gunicorn --bind='0.0.0.0:8000' ask.wsgin &
#sudo ln -s /home/box/web/etc/gunicorn.conf   /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn restart
#sudo /etc/init.d/mysql start
#git clone https://github.com/KozyarValeriy/Web_application.git /home/box/web
#bash /home/box/web/init.sh