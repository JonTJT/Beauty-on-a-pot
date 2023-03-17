# Guide to setup Apache test environment

1. On your linux virtual machine, install the Apache Web Server: <br>
   `sudo apt-get update` <br>
   `sudo apt-get install apache2` 
   
2. Change the `ServerName` variable in the `/etc/apache2/apache2.conf` file: <br>
   `ServerName your_ip_address` <br>
   
   If there is no ServerName variable, add it to the bottom of the configuration file.
   
3. Install PHP for processing <br>
   `sudo apt-get install php libapache2-mod-php php-mysql`
   
4. Configure the apache `dir.conf` file <br>
   `sudo nano /etc/apache2/mods-enabled/dir.conf` <br>
   Look for the `DirectoryIndex` value. It should look like this:
   
   ```
   <IfModule mod_dir.c>
      DirectoryIndex index.html index.cgi index.pl index.php index.xhtml index.htm
   </IfModule>
   ```
   Change it to:
   ```
   <IfModule mod_dir.c>
      DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
   </IfModule>
   ```
   
5. Verify that the configuration file has no syntax errors: <br>
   `sudo apache2ctl configtest`<br>
   
   If there are no syntax errors, you should see this output: <br>
   
   ```
   Output
   Syntax Ok
   ```
   
6. Copy and replace the `html` folder in the `apache_test_env` folder into `/var/www/html`

7.  Restart Apache and test that the website works. Note that your browser may cache the webpage, and using private browsing is recommended to verify the configurations of the webserver.<br>
   `sudo systemctl restart apache2`


## Debugging:
1. 502 Error: Please check that your configuration file `/etc/apache2/apache2.conf` has the correct value for the `ServerName` variable
