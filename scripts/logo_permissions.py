from django.contrib.auth.models import User, Permission

logoperm = 'manage_logo'

spons_junta = User.objects.filter(userprofile__dept__pk=11)
webops_cores = User.objects.filter(userprofile__dept__pk=12).filter(userprofile__status='core')

print spons_junta
print webops_cores


for guy in spons_junta:
    guy.user_permissions.add(Permission.objects.get(codename=logoperm))
    print guy.first_name, 'added'

for guy in webops_cores:
    guy.user_permissions.add(Permission.objects.get(codename=logoperm))
    print guy.first_name, 'added'