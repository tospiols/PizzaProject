from emoji import emojize
import click
from typing import Callable
import time
import pytest


class BasePizza:
    """The base class for all pizzas.
    Contains basic attributes for all pizzas to not repeat any code.
    Class attributes made using properties to keep all attributes in their ranges.
    """

    def __init__(self, sauce="tomato sauce", cheese="mozzarella", size="L"):
        self.sauce = sauce
        self.cheese = cheese
        self.size = size

    @property
    def sauce(self):
        return self._sauce

    @sauce.setter
    def sauce(self, value: str):
        if value not in ["tomato sauce", "no sauce"]:
            raise ValueError("Sauce must be tomato sauce or no sauce")
        self._sauce = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: str):
        if value not in ["L", "XL"]:
            raise ValueError("Size must be L or XL")
        self._size = value

    @property
    def cheese(self):
        return self._cheese

    @cheese.setter
    def cheese(self, value: str):
        if value not in ["mozzarella", "no cheese"]:
            raise ValueError("Cheese must be Mozzarella or no cheese")
        self._cheese = value

    def dict(self, emoji: str):
        recipe = [f"{self.__dict__[value]}" for value in self.__dict__]
        return f"Pizza {emoji}: " + ", ".join(recipe)


class Pepperoni(BasePizza):
    """The class for pepperoni, made in the same line with BasePizza."""

    def __init__(self, meat="pepperoni"):
        super().__init__()
        self.meat = meat

    @property
    def meat(self):
        return self._meat

    @meat.setter
    def meat(self, value: str):
        if value not in ["pepperoni", "no meat"]:
            raise ValueError("Meat must be pepperoni or no meat")
        self._meat = value

    def dict(self, signature="Pepperoni:pizza:"):
        return super().dict(emojize(signature))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Margherita(BasePizza):
    """The class for margherita, made in the same line with BasePizza.
    Contains specific ingredients common only for this pizza."""

    def __init__(self, tomatoes="tomatoes"):
        super().__init__()
        self.tomatoes = tomatoes

    @property
    def tomatoes(self):
        return self._tomatoes

    @tomatoes.setter
    def tomatoes(self, value: str):
        if value not in ["tomatoes", "no tomatoes"]:
            raise ValueError("Meat must be tomatoes or no tomatoes")
        self._tomatoes = value

    def dict(self, signature: str = "Margherita:tomato:"):
        return super().dict(emojize(signature))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Hawaiian(BasePizza):
    """The class for hawaiian pizza, made in the same line with BasePizza."""

    def __init__(self, meat="chicken", pineapple="pineapples"):
        super().__init__()
        self.meat = meat
        self.pineapple = pineapple

    @property
    def pineapple(self):
        return self._pineapple

    @pineapple.setter
    def pineapple(self, value: str):
        if value not in ["pineapples", "no pineapples"]:
            raise ValueError("Meat must be pineapples or no pineapples")
        self._pineapple = value

    def dict(self, signature: str = "Hawaiian:pineapple:"):
        return super().dict(emojize(signature))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


# Part 3: decorators


def log(comment: str) -> Callable:
    def time_counter(func: Callable) -> Callable:
        def inner_counter(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            print(comment.format(time.time() - start))
            return func(*args, **kwargs)

        return inner_counter

    return time_counter


# Part 2: CLI

MENU = {"margherita": Margherita(), "pepperoni": Pepperoni(), "hawaiian": Hawaiian()}


@log("Cooked in {}s")
def bake(pizza: BasePizza):
    pass


@log("Delivered in {}s")
def if_delivery(pizza: BasePizza):
    pass


@log("Picked up in {}s")
def pickup(pizza: BasePizza):
    pass


@click.group()
def cli():
    pass


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool):
    """Cooks and delivers pizza"""
    if pizza not in MENU:
        raise KeyError("We have not learned that pizza yet")

    if delivery:
        if_delivery(MENU[pizza])
    else:
        pickup(MENU[pizza])


@cli.command()
def menu():
    """prints menu"""
    menu_list = []
    for key, value in MENU.items():
        elem = value
        menu_list.append(elem.dict())
    menu_out = "Menu: \n -" + "\n -".join(menu_list)
    print(menu_out)


# Additional part: tests


def test_eq():
    pep = Pepperoni()
    pepp = Pepperoni()
    pepp.size = "XL"
    pepe = Pepperoni()
    pepes = Margherita()
    assert pep != pepp
    assert pepe == pep
    assert pepes != pepe
    assert pepes != pep


def test_exception():
    with pytest.raises(ValueError):
        pep = Pepperoni()
        pep.size = "S"


def test_changes():
    pep = Pepperoni()
    pep.cheese = "no cheese"
    assert pep.dict() == "Pizza Pepperoni🍕: tomato sauce, no cheese, L, pepperoni"


def test_output():
    pep = Pepperoni()
    assert pep.dict() == "Pizza Pepperoni🍕: tomato sauce, mozzarella, L, pepperoni"


if __name__ == "__main__":
    cli()
