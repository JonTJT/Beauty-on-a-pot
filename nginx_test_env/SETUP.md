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
6. Verify the configuration file has no syntax errors <br>
   `sudo nginx -t`
7. Copy and replace the `html` in the `nginx_test_env` folder into `/var/www/html`
8. Reload Nginx and test that the website works. Note that your browser may cache the webpage, and using private browsing is recommended to verify the configurations of the webserver.<br>
   `sudo systemctl reload nginx`
