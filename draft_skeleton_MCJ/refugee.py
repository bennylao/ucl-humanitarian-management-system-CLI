# Create refugee profile for each refugee including their family. Each
# refugee must be logged with: their camp identification, medical
# condition, etc. Keep it simple, you can assume a family is a singular
# entity, rather than their constituent members. <-- what does this mean?

class Refugee:

    def __init__(self, is_vaccinated = False):
        """Need to prompt user to fill in camp ID, medical condition, family name.
        Refugee is instantiated as not_vaccinated unless they are specified as True
        (something to add in User Manual??)"""
        self.family_name = family_name
        self.medical_condition = medical_condition
        self.associated_camp = associated_camp
        self.is_vaccinated = is_vaccinated


    def vaccinate_refugee(self):
        # How do we add logic here? Do we need to subtract one from the vaccines available
        # to this specific camp? Ie we've distributed our resource across our camps,
        # we can see what is available to this camp, and we want to use one of the
        # vaccinations to vaccinate a refugee. We should probably include logic to
        # subtract one vaccine from those available to the camp which this refugee belongs to
        pass

