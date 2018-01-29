#!/usr/bin/env python
import argparse
import crypt
import fnmatch
import jinja2
import random
import re
import os


def find_by_unix_pattern(ext, path):
    result = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, ext):
            result.append(os.path.join(root, filename))
    return result


def fix_path(path):
    return path if path.startswith("./") or path.startswith("/") else os.path.join("./", path)


def mkpasswd(length):
    password = ""

    for i in range(0, length):
        password += chr(random.randint(33, 126))

    return password


def mkfile_from_tpl(src, dst, ctx):
    file_body = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(src) or "./")).get_template(os.path.basename(src)).render(ctx)
    with open(dst, "w") as text_file:
        text_file.write(file_body)


def dir_list(path):
    directories = []
    for root in os.walk(path):
        if root != ".":
            directories.append(root)
    return directories


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description = "Site structure generator for shared hosting")
    parser.add_argument("-d", "--dryrun",   required=False,                             help="Run in read-only mode")
    parser.add_argument("-f", "--fqdn",     required=True,                              help="FQDN of the site")
    parser.add_argument("-t", "--tpl_dir",  required=False, default="./tpl",            help="Directory containing templates")
    parser.add_argument("-u", "--username", required=False, default=os.environ["USER"], help="Username for Basic Authentication")
    parser.add_argument("-p", "--password", required=False, default=mkpasswd(8),        help="Password for Basic Authentication")

    # User defined variables
    args     = parser.parse_args()
    password = args.password
    tpl_dir  = fix_path(args.tpl_dir)

    # Template variables
    fqdn         = args.fqdn                                        # <tpl_dir>/public/.htaccess.tpl
    rw_cond_fqdn = args.fqdn.replace(".", "\.")                     # <tpl_dir>/public/.htaccess.tpl
    site_dir     = os.path.join(os.environ["HOME"], "sites", fqdn)  # <tpl_dir>/etc/php.ini.tpl
    php_ini      = os.path.join(site_dir, "etc", "php.ini")         # <tpl_dir>/public/.htacces.tpl
    htpasswd     = os.path.join(site_dir, "htpasswds", "passwd")    # <tpl_dir>/public/.htacces.tpl
    title        = fqdn                                             # <tpl_dir>/public/{index.html, index.php}
    body         = fqdn                                             # <tpl_dir>/public/{index.html, index.php}
    username = args.username                                        # <tpl_dir>/htpasswds/passwd
    hash = crypt.crypt(args.password, "salt")                       # <tpl_dir>/htpasswds/passwd

    # Welcome message
    print "\r\nCreating site " + fqdn

    # Directory structure creation
    print "\r\nCreating directory structure in " + site_dir

    for directory in dir_list(tpl_dir):
        directory = directory[0].replace(tpl_dir, site_dir)
        if os.path.exists(directory):
            print "Directory " + directory + " already exists. Omiting."
        else:
            print "Creating directory: " + directory
            os.makedirs(directory)

    # Writing files
    print "\r\nWriting files in " + site_dir

    for template in find_by_unix_pattern("*.tpl", tpl_dir):
        with open(template, "r") as f:
            dst = os.path.join(site_dir, re.search("^" + tpl_dir + "/(.*).tpl$", template).group(1))
            ctx = eval(re.search("^{# context = (.*) #}", f.readline().strip()).group(1))
            print "Writing file: " + dst
            mkfile_from_tpl(template, dst, ctx)

    print ""
    print "Site " + fqdn + " created"
    print " * Path: " + site_dir
    print " * Apache username: " + username
    print " * Apache password: " + password
    print ""


if __name__ == "__main__":
    main()