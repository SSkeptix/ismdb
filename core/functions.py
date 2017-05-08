from account import tuples;


def validation_permission(user):
	if not user.is_authenticated:
		return False
		
	if user.category == tuples.CATEGORY.TEACHER and user.validated_by:
		return True
	else:
		return False