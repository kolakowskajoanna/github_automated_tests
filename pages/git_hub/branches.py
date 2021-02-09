from framework.action_framework import Page, Actions
from framework.conditions import XpathExists
from framework.selector import Selector, Using
from data_classes.github import GitHubUserWithRepo


class GitHubBranches(Page):
    url = 'https://github.com/{username}/{reponame}/branches'
    delete_branch_button = Selector(Using.XPATH,
                                    '//form[@action="/{username}/{reponame}/branches/{branchname}"]'
                                    '//button[@class="btn-link ml-3 text-red"]')

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

    def delete_branch(self, branchname: str):
        self.actions.click(self.delete_branch_button.parameterized(
            username=self.github_user_with_repo.user.username,
            reponame=self.github_user_with_repo.repo.name,
            branchname=branchname
        ))


