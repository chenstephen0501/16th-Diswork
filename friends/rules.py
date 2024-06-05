import rules

@rules.predicate
def is_friend_user(member_id):
    if not member_id.is_authenticated:
        return False
    return member_id.member_status == 1

rules.add_perm('friend_can_show', is_friend_user)