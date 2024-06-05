import rules

@rules.predicate
# def is_comment_user(user, comment):
#     return comment.comment.member == user

# def comment_rule():
#     rules.add_perm('user_can_show', is_comment_user)

def is_comment_user(user, comment=None):
    if not user.is_authenticated:
        return False
    return user.member_status == 1