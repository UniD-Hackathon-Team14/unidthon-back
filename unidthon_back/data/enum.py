import enum


class AnswerType(enum.Enum):
    AUDIO = 'audio'
    IMAGE = 'image'

    TYPE = (
        (AUDIO, '음성'),
        (IMAGE, '사진'),
    )