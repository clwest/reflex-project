import reflex as rx
from reflex.style import toggle_color_mode

from ..auth.state import SessionState
from .. import navigation

def sidebar_user_item() -> rx.Component:
    user_info_obj = SessionState.fetch_authenticated_user_info
    username_via_user_obj = rx.cond(SessionState.get_authenticated_username, 
                                    SessionState.get_authenticated_username, 
                                    "Account")
    return  rx.cond( 
        user_info_obj,
                rx.hstack(
                rx.icon_button(
                    rx.icon("user"),
                    size="3",
                    radius="full",
                ),
                rx.vstack(
                    rx.box(
                        rx.text(
                            username_via_user_obj,
                            size="3",
                            weight="bold",
                        ),
                        rx.text(
                            f"{user_info_obj.email}",
                            size="2",
                            weight="medium",
                        ),
                        width="100%",
                    ),
                    spacing="0",
                    align="start",
                    justify="start",
                    width="100%",
                ),
                padding_x="0.5rem",
                align="center",
                justify="start",
                width="100%",
            ),
        rx.fragment("")
    )

def sidebar_logout_item(
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("log-out"),

            rx.text("Log Out", size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "border-radius": "0.5em",
            },
        ),
        # href=href,
        on_click=navigation.NavState.to_logout,
        as_='button',
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_dark_mode_toggle_item(
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.color_mode_cond(
                light=rx.icon("moon"),
                dark=rx.icon("sun"),
            ),

            rx.text(
                rx.color_mode_cond(
                    light="Dark Mode",
                    dark="Light Mode",
                ),
                size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "border-radius": "0.5em",
            },
        ),
        # href=href,
        on_click= toggle_color_mode,
        as_='button',
        underline="none",
        weight="medium",
        width="100%",
    )



def sidebar_item(
    text: str, icon: str, href: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", navigation.routes.HOME_ROUTE),
        sidebar_item("Articles", "globe", navigation.routes.ARTICLE_LIST_ROUTE),
        sidebar_item("Blog", "square-library", navigation.routes.BLOG_POSTS_ROUTE),
        sidebar_item("Chat", "bot", navigation.routes.CHATBOT_ROUTE),
        sidebar_item("Create Post", "square-library", navigation.routes.BLOG_POSTS_ADD_ROUTE),
        sidebar_item("Profile Page", "user", navigation.routes.USER_PROFILE),
        sidebar_item("Contact Us", "mails", navigation.routes.CONTACT_US_ROUTE),
        # sidebar_item("Contact History", "contact-round", navigation.routes.CONTACT_ENTRIES_ROUTE),
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/close.png",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Donkey Betz", size="3", weight="bold"
                    ),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        sidebar_dark_mode_toggle_item(),
                        sidebar_logout_item(),
                        # sidebar_item(
                        #     "Settings", "settings", "/#"
                        # ),
                        # sidebar_item(
                        #     "Log out", "log-out", "/#"
                        # ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    sidebar_user_item(),
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                # position="fixed",
                # left="0px",
                # top="0px",
                # z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                # height="650px",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.icon("align-justify", size=30)
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    rx.icon("x", size=30)
                                ),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    sidebar_dark_mode_toggle_item(),
                                    sidebar_logout_item(),
                                    # sidebar_item(
                                    #     "Settings",
                                    #     "settings",
                                    #     "/#",
                                    # ),
                                    # sidebar_item(
                                    #     "Log out",
                                    #     "log-out",
                                    #     "/#",
                                    # ),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                sidebar_user_item(),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )