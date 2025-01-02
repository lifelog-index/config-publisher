use redis::AsyncCommands;
use serde_json::json;
use configparser::ini::Ini;
use std::collections::HashMap;
use tokio;

#[tokio::main]
async fn main() -> redis::RedisResult<()> {
    let mut config = Ini::new();
    config.load("vbs_config.cfg").expect("Failed to load config");

    let mut config_map: HashMap<String, String> = HashMap::new();

    // Assuming `get_map()` returns something like `HashMap<String, HashMap<String, Option<String>>>`
    
    if let Some(config_sections) = config.get_map() {
        for (section, properties) in config_sections.iter() {
            for (key, value) in properties.iter() {
                if let Some(value) = value {
                    let full_key = format!("{}.{}", section, key);
                    config_map.insert(full_key, value.clone());
                }
            }
        }
    } else {
        eprintln!("Config map is empty or not available.");
    }

    let serialized_config = serde_json::to_string(&config_map).unwrap();

    let client = redis::Client::open("redis://127.0.0.1/")?;
    let mut con = client.get_multiplexed_async_connection().await?;

    // Publish the configuration
    con.publish("config_channel", serialized_config).await?;
    println!("Configuration published!");

    // Notify subscribers to restart services
    let restart_message = json!({
        "command": "restart",
        "reason": "Config updated"
    });
    con.publish("control_channel", restart_message.to_string()).await?;
    println!("Restart command sent!");

    Ok(())
}
