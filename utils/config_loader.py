import os
import json
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger()


def load_servers():
    """
    Load servers from ENV first.
    If not found, fallback to JSON file.
    """
    load_dotenv()
    env_servers = os.getenv("SERVERS")
    
    # ======================
    # LOAD FROM Env
    # ======================    
    if env_servers:
        servers = [s.strip() for s in env_servers.split(",") if s.strip()]
        logger.info(f"Loaded {len(servers)} servers from ENV")
        
        return servers
    
    
    # ======================
    # LOAD FROM JSON
    # ======================
    json_path = "config/servers.json"
    
    if os.path.exists(json_path):
        with open(json_path,"r") as file:
            data = json.load(file)
        
        servers = data.get("servers",[])
        logger.info(f"Loaded {len(servers)} servers from JSON")
        
        return servers
    
    
    #=========================
    #Failr clearly
    #=========================
    logger.error("No servers found in ENV or config file")
    raise FileNotFoundError(
        "No servers found. Please set SERVERS in .env or config/servers.json"
    )
    
    
    