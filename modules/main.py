import base64
import dtlpy as dl
import os
from enum import Enum

assets_folder = './assets'


class NotificationResourceType(str, Enum):
    EXECUTIONS = "executions",
    PIPELINES = "pipelines",
    CYCLES = "pipeline.run",
    SERVICES = "services",
    TASKS = "tasks",
    ASSIGNMENTS = "assignments"


class EventMessage:
    def __init__(self, event_message: dict):
        if event_message is None:
            raise ValueError('event_message is None')
        if event_message.get('title', None) is None:
            raise ValueError('title is None')
        if event_message.get('description', None) is None:
            raise ValueError('description is None')
        self.title = event_message.get('title')
        self.description = event_message.get('description')
        self.resource_action = event_message.get('resourceAction', None)
        self.resource_id = event_message.get('resourceId', None)
        self.resource_type = event_message.get('resourceType', None)
        self.resource_name = event_message.get('resourceName', None)


class NotificationInfo:
    def __init__(self, notification_info: dict):
        if notification_info is None:
            raise ValueError('notification_info is None')
        if notification_info.get('notificationCode', None) is None:
            raise ValueError('notificationCode is None')
        if notification_info.get('context', None) is None:
            raise ValueError('context is None')
        if notification_info.get('priority', None) is None:
            raise ValueError('priority is None')
        if notification_info.get('eventMessage', None) is None:
            raise ValueError('eventMessage is None')
        self.notification_code = notification_info.get('notificationCode')
        self.type = notification_info.get('type', None)
        self.context = notification_info.get('context')
        self.priority = notification_info.get('priority')
        self.event_message = EventMessage(notification_info.get('eventMessage'))


