# Guide to setup NGINX test environment with OpenResty
For enhanced logging to grab all request headers with Lua, certain modules are included. Instead of manually installing the modules, it is required to use OpenResty, a wrapper around Nginx, as it comes packaged and properly configured to use the needed modules. This test environment is using Ubuntu 22.04 and PHP 8.2, which is also highly recommended to avoid errors.

1. On your Ubuntu 22.04 machine, install OpenResty: <br>
   `sudo systemctl disable nginx`<br>
   `sudo systemctl stop nginx`<br>
   `sudo apt-get -y install --no-install-recommends wget gnupg ca-certificates`<br>
   `wget -O - https://openresty.org/package/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/openresty.gpg`<br>
   `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/openresty.gpg] http://openresty.org/package/ubuntu $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/openresty.list > /dev/null`<br>
   `sudo apt-get update`<br>
   `sudo apt-get -y install openresty`
2. Install php 8.2<br>
   `sudo add-apt-repository ppa:ondrej/php`<br>
   `sudo apt-get update`<br>
   `sudo apt-get install php-fpm php-mysql`<br>
3. Copy the *nginx-test-env* directory from this git repo into your Ubuntu, and open a terminal in this directory.<br>
4. Run *php8.2conf.sh* to fix a compatibility issue with OpenResty and PHP<br>
   `sudo php8.2conf.sh`<br>
5. **(Optional)** If you would like to set up a test environment, run nginxconf.sh<br>
   `sudo nginxconf.sh`<br>
6. **(Optional)** Alternatively, if you want to use existing files, please copy them into the */usr/local/openresty/nginx/html/* directory.<br>
   `cp *.php /usr/local/openresty/nginx/html/`<br>

## Debugging:
To be updated.