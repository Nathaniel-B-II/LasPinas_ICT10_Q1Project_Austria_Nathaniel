# PyScript provides these tools in the browser, not in the local Python environment.
from pyscript import document, when  # type: ignore[reportMissingImports]


def show_view(view_name):
    # Show one panel and hide the other.
    for view_id in ("sku-view", "receipt-view"):
        view = document.getElementById(view_id)
        view.hidden = view_id != view_name

    # Highlight the navigation button for the open panel.
    for button_id in ("sku-nav", "receipt-nav"):
        button = document.getElementById(button_id)
        if button_id == "sku-nav":
            is_active = view_name == "sku-view"
        else:
            is_active = view_name == "receipt-view"
        button.classList.toggle("active", is_active)


# @when runs this function when the matching browser button is clicked.
@when("click", "#generate-button")
def generate_sku(event):
    category = document.getElementById("category").value
    product_name = document.getElementById("product_name").value.strip()
    stock_qty = document.getElementById("quantity").value.strip()
    sku_output = document.getElementById("sku_output")

    if not product_name or not stock_qty:
        sku_output.innerText = "Enter a product name and stock quantity to continue."
        return

    # Slicing keeps only the first three category letters and four product letters.
    sku = category[:3].upper() + "-" + product_name[:4].upper() + "-" + str(stock_qty)
    sku_output.innerText = "SKU: " + sku


@when("click", "#order-button")
def create_order(event):
    products = [
        document.getElementById("item1"),
        document.getElementById("item2"),
        document.getElementById("item3"),
        document.getElementById("item4"),
        document.getElementById("item5"),
    ]

    subtotal = 0
    for product in products:
        if product.checked:
            subtotal += float(product.value)

    tax_rate = 0.12
    tax = subtotal * tax_rate
    total = subtotal + tax

    if subtotal == 0:
        document.getElementById("show").innerText = "Select at least one menu item to create an order."
        return

    # :.2f displays money with exactly two decimal places.
    receipt = (
        "==== RECEIPT ====\n\n"
        f"Subtotal: ₱{subtotal:.2f}\n\n"
        f"VAT (12%): ₱{tax:.2f}\n\n"
        f"TOTAL: ₱{total:.2f}"
    )
    document.getElementById("show").innerText = receipt


@when("click", "#clear-order")
def clear_receipt(event):
    document.getElementById("show").innerText = "Your order summary will appear here."


@when("click", "#sku-nav")
def open_sku(event):
    show_view("sku-view")


@when("click", "#receipt-nav")
def open_receipt(event):
    show_view("receipt-view")