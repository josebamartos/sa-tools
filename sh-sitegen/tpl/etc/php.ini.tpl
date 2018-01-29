{# context = {'site_dir':site_dir, } #}
; Enable cgi.force_redirect for security reasons in a typical *Apache+PHP-CGI/FastCGI* setup
cgi.force_redirect=On

; Don't expose PHP
expose_php=Off

; Error display and logging
display_errors=Off
log_errors=On
;{{ site_dir }}/log/file.log

; Resource control
max_execution_time =  30
max_input_time = 30
memory_limit = 256M

; File uploads
file_uploads=On
upload_max_filesize = 256M
post_max_size = 256M
upload_tmp_dir="{{ site_dir }}/upload-tmp-dir"

; Session path
session.save_path="{{ site_dir }}/session"

; Disable remote code execution
allow_url_fopen = Off
allow_url_include = Off

; Disable dangerous functions
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source

; Jail the user in DocumentRoot
open_basedir = "{{ site_dir }}/public:{{ site_dir }}/session:{{ site_dir }}/upload-tmp-dir"