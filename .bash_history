virtualenv ~/.venv
source ~/.venv/bin/activate
pip install -U pip setuptools
pip install indico
indico setup wizard
mkdir ~/log/apache
chmod go-rwx ~/* ~/.[^.]*
chmod 710 ~/ ~/archive ~/assets ~/cache ~/log ~/tmp
chmod 750 ~/web ~/.venv
chmod g+w ~/log/apache
echo -e "\nSTATIC_FILE_METHOD = 'xsendfile'" >> ~/etc/indico.conf
indico db prepare
exit
cd etc
ls
nano indico.conf
cd ..
touch /opt/indico/web/indico.wsgi
indico setup list_plugins
exit
source ~/.venv/bin/activate
pip install indico-plugins
indico setup list_plugins
cd /opt/indico/etc/indico.conf
nano /opt/indico/etc/indico.conf
indico db --all-plugins upgrade
touch ~/web/indico.wsgi
systemctl restart indico-celery.service
exit
nano /opt/indico/etc/indico.conf
indico db --all-plugins upgrade
source ~/.venv/bin/activate
indico db --all-plugins upgrade
touch ~/web/indico.wsgi
nano /opt/indico/etc/indico.conf
indico db --all-plugins upgrade
touch ~/web/indico.wsgi
nano /opt/indico/etc/indico.conf
touch ~/web/indico.wsgi
exit
ls
indico
psql 
exit
psql
exit
psql
indico
source ~/
source ~/.venv/bin/activate
pwd
pwdindico
psql
history
service apache2 status
exit
history
history --help
history
exit
psql
cd /var/www/
ls
cd html/
ll
ls#
ls
git init
sudo apt-install git
exit
