from dataclasses import dataclass


@dataclass
class GitHubUser:
    username: str
    password: str


@dataclass
class GitHubRepo:
    name: str
    public: bool = True


class GitHubUserWithRepo:
    def __init__(self, user: GitHubUser, repo: GitHubRepo):
        self.user = user
        self.repo = repo
