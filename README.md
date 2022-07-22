# What is this?
This scaffolder generates a containerized Django project with the given config ready to be deployed using gunicorn. It also uses Letsencrypt to provide SSL on the given domain name. Github Actions is used for the deployment pipeline and you'll need to put a few secrets in your pipeline to make it happen.

### Prefer a quick demo video?
[![Demo Video](https://img.youtube.com/vi/DteRpg62hn8/0.jpg)](https://www.youtube.com/watch?v=DteRpg62hn8)

# Starting a project
1. Clone this repo on your local then copy the `startproject.py` and give the copy a name - the name does not matter, we make the copy to keep the original unchanged in case we need to get back to it.
2. Enter this new file (which from now on we'll call `project.py`) and set the value for all the variables wrapped in a `_("...value...")`. They all have enough comments but there is also a full list of them along with descriptions below in this document.
3. Run this file `python3 project.py` - it might raise a few errors if some variables aren't assigned yet; in which case, you must assign them. Otherwise it will give you a folder which will be your new Django project!
4. Enter the folder and run `docker-compose up` to make sure everything's working fine. You should be able to see the admin page at `localhost/admin`.
5. Put this folder on a Github repo and it will start a Github Actions job to deploy it - which will of course fail because we haven't set the secrets needed inside our pipeline.
6. Go to your repo settings -> Security tab -> Secrets -> Actions and add these secrets to "Repository Secrets":
- **HOST**: The IP of the server you want to deploy your project on (should be a linux machine).
- **USERNAME**: Username to login to on the host machine.
- **SSH_KEY**: The SSH key to use for logging into the username on the host.
- **ENV_PROD**: The contents of the `.env.prod` file in the project folder (this should be base64 encoded - see below).
- **ENV_PROD_DB**: The contents of the `.env.prod.db` file which should be encoded as above.
- **ENV_PROD_ACME_COMPANION**: The contents of the `.env.prod.acme-companion` file encoded like other env files.
7. That should be it!

#### Encoding the env files before putting inside repo secrets
Run this command to encode the env files:
```
base64 -i .env.prod (and the other prod files...)
```
Then copy the output and put it in the appropriate variable.

# Notes
- Server machine needs to have docker and docker-compose installed.
- If your repo is private then your server machine needs to have access to the repo (you can do this with repo settings on Github - look it up online).
- You cannot deploy multiple projects on the same host (unless you define all of them in the same docker-compose file).

# All Config Vars
- `project_slug`: A title for the project which will be used to create its folder. Preferably don't use spaces or any other non standard characters.
- `cleaned_project_slug`: This is supposed to be a safe version of the project slug. It will be used to identify your project everywhere: in docker containers, folder names, volumes, etc.. By default it uses the same value from `project_slug` and just replaces `-`s with `_`s but you can change it to whatever you want.
- `main_app_name`: Your project will have the basis of a Django project which is basically the main app - the one containing the settings file and root urls etc. This variable determines what that folder should be called. This is basically your main app in the project. Some people prefer to just call it "project" or something like that some prefer to give it a meaningful name.
- `domain_name`: What's the domain name from which your project is going to be accessible when deployed? This is going to be used in a few places. If you still don't know your domain name I would recommend putting a string here that's easy to find so you can quickly find-and-replace it whenever you know your domain. You can for example set it as `^^MY^DOMAIN^^` ^^.
- `project_container_root_folder`: The name of the folder on your docker container into which the project files will be copied. Doesn't really matter that much.
- `repo_clone_address`: The Github repository address. This should be in whatever format your host machine can clone. So if you have set up SSH keys for it then use the ssh format (`git@github.com:...`) otherwise use HTTPS format. The important thing is, your host machine should be able to use this address and clone the repo.
- `server_deploy_folder`: This determines where on the host machine your project should be cloned and deployed from. This is relative to `~` so if you put `my-cool-project` then this path will be created on your host machine: `~/my-cool-project/repo/` and your repo will be cloned there.

- `dev_secret_key`: Secret key for the local instance of the project. This goes into Django project's settings via the env vars.
- `dev_allowed_hosts`: Allowed hosts for accessing the local instance of the project. You'll most likely not need to change this.
- `dev_db_name`: A name for the PG Database in your local instance.
- `dev_db_username`: A username for the above database.
- `dev_db_password`: A password for the above username.

- `prod_secret_key`: The project's secret key for the production instance. This is important to be kept safe. Once you put it here and you run the python file so the project files are generated you can delete it from here and only keep the version inside `.env.prod`.
- `prod_allowed_hosts`: Allowed hosts for the production instance. Most likely only your domain name but it's your project.
- `prod_db_name`: Same as above, the name of the PG database for the production instance.
- `prod_db_username`: Username for the database.
- `prod_db_password`: Password for the username above.
- `prod_env_gitignore_files`: The pattern for the env files to be put inside project's `.gitignore`. Probably won't need to change this.
- `cert_email`: The email address to be used for your domain SSL certificates. 
