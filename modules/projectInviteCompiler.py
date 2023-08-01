from modules.emailCompiler import EmailCompiler
from modules.notificationInfo import ApplicationInput, EmailTemplate


class ProjectInviteCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)
        self.user_id = self.application_input.get_member()
        self.project_id = self.application_input.get_resource_id()
        self.contributor = self.get_contributor(user_id=self.user_id, project_id=self.project_id)
        self.role = self.contributor.role or 'Role Unknown'

    def replace_params(self, compiled):
        params = [
            {"name": "userEmail", "value": self.user_id},
            {"name": "role", "value": self.role},
            {"name": "projectName", "value": self.get_resource_name(self.project_id, self.get_project)},
            {"name": "domain", "value": self.env_prefix},
            {"name": "projectId", "value": self.project_id}
        ]
        for param in params:
            compiled = compiled.replace('##{0}##'.format(param['name']), param['value'])
        return compiled

    def replace_avatar(self, compiled):
        compiled = compiled.replace('@@userImage@@', self.contributor.avatar)
        return compiled

    def compile_html(self, template: EmailTemplate):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.replace_params(compiled)
        compiled = self.replace_avatar(compiled)
        return [compiled, attachments]
