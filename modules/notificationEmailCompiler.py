import base64

from assets.assetsLoader import AssetsLoader
from modules.emailCompiler import EmailCompiler
import dtlpy as dl
from modules.notificationInfo import NotificationResourceType, ApplicationInput
from datetime import datetime, timedelta


class NotificationEmailCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)

        self.replaced_links = dict()

    def build_icon_attachment(self):
        priority = self.application_input.get_priority()
        icon_image_id = 'notification_icon'
        if priority <= 50:
            icon_file = AssetsLoader.get_info_icon()
        elif priority <= 75:
            icon_file = AssetsLoader.get_warning_icon()
        else:
            icon_file = AssetsLoader.get_error_icon()

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
                        compiled_html: str, service: str = None):
        if service is not None:
            log_link = link_prefix + "/faas/logs?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceLogsLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Logs:</span><a href={0}>Service Logs</a></div>'.format(
                                                      log_link))
            self.replaced_links['$$ServiceLogsLink$$'] = True
        return compiled_html

    def insert_service_link(self, link_prefix: str,
                            compiled_html: str, service: str = None):
        if service is not None:
            service_link = link_prefix + "/services/{0}".format(service)
            resource_name = self.get_resource_name(service, self.get_service, NotificationResourceType.SERVICES)
            compiled_html = compiled_html.replace('$$ServiceLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Service:</span><a href={0}>{1}</a></div>'.format(
                                                      service_link, resource_name))
            self.replaced_links['$$ServiceLink$$'] = True
        return compiled_html

    def insert_model_link(self, link_prefix: str,
                          compiled_html: str, model: str = None):
        if model is not None:
            model_link = link_prefix + "/model/{0}".format(model)
            resource_name = self.get_resource_name(model, self.get_model, NotificationResourceType.MODELS)
            compiled_html = compiled_html.replace('$$ModelLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Model:</span><a href={0}>{1}</a></div>'.format(
                                                      model_link, resource_name))
            self.replaced_links['$$ModelLink$$'] = True
        return compiled_html

    def insert_executions_link(self,
                               link_prefix: str,
                               compiled_html: str,
                               service: str = None,
                               execution: dl.Execution = None):
        if service is not None and execution is not None:
            dt = datetime.strptime(execution.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            dt_adjusted = dt - timedelta(seconds=30)
            timestamp_ms_adjusted = int(dt_adjusted.timestamp() * 1000)
            executions_link = f"{link_prefix}/cloudops?tab=executions&page=1&sortBy=createdAt&descending=true&status=failed&service.id={service}&updatedAt[$gt]={timestamp_ms_adjusted}"
            compiled_html = compiled_html.replace('$$ServiceExecutionsLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Executions:</span><a href={0}>Service Executions</a></div>'.format(
                                                      executions_link))
            self.replaced_links['$$ServiceExecutionsLink$$'] = True
        return compiled_html

    def insert_pipeline_link(self, link_prefix: str,
                             compiled_html: str,
                             pipeline: str = None):
        if pipeline is not None:
            pipeline_link = link_prefix + "/pipelines/{}".format(pipeline)
            resource_name = self.get_resource_name(pipeline, self.get_pipeline, NotificationResourceType.PIPELINES)
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
            resource_name = self.get_resource_name(task, self.get_task, NotificationResourceType.TASKS)
            compiled_html = compiled_html.replace('$$TaskLink$$',
                                                  '<div><span style="color: #171723; padding-right: 2px;">Task:</span><a href={0}>{1}</a></div>'.format(
                                                      task_link, resource_name))
            self.replaced_links['$$TaskLink$$'] = True
        return compiled_html

    def insert_assignment_link(self, link_prefix: str,
                               compiled_html: str):
        resource_type = self.application_input.get_resource_type()
        if resource_type == NotificationResourceType.ASSIGNMENTS:
            assignment = self.application_input.get_resource_id()
        else:
            assignment = self.application_input.get_assignment()
        if assignment is None:
            return compiled_html

        assignments_link = link_prefix + "/assignments/{0}/items".format(assignment)
        assignment_name = self.get_resource_name(assignment, self.get_assignment, NotificationResourceType.ASSIGNMENTS)
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
                compiled = self.insert_model_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    model=self.application_input.get_model()
                )
                compiled = self.insert_pipeline_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    pipeline=self.application_input.get_pipeline()
                )
            elif resource_type == NotificationResourceType.EXECUTIONS:
                service = self.application_input.get_service()
                execution = dl.executions.get(execution_id=self.application_input.get_resource_id())
                compiled = self.insert_service_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service
                )
                compiled = self.insert_executions_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    service=service,
                    execution=execution
                )
                compiled = self.insert_model_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    model=self.application_input.get_model()
                )
                compiled = self.insert_pipeline_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                    pipeline=self.application_input.get_pipeline()
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
            elif resource_type == NotificationResourceType.ANNOTATIONS:
                compiled = self.insert_assignment_link(
                    link_prefix=link_prefix,
                    compiled_html=compiled,
                )
        for link in ["$$ProjectLink$$",
                     "$$ServiceLink$$",
                     "$$ServiceLogsLink$$",
                     "$$ServiceExecutionsLink$$",
                     "$$PipelineLink$$",
                     "$$TaskLink$$",
                     "$$AssignmentLink$$",
                     "$$ModelLink$$"
                     ]:
            if link not in self.replaced_links:
                compiled = compiled.replace(link, '')
        return compiled

    def compile_html(self, template):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.insert_links(compiled)
        return [compiled, attachments]
