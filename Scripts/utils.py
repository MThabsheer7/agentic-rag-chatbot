import yaml

def read_config():
    try:
        with open('/data/thabsheer/rough/agentic-rag-chatbot/Scripts/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"The file does not exist.")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")