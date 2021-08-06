from django.contrib.auth.management.commands import createsuperuser

class Command (createsuperuser.Command):
    help = 'Auth0のスーパーユーザーを作成するコマンド'

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        username = 'auth0user'
        email = 'auth0@gmail.com'
        password = 'admin'
        auth0_id = 'auth0user'
        database = options.get('database')

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'auth0_id': auth0_id,
        }
        exists = self.UserModel._default_manager.db_manager(database).filter(username=username).exists()

        if not exists:
            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
