from modules.emailCompiler import EmailCompiler
from modules.types import ApplicationInput, EmailTemplate


class ProjectInviteEmailCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)

    def compile_html(self, template: EmailTemplate):
        pass