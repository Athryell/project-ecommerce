from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("display_category/<str:category_type>", views.display_category, name="display_category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:article_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:article_id>", views.remove_watchlist, name="remove_watchlist"),
    path("remove_listing/<int:remove_id>", views.remove_listing, name="remove_listing"),
    path("listing/<int:article_id>", views.listing, name="listing"),
    path("post_comment/<int:article_id>", views.post_comment, name="post_comment"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("close/<int:article_id>", views.close, name="close"),
    path("closed_auctions", views.closed_auctions, name="closed_auctions")
]
