import redis
import json
from configparser import ConfigParser

def load_config(file_path):
    """
    Load configuration from a .cfg file and convert it into a dictionary.
    """
    parser = ConfigParser()
    parser.read(file_path)
    config = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            config[f"{section}.{key}"] = value
    return config

def publish_config(redis_client, channel, config):
    """
    Publish the configuration to a Redis channel.
    """
    serialized_config = json.dumps(config)
    redis_client.publish(channel, serialized_config)
    print(f"Configuration published to channel: {channel}")

def notify_restart(redis_client, control_channel, reason="Config updated"):
    """
    Notify subscribers to restart services by sending a control message.
    """
    control_message = {
        "command": "restart",
        "reason": reason
    }
    redis_client.publish(control_channel, json.dumps(control_message))
    print(f"Restart notification sent on channel: {control_channel}")

def main():
    # Redis connection
    redis_host = "127.0.0.1"
    redis_port = 6379
    config_channel = "config_channel"
    control_channel = "control_channel"

    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    # Load configuration
    config_path = "vbs_config.cfg"
    config = load_config(config_path)

    # Publish configuration and notify subscribers
    publish_config(redis_client, config_channel, config)
    notify_restart(redis_client, control_channel)

if __name__ == "__main__":
    main()
