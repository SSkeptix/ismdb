from account import tuples;


def validation_permission(user):
	if user.category == tuples.CATEGORY.TEACHER and user.validated_by:
		return True
	else:
		return False