from datetime import date

class Individual:
    def __init__(self, id: str, name: str = None, sex: str = None, birthDate: date = None, deathDate: date = None, childIn: str = None, spouseIn: str = None):
        self.id = id
        self.name = name
        self.sex = sex
        self.birthDate = birthDate
        self.deathDate = deathDate
        self.childIn = childIn
        self.spouseIn = spouseIn

    #def readValueFromFields(fields):




class Family:
    def __init__(self, id: str, husbandId: str = None, wifeId: str = None, childIds: list[str] = None, marriageDate: date = None, divorceDate: date = None):
        self.id = id
        self.husbandId = husbandId
        self.wifeId = wifeId
        self.childIds = childIds
        self.marriageDate = marriageDate
        self.divorceDate = divorceDate


class GEDCOMReadException(Exception):
    def __init__(self, message="Error while reading GEDCOM file"):
        self.message = message
        super().__init__(self.message)