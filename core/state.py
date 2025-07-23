
from . import settings
from . import actions

class AppState:
    def __init__(self):
        self.current_profile = settings.get_last_profile()
        self.load_all_data()

    def load_all_data(self):
        self.settings = settings.load_settings(self.current_profile)
        self.search_history = self.settings.get("search_history", [])
        self.saved_urls = self.settings.get("saved_urls", {})
        self.recommend_tags = self.settings.get("recommend_tags", [])
        self.left_search_history = self.settings.get("left_search_history", [])
        self.search_groups = self.settings.get("search_groups", ["기본"])
        self.url_groups = self.settings.get("url_groups", ["기본"])
        self.main_config = self.settings.get("main_config", {})
        actions.ensure_tags_in_history(self)

    def save_all_data(self):
        self.settings["search_history"] = self.search_history
        self.settings["saved_urls"] = self.saved_urls
        self.settings["recommend_tags"] = self.recommend_tags
        self.settings["left_search_history"] = self.left_search_history
        self.settings["search_groups"] = self.search_groups
        self.settings["url_groups"] = self.url_groups
        self.settings["main_config"] = self.main_config
        settings.save_settings(self.current_profile, self.settings)

    def set_config_key(self, key, value):
        if "main_config" not in self.settings:
            self.settings["main_config"] = {}
        self.settings["main_config"][key] = value

    def get_config_key(self, key, default=None):
        return self.settings.get("main_config", {}).get(key, default)

    def switch_profile(self, profile_name):
        self.save_all_data() # 현재 프로필 저장
        self.current_profile = profile_name
        settings.save_last_profile(profile_name)
        self.load_all_data()

    def save_search_history(self):
        self.settings["search_history"] = self.search_history
        settings.save_settings(self.current_profile, self.settings)

    def save_saved_urls(self):
        self.settings["saved_urls"] = self.saved_urls
        settings.save_settings(self.current_profile, self.settings)

    def save_recommend_tags(self):
        self.settings["recommend_tags"] = self.recommend_tags
        settings.save_settings(self.current_profile, self.settings)

    def save_left_history(self):
        self.settings["left_search_history"] = self.left_search_history
        settings.save_settings(self.current_profile, self.settings)

    def save_search_groups(self):
        self.settings["search_groups"] = self.search_groups
        settings.save_settings(self.current_profile, self.settings)

    def save_url_groups(self):
        self.settings["url_groups"] = self.url_groups
        settings.save_settings(self.current_profile, self.settings)

    def get_url_check_presets(self):
        presets = self.settings.get("url_check_presets", {})
        # Ensure that each preset entry is a dictionary
        for key, value in list(presets.items()): # Use list() to iterate over a copy since we might modify it
            if not isinstance(value, dict):
                # Assume old format was just a list of URLs, convert to new dict format
                presets[key] = {"name": key, "urls": value}
        return presets

    def save_url_check_presets(self, presets):
        self.settings["url_check_presets"] = presets
        self.save_all_data()


