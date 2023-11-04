# Unsure whether to have volunteer and admin as subclasses of a "User". Do we think admin is allowed to do
# Everything that a volunteer can do? Or maybe we just have volunteer as parent class and admin as child?
class Volunteer:

    total_number = 0

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        Volunteer.total_number += 1

    def edit_personal_info(self):
        pass

    def edit_camp_info(self):
        # Should this sit in the camp class & be called by volunteer?
        pass

    def create_refugee_profile(self):
        # Should this just sit in the refugee class and be called by volunteer?
        pass
