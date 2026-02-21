from me.models import Profile


def profile_context(request):
    return {"site_profile": Profile.objects.first()}
