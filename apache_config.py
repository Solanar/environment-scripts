# generates an apache config file

try:
    import settings
except ImportError:
    raise Exception('Create settings.py with sensitive settings defined')


if __name__ == '__main__':
    # args could be in an OrderedDict
    print('\n* Required args *\n')

    print('url: ', end='')
    url = input()
    if not url:
        exit('Enter an url')

    print('git_dir: ', end='')
    git_dir = input()
    if not git_dir:
        exit('Enter a git_dir')

    print('\n* Optional args (leave blank to use defaults) *\n')

    print('proj_dir (default is ' + git_dir + '): ', end='')
    proj_dir = input()
    if not proj_dir:
        proj_dir = git_dir

    print('venv (default is venv_' + proj_dir + '): ', end='')
    venv = input()
    if not venv:
        venv = 'venv_' + proj_dir

    default_user = settings.USER
    print('user (default is ' + default_user + '): ', end='')
    user = input()
    if not user:
        user = default_user

    print('favicon (leave blank to disable): ', end='')
    favicon = input()

    default_python_ver = '3.4'
    print('python_ver (default is ' + default_python_ver + '): ', end='')
    python_ver = input()
    if not python_ver:
        python_ver = default_python_ver

    print('server_alias (leave blank to disable): ', end='')
    server_alias = input()

    default_email = settings.EMAIL
    print('email (default is ' + default_email + '): ', end='')
    email = input()
    if not email:
        email = default_email

    print('ssl (enter [y]es or leave blank to disable): ', end='')
    ssl = input().lower()

    # Could be moved to a text file
    apache_template = '''
<VirtualHost *:80>
    ServerName <url>
    <server_alias_opt>ServerAlias <server_alias>
    ServerAdmin <email>

    <favicon_opt>Alias /favicon.ico /home/<user>/public_html/<url>/<git_dir>/static/<favicon>

    Alias /media/ /home/<user>/public_html/<url>/<git_dir>/media/
    Alias /static/ /home/<user>/public_html/<url>/<git_dir>/static/

    <Directory /home/<user>/public_html/<url>/<git_dir>/static>
        Require all granted
    </Directory>
    <Directory /home/<user>/public_html/<url>/<git_dir>/media>
        Require all granted
    </Directory>

    WSGIScriptAlias / /home/<user>/public_html/<url>/<git_dir>/<proj_dir>/wsgi.py
    WSGIDaemonProcess <url> python-path=/home/<user>/public_html/<url>/<git_dir>:/home/<user>/public_html/<url>/<venv>/lib/python<python_ver>/site-packages
    WSGIProcessGroup <url>

    <Directory /home/<user>/public_html/<url>/<git_dir>/<proj_dir>>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</Virtualhost>
'''  # noqa E501

    if server_alias:
        apache_template = apache_template.replace(
            '<server_alias>', server_alias
        ).replace(
            '<server_alias_opt>', ''
        )
    else:
        apache_template = apache_template.replace('<server_alias_opt>', '#')

    if favicon:
        apache_template = apache_template.replace(
            '<favicon>', favicon
        ).replace(
            '<favicon_opt>', ''
        )
    else:
        apache_template = apache_template.replace('<favicon_opt>', '#')

    apache_template = apache_template.replace(
        '<url>', url
    ).replace(
        '<email>', email
    ).replace(
        '<user>', user
    ).replace(
        '<git_dir>', git_dir
    ).replace(
        '<proj_dir>', proj_dir
    ).replace(
        '<venv>', venv
    ).replace(
        '<python_ver>', python_ver
    )

    if ssl == 'y' or ssl == 'yes':
        exit('ssl not implemented')

    # print(apache_template)
    filename = url + '.conf'
    f = open(filename, 'w')
    f.write(apache_template)
    f.close()
    print('Created file: ' + filename)