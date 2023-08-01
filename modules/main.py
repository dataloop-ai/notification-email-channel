import dtlpy as dl
from modules.compilerFactory import CompilerFactory
from modules.emailDispatcher import EmailDispatcher
from modules.notificationInfo import ApplicationInput
from modules.templateResolver import TemplateResolver


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def email(self, input: dict):
        application_input = ApplicationInput(input)
        if application_input.recipients is None or len(application_input.recipients) == 0:
            return
        template = TemplateResolver.resolve_template(application_input.notification_info.notification_code)
        compiler = CompilerFactory.get_compiler(template=template, application_input=application_input)
        [compiled_html, attachments] = compiler.compile_html(template=template)
        EmailDispatcher.dispatch(application_input=application_input, compiled_html=compiled_html, attachments=attachments)
