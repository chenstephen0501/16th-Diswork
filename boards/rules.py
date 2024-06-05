import rules

@rules.predicate
def is_board_user(member_id):
    if not member_id.is_authenticated:
        return False
    return member_id.member_status == 1

rules.add_perm('board_can_show', is_board_user)