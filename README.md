# agentic RAG demo

Building up on [this excellent video from AI Makerspace](https://www.youtube.com/watch?v=SEA3eJrDc-k), this project implements a RAG system that queries data about... RAG systems.

It uses a Streamlit UI to interact with the RAG system. The app is accessible on https://rag.yactouat.com.

The LLMs under the hood are a mixture of ChatGPT 4 and 3.5.

## pre requisites

To be able to use the application, you need:

- a working Python environment (I use 3.12)
- an OpenAI API key

For the OpenAI API key, if it's not loaded from a `.env` file, the user will be prompted to enter it.

## run locally

To run the application locally: `streamlit run agentic_rag.py` OR `python3 -m streamlit run agentic_rag.py`.

## run on an Ubuntu server

Deployment is done using GitHub Actions on push to the `master` branch, you need to fill in a few repository secrets, as stated in the `.github/workflows/cicd.yml` file.

### installation steps before letting the CI/CD pipeline run its course

These are actions you need to do on the remote server before you can run pipelines (I've run them on an Ubuntu 24 server)

- `mkdir ~/agentic-rag-demo`
- clone this very repo on your machine in order to be able to copy it to the server
- from your local machine => 

`scp -r <repo> <user>@<remote-server-ip>:/home/<remote-user>/agentic-rag-demo` (replace `<repo>`, `<user>`, `<remote-server-ip>`, and `<remote-user>` with the appropriate values

- back to your remote server from there on: `sudo apt update && sudo apt upgrade -y`
- `sudo apt install nginx`
- `sudo mkdir -p /var/www/<domain>` (replace `<domain>` with your domain or subdomain)
- `sudo chown -R www-data:www-data /var/www/<domain>`
- `sudo chmod -R 755 /var/www/<domain>`
- `sudo nano /etc/nginx/sites-available/<domain>.conf`
- add the following content:

```
server {
    listen 80;
    listen [::]:80;

    root /var/www/<domain>;
    index index.html;

    server_name <domain>;

    location / {
        proxy_pass http://0.0.0.0:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

}
```

- `sudo ln -s /etc/nginx/sites-available/<domain>.conf /etc/nginx/sites-enabled/`
- `sudo nginx -t`
- `sudo systemctl reload nginx`
- configure an A record in your DNS settings to point to your server's IP address for your domain or subdomain
- `cd ~/agentic-rag-demo`
- `pip install -r requirements.txt`
- `streamlit run agentic_rag.py`
- at this point, you should be able to see the dummy content when you navigate to your domain or subdomain on plain HTTP (after DNS propagation)
- now follow the instructions on certbot website to put the app behind HTTPS, you should now have a working RAG system accessible on your domain or subdomain 😎
- now we want to create a service for the app to run in the background, this helps us:
  - manage crashes
  - start the app on boot
  - release the terminal when we start the app from our CI/CD pipeline
  - provide us with an easy way of stopping the app in the same CI/CD pipeline before updating it
- `mkdir -p ~/.config/systemd/user`
- `nano ~/.config/systemd/user/agentic-rag.service`
- write the following content:

```
[Unit]
Description=a service for the agentic rag demo
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m streamlit run /home/<remote-user>/agentic-rag-demo/agentic_rag.py
Restart=on-failure
RestartSec=2

[Install]
WantedBy=default.target
```

... don't forget to replace the placeholders with the appropriate values.

- now we need our service to be stoppable/start-able from our CI/CD pipeline with our regular user, so let's do =>

```bash
systemctl --user daemon-reload
systemctl --user enable --now agentic-rag.service
systemctl --user start agentic-rag.service
systemctl --user status agentic-rag.service
```

- to stop the service => `systemctl --user stop agentic-rag.service`
- we are now ready to let the CI/CD pipeline do its magic 🚀