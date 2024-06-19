# Launching App on Google Cloud


## Setting Up Your Environment on Ubuntu

1. Update and Upgrade the System

```sh
sudo apt update && sudo apt upgrade -y
```

2. Install Python, Virtual Environments and Pip

```sh
sudo apt install python3 python3-venv python3-pip -y
sudo apt install
```

3. Install Git

```sh
sudo apt install git -y
```

4. Clone Your Dash App Repository

   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

5. Set Up Virtual Environment

   ```sh
   python -m venv .venv.v
   source .venv/bin/activate
   pip3 install -r requirements.txt
   ```

Running Your Dash App with Gunicorn

1. Install Gunicorn

   ```sh
   pip3 install gunicorn
   ```

2. Run Gunicorn to Serve Your App
Create a Gunicorn configuration file (optional):

   ```sh
   nano gunicorn_config.py
   ```

   Example content:

   ```*.txt
   bind = "0.0.0.0:8050"
   workers = 3
   ```

    Run Gunicorn

    ```sh
    gunicorn main:app --config gunicorn_config.py
    ```