class ApplicationInput:
    def __init__(self, application_input: dict):
        if application_input is None:
            raise ValueError('application_input is None')
        if application_input.get('notificationInfo', None) is None:
            raise ValueError('notificationInfo is None')
        if application_input.get('recipients', None) is None:
            raise ValueError('recipients is None')
        if application_input.get('notificationId', None) is None:
            raise ValueError('notificationId is None')
        self.notification_info = NotificationInfo(application_input.get('notificationInfo'))
        self.recipients = application_input.get('recipients')
        self.notification_id = application_input.get('notificationId')

    def get_service(self):
        return self.notification_info.context.get('service', None)

    def get_pipeline(self):
        return self.notification_info.context.get('pipeline', None)

    def get_resource_id(self):
        return self.notification_info.event_message.resource_id


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resource_names = dict()
        self.env_prefix = self.get_platform_url()

    @staticmethod
    def get_platform_url():
        env_prefix = dl.client_api.environments[dl.client_api.environment].get('url', None)
        if env_prefix is None:
            env_prefix = dl.client_api.environment.replace('-gate', '').replace('/api/v1', '')

    def get_resource_name(self, resource_id, callback: callable):
        if resource_id in self.resource_names:
            return self.resource_names[resource_id]
        else:
            try:
                resource = callback(resource_id)
                self.resource_names[resource_id] = resource.name
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

    def build_logo_attachment(self):
        dataloop_image_id = 'dataloop_logo'
        dataloop_logo_file_content = open(assets_folder + '/logo-dataloop.png', 'rb').read()
        dataloop_logo_base64_utf8_str = base64.b64encode(dataloop_logo_file_content).decode('utf-8')
        return {
            "filename": "logo-dataloop",
            "contentType": "image/png",
            "content_id": dataloop_image_id,
            "content": dataloop_logo_base64_utf8_str,
            "disposition": "inline"
        }

    def insert_log_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, service: str = None):
        if service is not None:
            log_link = link_prefix + "/faas/logs?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceLogsLink$$',
                                        '<div><span style="color: #171723; padding-right: 2px;">Logs:</span><a href={0}>Service logs</a></div>'.format(
                                            log_link))
            replaced_links['$$ServiceLogsLink$$'] = True
        return compiled_html

    def insert_service_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, service: str = None):
        if service is not None:
            service_link = link_prefix + "/services/{0}".format(service)
            resource_name = self.get_resource_name(service, self.get_service)
            compiled_html = compiled_html.replace('$$ServiceLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Service:</span><a href={0}>{1}</a></div>'.format(
                                                      service_link, resource_name))
            replaced_links['$$ServiceLink$$'] = True
        return compiled_html

    def insert_executions_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, service: str = None):
        if service is not None:
            executions_link = link_prefix + "/executions?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceExecutionsLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Executions:</span><a href={0}>Service executions</a></div>'.format(
                                                      executions_link))
            replaced_links['$$ServiceExecutionsLink$$'] = True
        return compiled_html

    def insert_pipeline_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, pipeline: str = None):
        if pipeline is not None:
            pipeline_link = link_prefix + "/pipelines/{}".format(pipeline)
            resource_name = self.get_resource_name(pipeline, self.get_pipeline)
            compiled_html = compiled_html.replace('$$PipelineLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Pipeline:</span><a href={0}>{1}</a></div>'.format(
                                                      pipeline_link, resource_name))
            replaced_links['$$PipelineLink$$'] = True
        return compiled_html

    def insert_task_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, task: str = None):
        if task is not None:
            task_link = link_prefix + "/tasks/{0}/assignments".format(task)
            resource_name = self.get_resource_name(task, self.get_task)
            compiled_html = compiled_html.replace('$$TaskLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Task:</span><a href={0}>{1}</a></div>'.format(
                                                      task_link, resource_name))
            replaced_links['$$TaskLink$$'] = True
        return compiled_html

    def insert_assignment_link(self, replaced_links: dict, link_prefix: str, compiled_html: str, assignment: str = None):
        assignments_link = link_prefix + "/assignments/{0}/items".format(assignment)
        assignment_name = self.get_resource_name(assignment, self.get_assignment)
        compiled_html = compiled_html.replace('$$AssignmentLink$$',
                                              '<div><span style="color: #171723; padding-right: 2px;">Assignment:</span><a href={0}>{1}</a></div>'.format(
                                                  assignments_link, assignment_name))
        replaced_links['$$AssignmentLink$$'] = True
        return compiled_html

    def insert_project_link(self, project: str, replaced_links: dict, compiled_html: str):
        project_link_prefix = self.env_prefix + "projects/"
        project_name = self.get_resource_name(project, self.get_project)
        compiled_html = compiled_html.replace('$$ProjectLink$$',
                                    '<div><span style="color: #171723; padding-right: 2px;">Project:</span><a href={0}>{1}</a></div>'.format(
                                        project_link_prefix + project, project_name))
        replaced_links['$$ProjectLink$$'] = True
        link_prefix = project_link_prefix + project
        return link_prefix, compiled_html

    def insert_links(self, html_template_string, application_input: ApplicationInput):
        compiled = html_template_string
        project = application_input.notification_info.context.get('project', None)
        replaced_links = dict()
        resource_type = application_input.notification_info.event_message.resource_type
        if project is not None:
            link_prefix, compiled = self.insert_project_link(project=project, replaced_links=replaced_links, compiled_html=compiled)
            if resource_type == NotificationResourceType.SERVICES:
                service = application_input.get_resource_id()
                compiled = self.insert_service_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
                compiled = self.insert_log_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
            elif resource_type == NotificationResourceType.EXECUTIONS:
                service = application_input.get_service()
                compiled = self.insert_service_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
                compiled = self.insert_executions_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
            elif resource_type == NotificationResourceType.CYCLES:
                pipeline = application_input.get_pipeline()
                compiled = self.insert_pipeline_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    pipeline=pipeline
                )
            elif resource_type == NotificationResourceType.TASKS:
                task = application_input.get_resource_id()
                compiled = self.insert_task_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    task=task
                )
            elif resource_type == NotificationResourceType.ASSIGNMENTS:
                assignment = application_input.get_resource_id()
                compiled = self.insert_assignment_link(
                    replaced_links=replaced_links,
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    assignment=assignment
                )
        for link in ["$$ProjectLink$$",
                     "$$ServiceLink$$",
                     "$$ServiceLogsLink$$",
                     "$$ServiceExecutionsLink$$",
                     "$$PipelineLink$$",
                     "$$TaskLink$$",
                     "$$AssignmentLink$$"
                     ]:
            if link not in replaced_links:
                compiled = compiled.replace(link, '')
        return compiled

    def build_icon_attachment(self, application_input: ApplicationInput):
        priority = application_input.notification_info.priority
        icon_image_id = 'notification_icon'
        if priority <= 50:
            icon_file = open(assets_folder + '/icon-dl-info-filled.png', 'rb').read()
        elif priority <= 75:
            icon_file = open(assets_folder + '/icon-dl-alert-filled.png', 'rb').read()
        else:
            icon_file = open(assets_folder + '/icon-dl-error-filled.png', 'rb').read()

        dataloop_logo_base64_utf8_str = base64.b64encode(icon_file).decode('utf-8')
        return {
            "filename": "notification-icon-dataloop",
            "contentType": "image/png",
            "content_id": icon_image_id,
            "content": dataloop_logo_base64_utf8_str,
            "disposition": "inline"
        }

    def compile_html(self, html_template_string, application_input: ApplicationInput):
        attachments = []
        compiled = html_template_string
        compiled = compiled.replace('##title##', application_input.notification_info.event_message.title)
        compiled = compiled.replace('##description##', application_input.notification_info.event_message.description)
        logo_attachment = self.build_logo_attachment()
        attachments.append(logo_attachment)
        icon_attachment = self.build_icon_attachment(application_input=application_input)
        attachments.append(icon_attachment)
        compiled = compiled.replace('@@dataloopLogo@@', 'cid:'+logo_attachment['content_id'])
        compiled = compiled.replace('@@notificationIcon@@', 'cid:' + icon_attachment['content_id'])
        compiled = self.insert_links(html_template_string=compiled, application_input=application_input)
        return compiled, attachments

    def email(self, input: dict):
        print(os.getcwd())
        application_input = ApplicationInput(input)
        with open(assets_folder + '/email_template.html', 'r') as file:
            template_string = file.read()

        [compiled_html, attachments] = self.compile_html(html_template_string=template_string, application_input=application_input)
        title = '[Dataloop] ' + str(application_input.notification_info.event_message.title).title()
        req_data = {
            "to": application_input.recipients,
            "from": "notifications@dataloop.ai",
            "subject": title,
            "body": compiled_html,
            "attachments": attachments,
            "personalize": True,
            "senderName": "Dataloop Notification"
        }
        if application_input.recipients is None or len(application_input.recipients) == 0:
            return
        dl.client_api.gen_request(req_type='post', json_req=req_data, path='/outbox')
