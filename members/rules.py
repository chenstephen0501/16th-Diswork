import rules

@rules.predicate
def is_member_user(user):
    return user.is_authenticated and user.member_status == "1"

rules.add_perm('user_can_show', is_member_user)