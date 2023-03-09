# Guide to setup NGINX test environment

1. On your linux virtual machine, install the Nginx Web Server: <br>
   `sudo apt-get update` <br>
   `sudo apt-get install nginx` 
2. Install PHP for processing <br>
   `sudo apt-get install php-fpm php-mysql`
3. Configure the PHP processor <br>
   `sudo nano /etc/php/8.2/fpm/php.ini` <br>
   Find the line `cgi.fix_pathinfo` and uncomment it, setting the value to 0: <br>
   `cgi.fix_pathinfo=0`
4. Restart the php processor <br>
   `sudo systemctl restart php8.2-fpm`
5. Configure Nginx to use the PHP processor by copying and replacing the `default` file in the `nginx_test_env` folder into `/etc/nginx/sites-available/`
6. Change the `server_name` value in the `/etc/nginx/sites-available/default` folder to the IP of your own VM. <br>
   `sudo nano /etc/nginx/sites-availble/default`
7. Verify the configuration file has no syntax errors <br>
   `sudo nginx -t`
8. Copy and replace the `html` in the `nginx_test_env` folder into `/var/www/html`
9.  Reload Nginx and test that the website works. Note that your browser may cache the webpage, and using private browsing is recommended to verify the configurations of the webserver.<br>
   `sudo systemctl reload nginx`


## Debugging:
1. 502 Error: Please check that your configuration file `/etc/nginx/sites-available/default` has the correct value for the `server_name` variable
2. For Ubuntu, the php-fpm version installed is 8.1, therefore for all the steps above, please use php8.1 instead of php8.2. The `/etc/nginx/sites-available/default` file also has to be configured to use php8.1 instead of 8.2: <br>
   `fastcgi_pass unix:/run/php/php8.2-fpm.sock` to `fastcgi_pass unix:/run/php/php8.1-fpm.sock`