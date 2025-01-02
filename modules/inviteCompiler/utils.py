class InviteCompilerUtils:
    @staticmethod
    def generate_redirect_link(body, env_prefix, base_path):
        is_user_registered = InviteCompilerUtils.get_body_param(body, 'isUserRegistered', default=False)
        if is_user_registered:
            return InviteCompilerUtils.redirect_resource(body, env_prefix, base_path)
        return InviteCompilerUtils.redirect_signup(body, env_prefix, base_path)

    def get_body_param(body, key, default=None):
        return body.get(key, default)

    @staticmethod
    def get_resource_id(body):
        return InviteCompilerUtils.get_body_param(body, 'id', default='Unknown id')

    @staticmethod
    def redirect_signup(body, env_prefix, base_path):
        resource_id = InviteCompilerUtils.get_resource_id(body)
        redirect_path = f"/{base_path}/{resource_id}"
        query_params = InviteCompilerUtils.encode_query_params({
            "redirect": redirect_path.replace('/', '%2F'),
            "link_source": "email_invitation"
        })
        return InviteCompilerUtils.build_url(env_prefix, 'welcome', query_params=query_params)

    @staticmethod
    def redirect_resource(body, env_prefix, base_path):
        resource_id = InviteCompilerUtils.get_resource_id(body)
        return InviteCompilerUtils.build_url(env_prefix, base_path, resource_id=resource_id)

    @staticmethod
    def build_url(env_prefix, base_path, resource_id=None, query_params=None):
        domain = env_prefix.rstrip('/')
        url = f'{domain}/{base_path}'
        if resource_id:
            url = f'{url}/{resource_id}'
        if query_params:
            url = f'{url}?{query_params}'
        return url

    @staticmethod
    def encode_query_params(params):
        return '&'.join(f"{key}={value}" for key, value in params.items())