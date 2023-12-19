from modules.emailCompiler import EmailCompiler
from modules.notificationInfo import ApplicationInput, EmailTemplate


class ProjectInviteCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)
        self.user_id = self.application_input.get_member()
        if self.user_id is None:
            raise ValueError('user_id is None')
        self.project_id = self.application_input.get_resource_id()
        if self.project_id is None:
            raise ValueError('project_id is None')
        self.contributor = self.get_contributor(user_id=self.user_id, project_id=self.project_id)

    @staticmethod
    def api_role_to_display_role(api_role):
        if api_role == 'engineer':
            return 'Developer'
        if api_role == 'annotationManager':
            return 'Annotation Manager'
        return api_role.title()

    def replace_params(self, compiled):
        role = ProjectInviteCompiler.api_role_to_display_role(
            self.application_input.notification_info.body.get('role', None) or 'Unknown role'
        )
        params = [
            {"name": "userEmail", "value": self.user_id},
            {"name": "role", "value": role},
            {"name": "domain", "value": self.env_prefix},
            {"name": "projectName", "value": self.application_input.notification_info.body.get('name', None) or 'Unknown name'},
            {"name": "projectId", "value": self.application_input.notification_info.body.get('id', None) or 'Unknown id'}
        ]
        for param in params:
            compiled = compiled.replace('##{0}##'.format(param['name']), param['value'])
        return compiled

    def replace_avatar(self, compiled):
        if self.contributor and self.contributor.avatar:
            compiled = compiled.replace('@@userImage@@', self.contributor.avatar)
        else:
            compiled = compiled.replace('@@userImage@@', self.default_avatar)
        return compiled

    def compile_html(self, template: EmailTemplate):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.replace_params(compiled)
        compiled = self.replace_avatar(compiled)
        return [compiled, attachments]
