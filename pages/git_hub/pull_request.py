from framework.action_framework import Page, Actions

from framework.selector import Selector, Using
from data_classes.github import GitHubUserWithRepo


class GitHubNewPullRequest(Page):
    url = 'https://github.com/{username}/{reponame}/compare/main...{branchname}'
    create_pull_request_button = Selector(Using.XPATH,
                                          '//div[@class="repository-content "]//button[contains(.,"Create")]')
    confirm_create_pull_request_button = Selector(Using.XPATH,
                                                  '//button[@type="submit" and contains(.,"Create pull request")]')

    def __init__(self, actions: Actions, github_user_with_repo: GitHubUserWithRepo, branchname: str):
        super().__init__(actions)
        self.github_user_with_repo = github_user_with_repo
        self.branchname = branchname

    def open(self, url: str = None):
        if url is not None: super().open(url)
        else:
            uri = self.url.format(
                username=self.github_user_with_repo.user.username,
                reponame=self.github_user_with_repo.repo.name,
                branchname=self.branchname
            )
            super().open(uri)

    def create(self):
        self.actions.click(self.create_pull_request_button)
        self.actions.click(self.confirm_create_pull_request_button)
