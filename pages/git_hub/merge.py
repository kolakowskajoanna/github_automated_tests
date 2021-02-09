from framework.action_framework import Page, Actions
from framework.conditions import XpathExists

from framework.selector import Selector, Using
from data_classes.github import GitHubUserWithRepo


class GitHubMerge(Page):
    url = 'https://github.com/{username}/{reponame}/branches/all'
    merge_pull_request = Selector(Using.XPATH,
                                  '//div[contains(@class,"select-menu")]//button[contains(.,"Merge pull request")]')
    confirm_merge = Selector(Using.XPATH,
                             '//button[contains(., "Confirm merge")]')
    xpath_pull_request = '//a[contains(.,"Open")]'
    pull_request = Selector(Using.XPATH, '//a[contains(.,"Open")]')

    def __init__(self, actions: Actions, github_user_with_repo: GitHubUserWithRepo):
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

    def pick_pull_requests(self):
        self.actions.click(self.pull_request)

    def create(self):
        self.actions.click(self.merge_pull_request)
        self.actions.click(self.confirm_merge)
