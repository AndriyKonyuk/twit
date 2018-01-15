from menu import Menu, MenuItem
from django.urls import reverse


# Add two items to our main menu
Menu.add_item("main", MenuItem("Main", reverse("twit.views.vmain")))

Menu.add_item("main", MenuItem("Search", reverse("twit.views.vsearch")))

Menu.add_item("main", MenuItem("Singin",reverse("twit.views.vlogin")))

Menu.add_item("main", MenuItem("Singup",reverse("twit.views.vregister")))

Menu.add_item("main", MenuItem("Logout",reverse("twit.views.vlogout")))


# Define children for the my account menu
# myaccount_children = (
#     MenuItem("Edit Profile",
#              reverse("accounts.views.editprofile"),
#              weight=10,
#              icon="user"),
#     MenuItem("Admin",
#              reverse("admin:index"),
#              weight=80,
#              separator=True,
#              check=lambda request: request.user.is_superuser),
#     MenuItem("Logout",
#              reverse("accounts.views.logout"),
#              weight=90,
#              separator=True,
#              icon="user"),
# )

# Add a My Account item to our user menu
# Menu.add_item("user", MenuItem("My Account",
#                                reverse("accounts.views.myaccount"),
#                                weight=10,
#                                children=myaccount_children))