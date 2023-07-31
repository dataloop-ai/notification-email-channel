from pathlib import Path


class AssetsLoader:
    @staticmethod
    def read(file_name, flag):
        return open(Path(__file__).with_name(file_name), flag).read()

    @staticmethod
    def get_logo():
        return AssetsLoader.read('logo.png', 'rb')

    @staticmethod
    def get_info_icon():
        return AssetsLoader.read('icon-dl-info-filled.png', 'rb')

    @staticmethod
    def get_warning_icon():
        return AssetsLoader.read('icon-dl-alert-filled.png', 'rb')

    @staticmethod
    def get_error_icon():
        return AssetsLoader.read('icon-dl-error-filled.png', 'rb')

    @staticmethod
    def get_template(template):
        return AssetsLoader.read('{0}.html'.format(template), 'r')
