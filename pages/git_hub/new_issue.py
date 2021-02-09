from data_classes.github import GitHubUser
from framework.action_framework import Page, Actions
# from framework.conditions import XpathExists
from framework.selector import Selector, Using


class GitHubNewIssue(Page):
    url = 'https://github.com/{username}/{reponame}/issues/new'
    issue_title_input = Selector(Using.NAME, 'issue[title]')
    issue_comment_input = Selector(Using.NAME, 'issue[body]')
    submit_button = Selector(Using.XPATH, '//button[@class="btn btn-primary" and contains(.,"Submit new issue")]')

    def __init__(self, actions: Actions, github_user: GitHubUser, reponame: str):
        super().__init__(actions)
        self.github_user = github_user
        self.reponame = reponame

    def open(self, url: str = None):
        if url is not None: super().open(url)
        else:
            uri = self.url.format(
                username=self.github_user.username,
                reponame=self.reponame
            )
            super().open(uri)

    def fill_form(self, title, comment=None):
        self.actions.type_text(self.issue_title_input, title)
        if comment is not None: self.actions.type_text(self.issue_comment_input, comment)

    def submit(self):
        self.actions.click(self.submit_button)
