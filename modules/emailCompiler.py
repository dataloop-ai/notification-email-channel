import base64
from abc import ABC, abstractmethod
from modules.notificationInfo import EmailTemplate, ApplicationInput
import dtlpy as dl


class EmailCompiler(ABC):
    @abstractmethod
    def __init__(self, application_input: ApplicationInput):
        super().__init__()
        self.application_input = application_input
        self.assets_folder = '../assets'
        self.resource_names = dict()
        self.env_prefix = dl.client_api.environments[dl.client_api.environment].get('url', None)
        if self.env_prefix is None:
            raise 'Failed to resolve env'

    def build_logo_attachment(self):
        image_id = 'logo'
        logo_file_content = open(self.assets_folder + '/logo.png', 'rb').read()
        logo_base64_utf8_str = base64.b64encode(logo_file_content).decode('utf-8')
        return {
            "filename": "logo",
            "contentType": "image/png",
            "content_id": image_id,
            "content": logo_base64_utf8_str,
            "disposition": "inline"
        }

    def append_logo_attachment(self, compiled):
        attachments = []
        logo_attachment = self.build_logo_attachment()
        attachments.append(logo_attachment)
        compiled = compiled.replace('@@logo@@', 'cid:'+logo_attachment['content_id'])
        return [compiled, attachments]

    def append_attachments(self, compiled):
        [compiled, attachments] = self.append_logo_attachment(compiled)
        return [compiled, attachments]

    @abstractmethod
    def compile_html(self, template: EmailTemplate):
        with open(self.assets_folder + '/{0}.html'.format(template), 'r') as file:
            compiled = file.read()
        compiled = compiled.replace('##title##', self.application_input.get_title())
        compiled = compiled.replace(
            '##description##', self.application_input.get_description())
        [compiled, attachments] = self.append_attachments(compiled)
        return [compiled, attachments]

    def get_resource_name(self, resource_id, callback: callable):
        try:
            resource = callback(resource_id)
            return resource.name
        except:
            return resource_id

    @staticmethod
    def get_service(service_id):
        return dl.services.get(service_id=service_id)

    @staticmethod
    def get_project(project_id):
        return dl.projects.get(project_id=project_id)

    @staticmethod
    def get_pipeline(pipeline_id):
        return dl.pipelines.get(pipeline_id=pipeline_id)

    @staticmethod
    def get_task(task_id):
        return dl.tasks.get(task_id=task_id)

    @staticmethod
    def get_assignment(assignment_id):
        return dl.assignments.get(assignment_id=assignment_id)

    @staticmethod
    def get_contributor(user_id, project_id) -> dl.entities.User:
        project = EmailCompiler.get_project(project_id)
        for contributor in project.contributors:
            if contributor.email == user_id:
                return contributor
        raise 'contributor {0} not found in project {1}'.format(user_id, project_id)

    @staticmethod
    def get_org(org_id):
        org = dl.organizations.get(organization_id=org_id)
        return org

    @staticmethod
    def get_org_member(org, user_id):
        for member in org.members:
            if member['id'] == user_id:
                return member
        raise 'member {0} not found in org {1}'.format(user_id, org['id'])