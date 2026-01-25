from modules.emailCompiler import EmailCompiler
import dtlpy as dl
from modules.notificationInfo import NotificationResourceType, ApplicationInput
from datetime import datetime, timedelta


class NotificationEmailCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)

        self.replaced_links = dict()


    def insert_log_link(self, link_prefix: str,
                        compiled_html: str, service: str = None):
        if service is not None:
            log_link = link_prefix + "/faas/logs?serviceId={0}".format(service)
            compiled_html = compiled_html.replace('$$ServiceLogsLink$$',
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Logs:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">Service Logs</a></td></tr>'.format(
                                                      log_link))
            self.replaced_links['$$ServiceLogsLink$$'] = True
        return compiled_html

    def insert_service_link(self, link_prefix: str,
                            compiled_html: str, service: str = None):
        if service is not None:
            service_link = link_prefix + "/services/{0}".format(service)
            resource_name = self.get_resource_name(service, self.get_service, NotificationResourceType.SERVICES)
            compiled_html = compiled_html.replace('$$ServiceLink$$',
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Service:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
                                                      service_link, resource_name))
            self.replaced_links['$$ServiceLink$$'] = True
        return compiled_html

    def insert_model_link(self, link_prefix: str,
                          compiled_html: str, model: str = None):
        if model is not None:
            model_link = link_prefix + "/model/{0}".format(model)
            resource_name = self.get_resource_name(model, self.get_model, NotificationResourceType.MODELS)
            compiled_html = compiled_html.replace('$$ModelLink$$',
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Model:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
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
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Executions:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">Service Executions</a></td></tr>'.format(
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
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Pipeline:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
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
                                                  '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Task:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
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
                                              '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Assignment:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
                                                  assignments_link, assignment_name))
        self.replaced_links['$$AssignmentLink$$'] = True
        return compiled_html

    def insert_project_link(self, project: str, compiled_html: str):
        project_link_prefix = self.env_prefix + "projects/"
        project_name = self.get_resource_name(project, self.get_project)
        compiled_html = compiled_html.replace('$$ProjectLink$$',
                                              '<tr><td style="width: 79px; padding-bottom: 16px;"><span style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 500; font-size: 14px; line-height: 20px; color: #333333;">Project:</span></td><td style="padding-bottom: 16px;"><a href="{0}" style="font-family: \'Roboto\', Arial, sans-serif; font-weight: 400; font-size: 14px; line-height: 20px; color: #0062AB;">{1}</a></td></tr>'.format(
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
