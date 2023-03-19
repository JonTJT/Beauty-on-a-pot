#!/bin/bash

if [ ! -f "~/.bash_aliases" ]; then
    touch ~/.bash_aliases
fi
if [ ! -f "/usr/local/openresty/nginx/logs/honeypot.log" ]; then
    touch /usr/local/openresty/nginx/logs/honeypot.log
fi
echo "alias hptlog='cat /usr/local/openresty/nginx/logs/honeypot.log'" >> ~/.bash_aliases
echo "Alias done, use hptlog to see honeypot logs, if any have been created."
echo "Might need to start a new shell for shortcut to work."
