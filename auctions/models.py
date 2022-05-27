from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, HiddenInput, TextInput, NumberInput, Textarea, FileInput, Select


class User(AbstractUser):
    pass


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Generic', 'Generics'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Pets', 'Pets'),
        ('Cool Stuff', 'Cool Stuff'),
        ('Food', 'Food'),
        ('Books', 'Books'),
    )
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category
    

class Listing(models.Model):
    is_active = models.BooleanField(default='True')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won', blank=True, null=True)
    img = models.ImageField(upload_to='products', null=True, blank=True)
    name_article = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.name_article}: created on {self.created_on} by {self.created_by}. Active: {str(self.is_active).upper()}'


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['name_article', 'price', 'category', 'description', 'created_by', 'img']
        widgets = {
            'created_by': HiddenInput(),
            'name_article': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'img': FileInput(attrs={'class': 'form-control-file'}),
            'is_active': HiddenInput()
        }

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=7, decimal_places=2)
    bid_listings_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing", blank=True)
    bid_created_by_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user", blank=True)
    bid_created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bid_created_by_id} bid ${self.bid_amount} for {self.bid_listings_id.name_article}'

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bid_listings_id', 'bid_created_by_id']
        widgets = {
            'bid_listings_id': HiddenInput(),
            'bid_created_by_id': HiddenInput()
            }


class WatchlistManager(models.Manager):
    def create_watchlist(self, user):
        user = self.create(user=user)
        return user


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="watchlist")
    products = models.ManyToManyField(Listing, related_name="watched_by", blank=True)

    objects = WatchlistManager()

    def __str__(self):
        return f"{self.user}'s watchlist"
    


class Comment(models.Model):
    content = models.CharField(max_length=255)
    item_commented = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.created_by} about {self.item_commented.name_article}'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'item_commented': HiddenInput(),
            'created_by': HiddenInput()
        }
        labels = {
            "content": ""
        }
        


