from framework.action_framework import Page, Actions
from framework.selector import Selector, Using
from data_classes.github import GitHubUserWithRepo


class GitHubNewCommit(Page):
    url = 'https://github.com/{username}/{reponame}/new/{branchname}'
    file_name_input = Selector(Using.NAME, 'filename')
    file_text_input = Selector(Using.NAME, 'value')
    commit_name_input = Selector(Using.NAME, 'message')
    commit_description_input = Selector(Using.NAME, 'description')
    submit_commit_button = Selector(Using.ID, 'submit-file')

    def __init__(self, actions: Actions, github_user_with_repo: GitHubUserWithRepo, branchname: str):
        super().__init__(actions)
        self.github_user_with_repo = github_user_with_repo
        self.branchname = branchname

    def open(self, url: str = None):
        if url is not None:
            super().open(url)
        else:
            uri = self.url.format(
                username=self.github_user_with_repo.user.username,
                reponame=self.github_user_with_repo.repo.name,
                branchname=self.branchname
            )
            super().open(uri)

    def fill_form(self, filename):
        self.actions.type_text(self.file_name_input, filename)
        # self.actions.type_text(self.file_text_input, file_text)
        # self.actions.type_text(self.commit_name_input, f'add {filename}')
        # self.actions.type_text(self.commit_description_input, f'{filename} ist zuper')

    def submit(self):
        self.actions.click(self.submit_commit_button)
