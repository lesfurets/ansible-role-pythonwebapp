Python webapp
=========

[![Build Status](https://travis-ci.org/lesfurets/ansible-role-pythonwebapp.svg?branch=master)](https://travis-ci.org/lesfurets/ansible-role-pythonwebapp)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ansible Galaxy: lesfurets.pythonwebapp](https://img.shields.io/badge/galaxy-lesfurets.pythonwebapp-blueviolet.svg)](https://galaxy.ansible.com/lesfurets/pythonwebapp)

Ansible role to install python web applications (django, flask...) and setup uwsgi/nginx to expose the app.

## Requirements

Your app must be in **a git repository** and have a **requirements.txt** file (which include wsgi) and have a **wsgi.py** file and a **.ini** conf file.

## Dependencies

Role **lesfurets.nginx** and **lesfurets.python3** alongside their own dependencies.

## Role Variables

### Python webapp vars

- **webapp_name**: is the name of the app to deploy. It is also used as the systemd service name.
- **webapp_dest_folder**: is the installation folder on the target host.
- **webapp_repo_url**: is the git repository where your webapp source is hosted.
- **webapp_scm_revision**: is the tag/branch to use on the git clone. Default is HEAD, but it is highly advised to change it to a tag to avoid unwanted changes.
- **webapp_requirements**: is the path of the pip requirements file on the target host.
- **webapp_ini_file**: is the path of the uWSGI ini file on the target host.
- **webapp_settings_file_path**: is the local path for a potential settings file.
- **webapp_user**: *Optional*, is an **existing user** used to run uwsgi and own the project files.

### Nginx related vars

Do not forget to setup the Nginx related vars depending on you uwsgi **.ini** file.
Here is a basic example:

```
nginx_remove_default_vhost: true
nginx_vhosts:
  - listen: "80"
    server_name: "mywebapp.com"
	locations:
	  - location: "/"
	    include: "uwsgi_params"
        uwsgi_pass: "unix://{{ webapp_dest_folder }}/demo.sock"
```

## Example Playbook

```
- hosts: webapp
  vars:
    webapp_repo_url: "https://github.com/lesfurets/demo-flask-uwsgi.git"
    webapp_scm_revision: "v2"
    webapp_ini_file: "{{ webapp_dest_folder }}/demo.ini"
    webapp_settings_file_path: "settings.py"
    webapp_user: "webapp"
    nginx_capable_user: "webapp"
    nginx_remove_default_vhost: true
    nginx_vhosts:
      - listen: "80"
        server_name: "mywebapp.com"
        locations:
          - location: "/"
            include: "uwsgi_params"
            uwsgi_pass: "unix://{{ webapp_dest_folder }}/demo.sock"
  tasks:
    - name: create webapp user
      user:
        name: webapp
        state: present
    - name: setup webapp
      import_role:
        name: lesfurets.pythonwebapp
```

## License

Licensed unter the GPLv3 License. See LICENSE file for details.
