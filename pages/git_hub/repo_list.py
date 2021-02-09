from typing import List

from framework.action_framework import Page, Actions
from framework.selector import Selector, Using


class GitHubRepoList(Page):
    url = 'https://github.com/{username}?tab=repositories'
    repo_name_label = Selector(
        Using.XPATH,
        '//h3[@class="wb-break-all" and contains(itemprop, name)]/a'
    )

    def __init__(self, actions: Actions, github_user):
        super().__init__(actions)
        self.github_user = github_user

    def open(self, url: str = None):
        if url is not None: super().open(url)
        else:
            uri = self.url.format(username=self.github_user.username)
            super().open(uri)

    def get_names(self, avoided_repos: List[str]) -> List[str]:
        repos_names = self.actions.get_elements_text(self.repo_name_label)
        result = []
        for repo_name in repos_names:
            if repo_name not in avoided_repos:
                result.append(repo_name)
        return result

    def get_names_with_prefix(self):
        repos_names = self.actions.get_elements_text(self.repo_name_label)
        result = []
        for repo_name in repos_names:
            if repo_name.startswith('TEST__'): result.append(repo_name)
        print(result)
        return result

