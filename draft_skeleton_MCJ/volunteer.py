# Unsure whether to have volunteer and admin as subclasses of a "User". Do we think admin is allowed to do
# Everything that a volunteer can do? Or maybe we just have volunteer as parent class and admin as child?

class Volunteer:
    pass


    def edit_personal_info(self):
        pass

    def edit_camp_info(self):
        # Should this sit in the camp class & be called by volunteer?
        pass


    def create_refugee_profile(self):
        # Should this just sit in the refugee class and be called by volunteer?
        pass

