import reflex as rx
from . import routes


class NavState(rx.State):
    
    # Home and About Routes
    def to_home(self):
        return rx.redirect(routes.HOME_ROUTE)
    def to_about_us(self):
        return rx.redirect(routes.ABOUT_US_ROUTE)
    def to_pricing(self):
        return rx.redirect(routes.PRICE_ROUTE)

    # Blog and Detail routes
    def to_blog(self):
        return rx.redirect(routes.BLOG_POSTS_ROUTE)
    def to_blog_add(self):
        return rx.redirect(routes.BLOG_POSTS_ADD_ROUTE)
    def to_create(self):
        return self.to_blog_add()

    # Contact Routes
    def to_contact(self):
        return rx.redirect(routes.CONTACT_US_ROUTE)