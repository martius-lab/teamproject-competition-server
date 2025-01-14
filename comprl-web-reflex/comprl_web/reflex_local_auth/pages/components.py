import reflex as rx

PADDING_TOP = "10vh"
MIN_WIDTH = "50vw"


def input_100w(name, **props) -> rx.Component:
    """Render a 100% width input.

    Returns:
        A reflex component.
    """
    if "placeholder" not in props:
        props["placeholder"] = name.replace("_", " ").title()

    return rx.input(
        id=name,
        name=name,
        width="100%",
        **props,
    )
