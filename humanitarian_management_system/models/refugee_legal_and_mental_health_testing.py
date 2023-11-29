# import click
# def create_terminal_link(text, url):
#     return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'
#
# @click.command()
# def open_legal_site():
#
#     links = [
#         ("Refugee Council Legal Advice Site", "https://www.refugeecouncil.org.uk/"),
#         ("Red Cross Legal Support", "https://www.redcross.org.uk/"),
#         ('RETURN', '')
#     ]
#     for i in enumerate(links, 1):
#         click.echo(f"{i}")
#     while True:
#         try:
#             choice = click.prompt("Enter a number for the page you want to redirect to: ", type=int)
#             selected_link = links[choice - 1]
#             if selected_link[0] == 'RETURN':
#                 print("Returning back from this menu.")
#                 return
#             document_name, document_url = selected_link
#             terminal_link = create_terminal_link(document_name, document_url)
#             click.echo(f"Open the document: {terminal_link}")
#         except (ValueError, IndexError):
#                 click.echo("Invalid selection. Please enter a valid number.")
#
# if __name__ == "__main__":
#     # print(f"Open the document: {legal_advice}")
#     open_legal_site()


def legal_advice_support():
    print("Below are links to our partner legal charities to offer legal support to refugees whilst we work on building"
          "our own team."
          "Clicking on these links will direct you to a web page. You will have to return back "
          "to the application manually.")

    links = [
        ("Refugee Council Legal Advice Site", "https://www.refugeecouncil.org.uk/"),
        ("Red Cross Legal Support", "https://www.redcross.org.uk/"),
        ("Refugee Legal Centre", "https://www.refugee-legal-centre.org.uk/"),
        ('RETURN', '')
    ]
    while True:
        for i, (name, url) in enumerate(links, 1):
            print(f"{i}. {name}: {url}")
        user_input = input("Click on one of the above links or enter RETURN to leave this menu: ")
        if user_input.lower() == "RETURN":
            return
        break



legal_advice_support()