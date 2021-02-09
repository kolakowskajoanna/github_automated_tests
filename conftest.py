import pytest, os, logging, uuid
import pytest_html
from selenium import webdriver
from py.xml import html

from framework.action_framework import Actions
from framework.configuration import Config
from framework.element_provider import BasicWebElementProvider

DRIVER_SCOPE = os.environ.get('DRIVER_SCOPE', 'function')
CONFIG_PATH = os.environ.get('SELENIUM_CONFIG_PATH', None)
if not CONFIG_PATH:
    logging.warning('SELENIUM_CONFIG_PATH not set! using default config.yml')
    CONFIG_PATH = 'configurationz/config.yml'

ROOT_DIR = os.path.dirname(__file__)
REPORT_DIR = os.environ.get('REPORT_DIR', ROOT_DIR + '/reports')
SCREENSHOTS_DIR = REPORT_DIR + '/screenshots'
CHROME_DRIVER_PATH = 'C:/webdriver/chromedriver.exe'


@pytest.fixture(scope=DRIVER_SCOPE)
def driver(conf):
    if conf.wd_hub_url:
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
        driver = webdriver.Remote(
            command_executor=conf.wd_hub_url,
            desired_capabilities=caps,
            options=options
        )
    else:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        driver.maximize_window()

    yield driver
    driver.quit()


@pytest.fixture(scope=DRIVER_SCOPE)
def actions(driver, conf):
    actions = Actions(BasicWebElementProvider(driver, conf))
    return actions


@pytest.fixture(scope='session')
def conf():
    cfg = Config.from_file(CONFIG_PATH)
    return cfg


def pytest_html_report_title(report):
    report.title = os.environ.get('TEST_JOB_NAME', 'Tests report')


def pytest_html_results_table_header(cells):
    cells.pop()
    cells.insert(4, html.th('Title'))
    title = cells.pop()
    duration = cells.pop()
    test = cells.pop()
    cells.insert(1, title)
    cells.insert(2, test)
    cells.insert(3, duration)


def pytest_html_results_table_row(report, cells):
    cells.pop()
    cells.insert(4, html.td(report.test_tile))
    title = cells.pop()
    duration = cells.pop()
    test = cells.pop()
    cells.insert(1, title)
    cells.insert(2, test)
    cells.insert(3, duration)


# noinspection PyUnresolvedReferences
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    docs = item.function.__doc__.split('\n') if item.function.__doc__ else []
    report.test_tile = docs[1] if len(docs) >= 1 else ''
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        htmldocs = []
        if len(docs) >= 2:
            docs = docs[1:]
            for doc in docs:
                if doc.strip() == '':
                    htmldocs.append('<br>')
                else:
                    htmldocs.append(f'<p style="margin: 5px; margin-left: 12px;">{doc}</p>')
            docstr = ''.join(htmldocs[2:len(htmldocs) - 1])
            extra.append(pytest_html.extras.html(f'<h4 style="margin: 8px;">Test description</h4>{docstr}'))
        if report.failed:
            actions: Actions = item.funcargs.get('actions', None)
            driver: Actions = item.funcargs.get('driver', None)
            wd = None
            if actions: wd = actions.element_provider.driver
            if driver: wd = driver
            if wd:
                name = f'{item.function.__name__}__{str(uuid.uuid4()).replace("-", "")[:15]}.png'
                spath = f'{SCREENSHOTS_DIR}/{name}'
                print('taking screenshot ->', spath)
                wd.save_screenshot(spath)
                dom = '<div class="image">'
                dom += f'<a href="screenshots/{name}" target="_blank">'
                dom += f'<img src="screenshots/{name}"></a></div>'
                extra.append(pytest_html.extras.html(dom))
        report.extra = extra
