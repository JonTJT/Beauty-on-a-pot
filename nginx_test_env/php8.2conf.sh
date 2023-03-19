#!/bin/bash

rm /etc/php/8.2/fpm/pool.d/www.conf
cp www.conf /etc/php/8.2/fpm/pool.d/
systemctl restart php8.2-fpm