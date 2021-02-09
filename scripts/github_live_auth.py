from selenium import webdriver

from framework.action_framework import Actions
from framework.configuration import Config
from framework.element_provider import BasicWebElementProvider
from pages.git_hub.login import GitHubLogin

CONFIG_PATH = '../configurationz/selenium_config.local.yml'
CFG = Config.from_file(CONFIG_PATH)


def driver(conf):
    caps = {
        "browser_name": conf.browser,
        "version": str(conf.browser_version),
        "enableVNC": True,
        "enableVideo": False,
        "acceptInsecureCerts": True
    }
    options = webdriver.ChromeOptions()
    options.headless = conf.headless
    options.add_argument('--start-maximized')
    return webdriver.Remote(
        command_executor=conf.wd_hub_url,
        desired_capabilities=caps,
        options=options
    )


if __name__ == '__main__':
    driver = driver(CFG)
    actions = Actions(BasicWebElementProvider(driver, CFG))
    gl = GitHubLogin(actions)
    gl.open()
    gl.goto_login_form()
    gl.live_login()
