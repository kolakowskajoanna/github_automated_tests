import yaml
from dataclasses import dataclass


@dataclass
class ActionFrameworkConfig:
    wait_between_actions_sec: int = 1
    timeout_find_element_sec: int = 5
    timeout_wait_for_condition_sec: int = 10


@dataclass
class Config:
    browser: str = 'chrome'
    browser_version: str = '83.0'
    wd_hub_url: str = None
    headless: bool = False
    action_framework: ActionFrameworkConfig = ActionFrameworkConfig()

    @staticmethod
    def from_file(file='selenium_config.yml'):
        try:
            with open(file, mode='r', encoding='utf-8') as f:
                loaded = yaml.load(f, Loader=yaml.FullLoader)
                loaded['action_framework'] = ActionFrameworkConfig(**loaded['action_framework'])
                return Config(**loaded)
        except Exception as e:
            print('Read config failed ...\n' + repr(e))
            return Config()
