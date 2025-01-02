import redis
import json
from configparser import ConfigParser
import os
import time

def save_config_to_file(config, file_path="output_config.cfg"):
    parser = ConfigParser()
    for key, value in config.items():
        section, option = key.split('.', 1)
        if section not in parser:
            parser.add_section(section)
        parser.set(section, option, value)
    with open(file_path, 'w') as configfile:
        parser.write(configfile)

def restart_service():
    print("Restarting services...")
    # Example: Restart by reloading the configuration or restarting a process
    time.sleep(1)
    print("Services restarted.")

def process_config_update(config_data):
    config = json.loads(config_data)
    print("Received configuration update!")
    save_config_to_file(config)
    print("Configuration saved to file.")

def process_control_message(message_data):
    control_message = json.loads(message_data)
    command = control_message.get("command")
    if command == "restart":
        print(f"Restart command received: {control_message.get('reason')}")
        restart_service()

def main():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("config_channel")
    pubsub.subscribe("control_channel")

    print("Subscribed to channels...")
    for message in pubsub.listen():
        if message["type"] == "message":
            if message["channel"] == "config_channel":
                process_config_update(message["data"])
            elif message["channel"] == "control_channel":
                process_control_message(message["data"])

if __name__ == "__main__":
    main()
