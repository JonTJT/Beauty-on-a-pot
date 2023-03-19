import re, os

def test():
    # Set expected php path to check for
    PHP_DIR = '/etc/php/8.2/fpm'

    # Set the path to the Nginx config file
    CONFIG_FILE = '/usr/local/openresty/nginx/conf/nginx.conf'

    # Define the string to insert for log_format
    LOG_FORMAT_STRING = '''    log_format log_req escape=none '[$time_local] $remote_addr $remote_port $server_addr $server_port'\n    '\\n$request$req_header$request_body\\n|\\n';\n\n'''

    # Define the  string to insert for lua processing
    LUA_STRING = '''
        lua_need_request_body on;

        set $req_header "\\n";
        header_filter_by_lua_block {
        local h = ngx.req.get_headers()
        for k, v in pairs(h) do
                if (type(v) == "table") then
                ngx.var.req_header = ngx.var.req_header .. k.."="..table.concat(v,",").."\\n"
                else
                ngx.var.req_header = ngx.var.req_header .. k.."="..v.."\\n"
                end
        end
        }\n\n'''

    # Define the string to insert for location
    LOCATION_STRING = '''
        location = /process_login.php {
            fastcgi_pass unix:/run/php/php8.2-fpm.sock;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;

            access_log logs/honeypot.log log_req;
        }

        location = /process_search.php {
            fastcgi_pass unix:/run/php/php8.2-fpm.sock;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;

            access_log logs/honeypot.log log_req;
        }
    '''

    # Check if php version is correct
    if not os.path.isdir(PHP_DIR):
        print('Please confirm if php8.2 is installed. If the version of php used is not 8.2, please edit this script to reflect the correct version.')
        exit(0)

    # Create a backup nginx.conf file
    if not os.path.isfile('/usr/local/openresty/nginx/conf/nginx.conf.backup'):
        os.system('cp /usr/local/openresty/nginx/conf/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf.backup')
        print('Backup created as /usr/local/openresty/nginx/conf/nginx.conf.backup.')

    # Use awk to find the http block and insert the strings
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()

    with open(CONFIG_FILE + '.tmp', 'w') as f:
        in_http_block = False
        in_server_block = False
        in_location_block = False
        http_write = False
        server_write = False
        location_write = False
        for line in lines:
            if 'http {' in line and not http_write:
                in_http_block = True
                http_write = True
                f.write(line)
                f.write(LOG_FORMAT_STRING)
            elif 'server {' in line and not server_write:
                in_server_block = True
                server_write = True
                f.write(line)
                f.write(LUA_STRING)
            elif 'location /' in line:
                in_location_block = True
                f.write(line)
            elif in_location_block and '}' in line and not location_write:
                in_location_block = False
                f.write(line)
                f.write(LOCATION_STRING)
                location_write = True
            # elif in_http_block or in_server_block or in_location_block:
            #     pass
            else:
                f.write(line)

    # Overwrite the original config file with the modified version
    os.system('mv ' + CONFIG_FILE + '.tmp ' + CONFIG_FILE)


def main():
    test()

main()