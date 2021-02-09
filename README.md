## Getting started   

Install pipenv `pip install pipenv`   

Download chromedriver from https://chromedriver.chromium.org/   
Add chromedriver to PATH.

Run tests with HTML report 
`pipenv run pytest -vvv --html=report.html --self-contained-html --log-file=tests.log -m "github"`   

In github_passwords.yaml insert your 
login_name:password

In github_tests.py in value tester change 'jtesterk' to your login_name 


#### Example configuration (default configuration dir is configurationz/config.yml)
```yaml
browser: chrome
browser_version: 83.0
wd_hub_url: null  # when null -> local webrdriver is being used :)
headless: false
action_framework:
  wait_between_actions_sec: 1
  timeout_find_element_sec: 5
  timeout_wait_for_condition_sec: 15
```

#### Tips   
Random string powershell `$env:output =-join ((65..90) + (97..122) | Get-Random -Count 25 | % {[char]$_})`
Random string linuxshell `output=$(tr -cd '[:alnum:]' < /dev/urandom | head -c25)`
