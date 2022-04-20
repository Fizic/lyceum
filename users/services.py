from users.forms import ProfileForm


def get_profile_data(request) -> dict:
    user = request.user
    ratings = user.rating.filter(star=5).select_related("item").only("item__name")
    form = ProfileForm()
    context = {"user": user, "ratings": ratings, "form": form}
    return context
