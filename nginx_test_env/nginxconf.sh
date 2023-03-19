#!/bin/bash

rm -r /usr/local/openresty/nginx/html
#cp nginx.conf /usr/local/openresty/nginx/conf
cp -r html/ /usr/local/openresty/nginx/
systemctl restart openresty