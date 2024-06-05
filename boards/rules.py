import rules
from members.models import Member

@rules.predicate
def is_board_member(user):
    member = Member.objects.filter(user=user).first()
    if member and member.member_status == 1:
        return True
    else:
        return False
rules.add_perm("boards.create", is_board_member)