from .models import UserInformation


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['is_teacher'] = self.check_teacher(context['user'])

        try:
            user_class = UserInformation.objects.get(user=context['user']).user_class.name_class
            context['is_kicked'] = user_class == 'kicked'
        except AttributeError:
            pass

        return context

    def check_teacher(self, user):
        if user.groups.filter(id=5):
            return True
        else:
            return False
