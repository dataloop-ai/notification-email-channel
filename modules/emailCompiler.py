import base64
from abc import ABC, abstractmethod

from assets.assetsLoader import AssetsLoader
from modules.notificationInfo import EmailTemplate, ApplicationInput, NotificationResourceType
import dtlpy as dl


class EmailCompiler(ABC):
    @abstractmethod
    def __init__(self, application_input: ApplicationInput):
        super().__init__()
        self.application_input = application_input
        self.env_prefix = dl.client_api.environments[dl.client_api.environment].get('url', None)
        if self.env_prefix is None:
            raise Exception('Failed to resolve env')
        self.default_avatar = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"

    @staticmethod
    def build_logo_attachment():
        image_id = 'logo'
        logo_file_content = AssetsLoader.get_logo()
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
        compiled = AssetsLoader.get_template(template)
        compiled = compiled.replace('##title##', self.application_input.get_title())
        compiled = compiled.replace(
            '##description##', self.application_input.get_description())
        [compiled, attachments] = self.append_attachments(compiled)
        return [compiled, attachments]

    def get_resource_name(self, resource_id, callback: callable, resource_type: NotificationResourceType = None):
        if resource_type is not None and resource_type == self.application_input.notification_info.event_message.resource_type:
            return self.application_input.notification_info.event_message.resource_name
        try:
            resource = callback(resource_id)
            return resource.name
        except:
            return resource_id

    @staticmethod
    def get_service(service_id):
        return dl.services.get(service_id=service_id)

    @staticmethod
    def get_model(model_id):
        return dl.models.get(model_id=model_id)

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
        contributors = project.contributors
        members = project.list_members()
        for contributor in contributors:
            if contributor.email == user_id:
                return contributor
        for member in members:
            if member.email == user_id:
                return member
        return None

    @staticmethod
    def get_org(org_id):
        try:
            org = dl.organizations.get(organization_id=org_id)
            return org
        except:
            return None

    @staticmethod
    def get_org_member(org, user_id):
        if org is None:
            return None
        try:
            for member in org.members:
                if member['id'] == user_id:
                    return member
            for member in org.list_members():
                if member.id == user_id:
                    return member
            return None
        except:
            return None