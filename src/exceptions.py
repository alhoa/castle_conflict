class CorruptedSaveError(Exception):
	def __init__(self, message):
		super(CorruptedSaveError, self).__init__(message)