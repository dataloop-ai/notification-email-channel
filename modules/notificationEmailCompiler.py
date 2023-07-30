import base64

from modules.emailCompiler import EmailCompiler
import dtlpy as dl
from modules.notificationInfo import NotificationResourceType, ApplicationInput


class NotificationEmailCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)

        self.replaced_links = dict()

    def build_icon_attachment(self):
        priority = self.application_input.get_priority()
        icon_image_id = 'notification_icon'
        if priority <= 50:
            icon_file = open(self.assets_folder + '/icon-dl-info-filled.png', 'rb').read()
        elif priority <= 75:
            icon_file = open(self.assets_folder + '/icon-dl-alert-filled.png', 'rb').read()
        else:
            icon_file = open(self.assets_folder + '/icon-dl-error-filled.png', 'rb').read()

        dataloop_logo_base64_utf8_str = base64.b64encode(icon_file).decode('utf-8')
        return {
            "filename": "notification-icon-dataloop",
            "contentType": "image/png",
            "content_id": icon_image_id,
            "content": dataloop_logo_base64_utf8_str,
            "disposition": "inline"
        }

    def append_attachments(self, compiled):
        [compiled, attachments] = super().append_attachments(compiled)
        icon_attachment = self.build_icon_attachment()
        attachments.append(icon_attachment)
        compiled = compiled.replace('@@notificationIcon@@', 'cid:' + icon_attachment['content_id'])
        return [compiled, attachments]

    def insert_log_link(self, link_prefix: str,
                        compiled_html: str, service: str=None):
        if service is not None:
            log_link = link_prefix + "/faas/logs?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceLogsLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Logs:</span><a href={0}>Logs</a></div>'.format(
                                                      log_link))
            self.replaced_links['$$ServiceLogsLink$$'] = True
        return compiled_html

    def insert_service_link(self, link_prefix: str,
                            compiled_html: str, service: str = None):
        if service is not None:
            service_link = link_prefix + "/services/{0}".format(service)
            resource_name = self.get_resource_name(service, self.get_service)
            compiled_html = compiled_html.replace('$$ServiceLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Service:</span><a href={0}>{1}</a></div>'.format(
                                                      service_link, resource_name))
            self.replaced_links['$$ServiceLink$$'] = True
        return compiled_html

    def insert_executions_link(self, link_prefix: str,
                               compiled_html: str,
                               service: str=None):
        if service is not None:
            executions_link = link_prefix + "/executions?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceExecutionsLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Executions:</span><a href={0}>Executions</a></div>'.format(
                                                      executions_link))
            self.replaced_links['$$ServiceExecutionsLink$$'] = True
        return compiled_html

    def insert_pipeline_link(self, link_prefix: str,
                             compiled_html: str,
                             pipeline: str=None):
        if pipeline is not None:
            pipeline_link = link_prefix + "/pipelines/{}".format(pipeline)
            resource_name = self.get_resource_name(pipeline, self.get_pipeline)
            compiled_html = compiled_html.replace('$$PipelineLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Pipeline:</span><a href={0}>{1}</a></div>'.format(
                                                      pipeline_link, resource_name))
            self.replaced_links['$$PipelineLink$$'] = True
        return compiled_html

    def insert_task_link(self, link_prefix: str,
                         compiled_html: str):
        task = self.application_input.get_resource_id()
        if task is not None:
            task_link = link_prefix + "/tasks/{0}/assignments".format(task)
            resource_name = self.get_resource_name(task, self.get_task)
            compiled_html = compiled_html.replace('$$TaskLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Task:</span><a href={0}>{1}</a></div>'.format(
                                                      task_link, resource_name))
            self.replaced_links['$$TaskLink$$'] = True
        return compiled_html

    def insert_assignment_link(self, link_prefix: str,
                               compiled_html: str):
        assignment = self.application_input.get_resource_id()
        assignments_link = link_prefix + "/assignments/{0}/items".format(assignment)
        assignment_name = self.get_resource_name(assignment, self.get_assignment)
        compiled_html = compiled_html.replace('$$AssignmentLink$$',
                                              '<div><span style="color: #171723; padding-right: 2px;">Assignment:</span><a href={0}>{1}</a></div>'.format(
                                                  assignments_link, assignment_name))
        self.replaced_links['$$AssignmentLink$$'] = True
        return compiled_html

    def insert_project_link(self, project: str, compiled_html: str):
        project_link_prefix = self.env_prefix + "projects/"
        project_name = self.get_resource_name(project, self.get_project)
        compiled_html = compiled_html.replace('$$ProjectLink$$',
                                              '<div><span style="color: #171723; padding-right: 2px;">Project:</span><a href={0}>{1}</a></div>'.format(
                                                  project_link_prefix + project, project_name))
        self.replaced_links['$$ProjectLink$$'] = True
        link_prefix = project_link_prefix + project
        return link_prefix, compiled_html

    def insert_links(self, html_template_string):
        compiled = html_template_string
        project = self.application_input.get_project()
        resource_type = self.application_input.get_resource_type()
        if project is not None:
            link_prefix, compiled = self.insert_project_link(project=project,
                                                             compiled_html=compiled)
            if resource_type == NotificationResourceType.SERVICES:
                service = self.application_input.get_resource_id()
                compiled = self.insert_service_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
                compiled = self.insert_log_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
            elif resource_type == NotificationResourceType.EXECUTIONS:
                service = self.application_input.get_service()
                compiled = self.insert_service_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
                compiled = self.insert_executions_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
            elif resource_type == NotificationResourceType.CYCLES:
                pipeline = self.application_input.get_pipeline()
                compiled = self.insert_pipeline_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    pipeline=pipeline
                )
            elif resource_type == NotificationResourceType.TASKS:
                compiled = self.insert_task_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled
                )
            elif resource_type == NotificationResourceType.ASSIGNMENTS:
                compiled = self.insert_assignment_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled
                )
        for link in ["$$ProjectLink$$",
                     "$$ServiceLink$$",
                     "$$ServiceLogsLink$$",
                     "$$ServiceExecutionsLink$$",
                     "$$PipelineLink$$",
                     "$$TaskLink$$",
                     "$$AssignmentLink$$"
                     ]:
            if link not in self.replaced_links:
                compiled = compiled.replace(link, '')
        return compiled

    def compile_html(self, template):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.insert_links(compiled)
        return [compiled, attachments]
