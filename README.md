
# Configuration Publishers - Subscribers

The Configuration Pub-Sub concept is a simple server that listens for configuration updates and publishes them to a Redis server. This allows other services using the same Redis server to receive the latest configuration updates seamlessly.



## Install Redis

To install Redis, follow these steps:

1. Download the latest version of Redis from [here](https://download.redis.io/redis-stable.tar.gz).

    ```bash
    wget https://download.redis.io/redis-stable.tar.gz
    ```

2. Compile and install Redis:

    ```bash
    mkdir $HOME/redis/
    cp redis-stable.tar.gz $HOME/redis/
    cd $HOME/redis/
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    ```

3. (Optional) Add Redis to the PATH:

    ```bash
    echo "alias redis-server='$HOME/redis/redis-stable/src/redis-server'" >> $HOME/.bashrc
    source $HOME/.bashrc
    ```

## Start the Redis Server

To start the Redis server, run the following command:

```bash
redis-server
```

## Usage

### Requirements

```bash
pip install redis
```

### Edit Configuration

Edit the `config.cfg` file according to your configuration requirements.

### Publish Configuration

To publish the configuration, use the following command:

```bash
python publisher.py
```

### Check Configuration Using a Python Subscriber

To check the configuration using a Python subscriber, follow these steps:

```bash
python subscriber.py
python publisher.py
```