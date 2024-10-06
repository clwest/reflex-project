import reflex as rx

from .state import (
    BlogAddFormState,
    BlogEditFormState
)

def blog_post_add_form() -> rx.Component:      
    return rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        name="title",
                        placeholder="Title",
                        required=True,
                        width='100%'
                        
                    ),
                    width="100%",
                ),
                rx.text_area(
                    name='content',
                    placeholder='Your Message',
                    required=True,
                    height='50vh',
                    width='100%'
                    ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=BlogAddFormState.handle_submit,
            reset_on_submit=True,
        ),

def blog_post_edit_form() -> rx.Component:   
    post = BlogEditFormState.post
    title = post.title
    
    post_content = BlogEditFormState.post_content  

    
    return rx.form(
            rx.box(
                rx.input(
                    type='hidden',
                    name='post_id',
                    value=post.id
                ),
                display='none'
            ),
            rx.vstack(
                rx.hstack(
                    rx.input(
                        default_value=title,
                        name="title",
                        placeholder="Title",
                        required=True,
                        width='100%'
                        
                    ),
                    width="100%",
                ),
                rx.text_area(
                    value=post_content,
                    on_change=BlogEditFormState.set_post_content,
                    name='content',
                    placeholder='Your Message',
                    required=True,
                    height='50vh',
                    width='100%'
                    ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=BlogEditFormState.handle_submit
        ),
    

