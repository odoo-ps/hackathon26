from odoo import http
from odoo.http import request  # noqa: F401


class ShelterController(http.Controller):
    """ The pages of the website of the shelter.

    Keep the controllers thin: the business logic belongs to the models (TODO 1 and TODO 4).
    """

    # ----------------------------------------------------------------------------
    # TODO 2 - The page /adopt
    #
    # A public page of the website (anybody can see it, without logging in), which
    # renders the template trivia_animal_shelter.animal_list with the adoptable
    # animals (TODO 1). An optional parameter filters the species: /adopt?species=cat
    # ----------------------------------------------------------------------------
    @http.route(['/adopt'], auth='public', website=True)
    def adopt_index(self, species=None):
        all_species = request.env['shelter.animal']._get_species()
        current_species = next(iter([s[0] for s in all_species if s[0] == species]), False)
        animals = self.env["shelter.animal"]._get_adoptable_animals(species=current_species)
        return request.render('trivia_animal_shelter.animal_list', {
            'animals': animals,
            'all_species': all_species,
            'current_species': current_species,
        })

    # ----------------------------------------------------------------------------
    # TODO 3 - The page of an animal
    #
    # /adopt/<model("shelter.animal"):animal> renders the template
    # trivia_animal_shelter.animal_detail.
    # ----------------------------------------------------------------------------

    @http.route(['/adopt/<model("shelter.animal"):animal>'], auth='public', website=True)
    def adopt_detail(self, animal):
        return request.render("trivia_animal_shelter.animal_detail", {
            'animal': animal,
        })

    # ----------------------------------------------------------------------------
    # TODO 4 - The adoption request
    #
    # The form of the page of an animal is posted (POST only) to
    # /adopt/<model("shelter.animal"):animal>/request: create the request with
    # shelter.adoption.request._create_from_website(), then render the template
    # trivia_animal_shelter.adoption_thanks.
    # ----------------------------------------------------------------------------

    @http.route(['/adopt/<model("shelter.animal"):animal>/request'], methods=['POST'], auth="public", website=True)
    def adopt_request(self, animal, **values):
        adoption_request = request.env["shelter.adoption.request"]
        if not adoption_request.has_access('create'):
            adoption_request = adoption_request.sudo()

        return request.render("trivia_animal_shelter.adoption_thanks", {
            'animal': animal,
            'adoption_request': adoption_request._create_from_website(animal, values)
        })