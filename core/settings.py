
import os
import json
import sys

APP_CONFIG_FILE = "app_config.json"

def load_app_config():
    if os.path.exists(APP_CONFIG_FILE):
        with open(APP_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_app_config(config):
    with open(APP_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_font_size():
    config = load_app_config()
    # 글자설정치: 여기서 기본 글꼴 크기를 조정할 수 있습니다.
    return config.get("font_size", 8)

def save_font_size(size):
    config = load_app_config()
    config["font_size"] = size
    save_app_config(config)


def get_last_profile():
    config = load_app_config()
    return config.get("last_profile", "profile1")

def save_last_profile(profile_name):
    config = load_app_config()
    config["last_profile"] = profile_name
    save_app_config(config)

def get_settings_filename(profile):
    return f"settings_{profile}.json"

def load_settings(profile):
    filename = get_settings_filename(profile)
    full_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            return {}
        except Exception as e:
            return {}
    else:
        return {}

def save_settings(profile, settings):
    filename = get_settings_filename(profile)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)



def load_config_key(profile, key, default=None):
    settings = load_settings(profile)
    return settings.get("main_config", {}).get(key, default)

def save_theme(profile, theme_name):
    save_config_key(profile, "theme", theme_name)

def migrate_to_settings_json(profile):
    settings = load_settings(profile)
    files_to_migrate = [
        ("search_history", "search_history.json"),
        ("saved_urls", "saved_urls.json"),
        ("search_groups", "search_groups.json"),
        ("main_config", "main_config.json"),
        ("recommend_tags", "recommend_tags.json"),
        ("left_search_history", "left_search_history.json"),
    ]
    
    changed = False
    for key, filename in files_to_migrate:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                settings[key] = json.load(f)
            os.remove(filename)
            changed = True

    if changed:
        save_settings(profile, settings)

def set_work_directory():
    script_path = os.path.abspath(sys.argv[0])
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)
