import os
from distutils.dir_util import copy_tree

def normalize(name):
    return name.replace('-', '_')

class Config(str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)
_ = Config

project_slug = _("my-cool-project")
cleaned_project_slug = _(normalize(project_slug))

# The main app name (name of the folder containing the settings.py)
main_app_name = _(cleaned_project_slug)

# The domain name for nginx virtual host and letsencrypt certs - you still have to add it
# to the allowed hosts below
domain_name = _("")

# The project will be put inside this directory in the container: /home/<this variable>/
project_container_root_folder = _(project_slug)

# Whatever you put here goes after a "git clone ..." from your deployment server. So if you use
# ssh make sure your server has access to the repo via ssh. This is only used for the deployment process.
repo_clone_address = _("https://github.com/...")

# The folder on server to clone the repo in (relative to ~). Another folder will be created inside 
# this folder and the project will be cloned there. (the inner folder will be called "repo")
server_deploy_folder = _("my-project")

######################## Dev environment ###########################

# The dev project secret key (this is SECRET_KEY in django settings)
dev_secret_key = _("RANDOM STRING...")

# ALLOWED_HOSTS in django settings for dev
dev_allowed_hosts = _(' '.join(["localhost", "127.0.0.1", "[::1]"]))

# Postgres db name for dev environment
dev_db_name = _(cleaned_project_slug)
# Choose a username and password
dev_db_username = _("")
dev_db_password = _("")


######################## Product environment ###########################

# The production secret key (this is SECRET_KEY in django settings)
prod_secret_key = _("RANDOM STRING...")

# ALLOWED_HOSTS in django settings for production
prod_allowed_hosts = _(' '.join([]))

# Postgres db name for prod environment
prod_db_name = _(cleaned_project_slug)
# Choose a username and password
prod_db_username = _("")
prod_db_password = _("")

# This goes into .gitignore - you probably won't need to change it
prod_env_gitignore_files = _(".env.prod*")

# The default email on certificates - goes in .env.prod.acme-companion
cert_email = _("")

if __name__ == '__main__':
    replacements = {
        name: value for name, value in vars().copy().items()
        if type(value) == Config
    }
    for key, val in replacements.items():
        if val == '':
            raise ValueError(f'{key} setting cannot be empty.')

    output_folder = f"output_{replacements['project_slug']}"
    copy_tree("django-project-template", output_folder)
    os.rename(f'{output_folder}/src/main_app_name', f'{output_folder}/src/{replacements["main_app_name"]}')
    for dname, dirs, files in os.walk(output_folder):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            for key, val in replacements.items():
                s = s.replace(f"%%{key}%%", str(val))
            with open(fpath, "w") as f:
                f.write(s)
