from framework.action_framework import Page, Actions
from framework.conditions import XpathExists
from framework.selector import Selector, Using
from data_classes.github import GitHubUserWithRepo


class GitHubRepoMain(Page):
    url = 'https://github.com/{username}/{reponame}'
    branches_list = Selector(Using.ID, 'branch-select-menu')
    branch_name_input = Selector(Using.ID, 'context-commitish-filter-field')
    create_branch_button = Selector(Using.XPATH, "//span[contains(.,'Create branch')]")
    download_button = Selector(Using.XPATH,'//li[contains(.,"Download ZIP")]')

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

    def add_branch(self, branchname: str):
        self.actions.click(self.branches_list)
        self.actions.type_text(self.branch_name_input, branchname)
        self.actions.wait_for(XpathExists("//span[contains(.,'Create branch')]"))
        self.actions.click(self.create_branch_button)
