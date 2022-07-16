# What is this?
This scaffolder generates a containerized Django project with the given config ready to be deployed using gunicorn. It also uses Letsencrypt to provide SSL on the given domain name. Github Actions is used for the deployment pipeline and you'll need to put a few secrets in your pipeline to make it happen.

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
base64 -i .env.prod
```
Then copy the output and put it in the appropriate variable.

# Notes
- Server machine needs to have docker and docker-compose installed.
- If your repo is private then your server machine needs to have access to the repo (you can do this with repo settings on Github - look it up online).
- You cannot deploy multiple projects on the same host (unless you define all of them in the same docker-compose file).

