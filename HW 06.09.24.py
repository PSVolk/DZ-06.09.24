import os
import json
from datetime import datetime

# Модели
class HotDogRecipe:
    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients

class Ingredient:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class HotDogOrder:
    def __init__(self, recipe, extras, payment_method):
        self.recipe = recipe
        self.extras = extras
        self.payment_method = payment_method
        self.total_price = recipe.price + sum(extra.price for extra in extras)
        self.discount = self.calculate_discount()

    def calculate_discount(self):
        if len(self.recipe.ingredients) >= 3:
            return 0.1
        return 0

    def __str__(self):
        extras_str = ", ".join(extra.name for extra in self.extras)
        return f"Заказ: {self.recipe.name} с {extras_str}. Итого: {self.total_price:.2f} руб. Скидка: {self.discount*100}%"

# Контроллер
class HotDogShop:
    def __init__(self):
        self.recipes = []
        self.ingredients = []
        self.orders = []
        self.revenue = 0
        self.profit = 0

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def place_order(self, recipe, extras, payment_method):
        order = HotDogOrder(recipe, extras, payment_method)
        self.orders.append(order)
        self.revenue += order.total_price
        self.profit += order.total_price * (1 - order.discount)
        self.update_ingredients(recipe, extras)
        return order

    def update_ingredients(self, recipe, extras):
        for ingredient in recipe.ingredients:
            for i in self.ingredients:
                if i.name == ingredient.name:
                    i.quantity -= 1
                    break
        for extra in extras:
            for i in self.ingredients:
                if i.name == extra.name:
                    i.quantity -= 1
                    break

    def check_ingredients(self):
        low_ingredients = [i for i in self.ingredients if i.quantity < 10]
        if low_ingredients:
            print("Необходимо пополнить следующие ингредиенты:")
            for ingredient in low_ingredients:
                print(f"{ingredient.name} - {ingredient.quantity} шт.")

    def display_sales_info(self):
        print(f"Всего продано: {len(self.orders)} хот-догов")
        print(f"Общая выручка: {self.revenue:.2f} руб.")
        print(f"Общая прибыль: {self.profit:.2f} руб.")

    def save_orders(self):
        orders_data = [order.__dict__ for order in self.orders]
        with open("orders.json", "w") as f:
            json.dump(orders_data, f, indent=4)

    def load_orders(self):
        if os.path.exists("orders.json"):
            with open("orders.json", "r") as f:
                orders_data = json.load(f)
            self.orders = [HotDogOrder(**order_data) for order_data in orders_data]

# Представление
class HotDogShopView:
    def display_menu(self, shop):
        print("Меню хот-догов:")
        for recipe in shop.recipes:
            print(f"{recipe.name} - {recipe.price:.2f} руб.")
        print("Вы можете создать свой рецепт.")

    def display_extras(self, shop):
        print("Дополнительные ингредиенты:")
        for ingredient in shop.ingredients:
            print(f"{ingredient.name} - {ingredient.price:.2f} руб. (в наличии: {ingredient.quantity} шт.)")


    def display_order(self, order):
        print(order)

    def display_low_ingredients(self, shop):
        shop.check_ingredients()

    def display_sales_info(self, shop):
        shop.display_sales_info()

# Главный код
if __name__ == "__main__":
    shop = HotDogShop()

    # Добавление рецептов
    recipe1 = HotDogRecipe("Классический", 100, [
        Ingredient("Булочка", 20, 100),
        Ingredient("Сосиска", 50, 100),
        Ingredient("Кетчуп", 10, 50),
        Ingredient("Горчица", 10, 50)
    ])
    recipe2 = HotDogRecipe("Чили-дог", 120, [
        Ingredient("Булочка", 20, 100),
        Ingredient("Сосиска", 50, 100),
        Ingredient("Чили", 15, 50),
        Ingredient("Лук", 10, 50)
    ])
    recipe3 = HotDogRecipe("Вегетарианский", 90, [
        Ingredient("Булочка", 20, 100),
        Ingredient("Соевая сосиска", 30, 100),
        Ingredient("Кетчуп", 10, 50),
        Ingredient("Майонез", 10, 50)
    ])
    shop.add_recipe(recipe1)
    shop.add_recipe(recipe2)
    shop.add_recipe(recipe3)

    # Добавление ингредиентов
    shop.add_ingredient(Ingredient("Булочка", 20, 100))
    shop.add_ingredient(Ingredient("Сосиска", 50, 100))
    shop.add_ingredient(Ingredient("Кетчуп", 10, 50))
    shop.add_ingredient(Ingredient("Горчица", 10, 50))
    shop.add_ingredient(Ingredient("Чили", 15, 50))
    shop.add_ingredient(Ingredient("Лук", 10, 50))
    shop.add_ingredient(Ingredient("Соевая сосиска", 30, 100))
    shop.add_ingredient(Ingredient("Майонез", 10, 50))

    # Работа с приложением
    view = HotDogShopView()
    view.display_menu(shop)
    view.display_extras(shop)

    order = shop.place_order(recipe1, [shop.ingredients[2], shop.ingredients[3]], "Наличные")
    view.display_order(order)

    order = shop.place_order(recipe2, [shop.ingredients[4], shop.ingredients[5]], "Карта")
    view.display_order(order)

    order = shop.place_order(recipe3, [shop.ingredients[6], shop.ingredients[7]], "Наличные")
    view.display_order(order)

    view.display_low_ingredients(shop)
    view.display_sales_info(shop)
    shop.save_orders()
