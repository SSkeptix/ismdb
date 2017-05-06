# for 'edit_profile' and 'profile'
class Skill:
	value = None
	id = None
	validated_by = None
	validated_by_username = None
	updated = None

	def __init__(self, skill):
		self.value = skill.skill.__str__()
		if skill.validated_by:
			self.validated_by = skill.validated_by
			self.validated_by_username = skill.validated_by.username
			self.updated = skill.updated

		self.id = skill.id