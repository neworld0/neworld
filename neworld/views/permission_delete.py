from neworld.models import Question, Answer, Meditation, Research
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Question)
permission = Permission.objects.delete(
    codename='can_delete',
    name='Can Delete Posts',
    content_type=content_type,
)


content_type = ContentType.objects.get_for_model(Answer)
permission = Permission.objects.delete(
    codename='can_delete',
    name='Can Delete Posts',
    content_type=content_type,
)


content_type = ContentType.objects.get_for_model(Meditation)
permission = Permission.objects.delete(
    codename='can_delete',
    name='Can Delete Posts',
    content_type=content_type,
)


content_type = ContentType.objects.get_for_model(Research)
permission = Permission.objects.delete(
    codename='can_delete',
    name='Can Delete Posts',
    content_type=content_type,
)
