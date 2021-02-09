from framework.action_framework import Page
from framework.selector import Selector, Using


class GitHubNewRepo(Page):
    url = 'https://github.com/new'
    new_repo_button = Selector(Using.XPATH, "//a[@href='/new' and contains(@class, 'btn-sm')]")
    new_repo_name_input = Selector(Using.NAME, 'repository[name]')
    new_repo_descrip_input = Selector(Using.ID, 'repository_description')
    visibility_public_check = Selector(Using.ID, 'repository_visibility_public')
    visibility_private_check = Selector(Using.ID, 'repository_visibility_private')
    submit_button = Selector(Using.XPATH, "//div[@class='js-with-permission-fields']//button[@type='submit']")
    license_toggle = Selector(Using.ID, "repository_license_template_toggle")
    license_dropdown_activator = Selector(Using.XPATH, "//summary[@role='button']//span[contains(., 'License')]")
    license_option = Selector(Using.XPATH, "//div[@aria-label='License']//label[contains(., '{label}')]")

    def fill_form(self, reponame: str, public: bool = True, license_label: str = "MIT License"):
        self.actions.type_text(self.new_repo_name_input, reponame)
        # self.actions.wait_for(XpathExists("//dd[@class='success']"))
        if public: self.actions.click(self.visibility_public_check)
        else: self.actions.click(self.visibility_private_check)
        self.actions.click(self.license_toggle)
        self.actions.click(self.license_dropdown_activator)
        self.actions.click(self.license_option.parameterized(label=license_label))

    def submit(self):
        self.actions.click(self.submit_button)
