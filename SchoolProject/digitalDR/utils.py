class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context = {
            'is_teacher': self.check_teacher(context['user'])
        }
        return context

    def check_teacher(self, user):
        if user.groups.filter(id=5):
            return True
        else:
            return False