{# context = {'php_ini': php_ini, 'htpasswd': htpasswd, 'rw_cond_fqdn': rw_cond_fqdn, 'fqdn': fqdn} #}
# Custom php.ini
suPHP_ConfigPath {{ php_ini }}

# Enable Perl and Python interpreters
# AddHandler cgi-script .cgi .pl .py

# Disable Server Signature information
ServerSignature Off

# Disable directory listingindex
Options -Indexes

# Password protection
AuthUserFile "{{ htpasswd }}"
AuthType Basic
AuthName "Authorization required"
require valid-user

<IfModule mod_rewrite.c>
    RewriteEngine On

    # Force non-www:
    RewriteCond %{HTTP_HOST} ^www\.{{ rw_cond_fqdn }} [NC]
    RewriteRule ^(.*)$ http://{{ fqdn }}/$1 [L,R=301]

    # Force only GET and POST requests
    RewriteCond %{REQUEST_METHOD} ^(TRACE|DELETE|TRACK) [NC]
    RewriteRule .* - [F,L]
</IfModule>
