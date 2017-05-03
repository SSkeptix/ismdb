# for 'edit_profile' and 'profile'
class Skill:
	value = None
	id = None
	validated_by = None
	validated_by_username = None
	validated_at = None

	def __init__(self, skill):
		self.value = skill.skill.__str__()
		if skill.validated_by:
			self.validated_by = '{0} {1}'.format(skill.validated_by.last_name, skill.validated_by.first_name)
			self.validated_by_username = skill.validated_by.username
			self.validated_at = skill.validated_at

		self.id = skill.id