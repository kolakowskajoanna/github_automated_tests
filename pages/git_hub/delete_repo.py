from framework.action_framework import Page, Actions
from framework.conditions import XpathExists
from framework.selector import Selector, Using


class DeleteRepo(Page):
    url = 'https://github.com/{username}/{reponame}/settings'
    delete_button = Selector(Using.XPATH, '//summary[@role="button" and contains(., "Delete this repository")]')
    confirm_input = Selector(Using.XPATH, '//form[contains(@action, "settings/delete")]//input[@name="verify"]')
    confirm_button = Selector(Using.XPATH, "//button[contains(.,'delete this repository')]")

    def __init__(self, actions: Actions, github_user_with_repo):
        super().__init__(actions)
        self.github_user_with_repo = github_user_with_repo

    def open(self, url: str = None):
        if url is not None: super().open(url)
        else:
            uri = self.url.format(
                username=self.github_user_with_repo.user.username,
                reponame=self.github_user_with_repo.repo.name
            )
            super().open(uri)

    def delete(self):
        self.actions.click(self.delete_button)

    def confirm(self):
        repo_path = f'{self.github_user_with_repo.user.username}/{self.github_user_with_repo.repo.name}'
        self.actions.type_text(self.confirm_input, repo_path)
        self.actions.click(self.confirm_button)
