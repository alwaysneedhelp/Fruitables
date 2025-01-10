from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField



STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)


STATUS = (
    ('draft', 'Processing'),
    ('disabled', 'Shipped'),
    ('rejected', 'Delivered'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    (1, '★☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}.format(instance.user.id, filename)'


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length = 20, alphabet = 'abcdefgh12345', prefix='cat')
    title = models.CharField(max_length=100, default='Food ')
    image = models.ImageField(upload_to='category', default='category.jpg')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe("<img src = '%s' width='50' height = '50' />" % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Tags(models.Model):
    pass
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length = 20, alphabet = 'abcdefgh12345', prefix='ven')

    title = models.CharField(max_length=100, default='Nestify')
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True, blank=True, default='I am amazing Vendor')

    adress = models.CharField(max_length=100, default='123 Main Street.')
    contact = models.CharField(max_length=100, default='+123 (456) 789')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe("<img src = '%s' width='50' height = '50' />" % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length = 20, alphabet = 'abcdefgh12345', prefix='prod')

    title = models.CharField(max_length=100, default='Fresh Pear')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True, blank=True, default='This is a product')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=9999999, decimal_places=2, default='1.99')
    old_price = models.DecimalField(max_digits=9999999, decimal_places=2, default='1.99')

    specifications = models.TextField(null=True, blank=True)
    life = models.CharField(max_length=100, default='100 Days', null=True, blank=True)
    stock_count = models.CharField(max_length=100, default='10', null=True, blank=True)
    tags = TaggableManager(blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)


    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    feautured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=10, max_length = 20, alphabet = 'abcdefgh12345', prefix='sku')

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src = "%s" width="50" height = "50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price/self.old_price)*100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to='products_images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


######################################## Cart, Order, OrderItems and Adress ########################################
######################################## Cart, Order, OrderItems and Adress ########################################
######################################## Cart, Order, OrderItems and Adress ########################################
######################################## Cart, Order, OrderItems and Adress ########################################
        

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    city= models.CharField(max_length=100, null=True, blank=True)
    country= models.CharField(max_length=100, null=True, blank=True)

    price = models.DecimalField(max_digits=99999, decimal_places=2, default='0.00')
    saved = models.DecimalField(max_digits=99999, decimal_places=2, default='0.00')
    coupons = models.ManyToManyField('Coupon', blank=True)
    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address = models.CharField(max_length=100, null=True, blank=True)


    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='processing')
    oid = ShortUUIDField(null=True, blank=True, length=5, max_length=20, alphabet = '1234567890')

    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cart Orders'



class CartOrderItems(models.Model):
    pid = models.CharField(max_length=200)
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='processing')
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=99999, decimal_places=2, default='1.99')

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def cart_image(self):
        return mark_safe('<img src = "%s" width="50" height = "50" />' % (self.image))
    
    def order_img(self):
        return mark_safe('<img src = "/media/%s" width="50" height = "50" />' % (self.image))
    


######################################## Product Review, wishlists, Address ########################################
######################################## Product Review, wishlists, Address ########################################
######################################## Product Review, wishlists, Address ########################################
######################################## Product Review, wishlists, Address ########################################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def product_image(self):
        return mark_safe("<img src = '%s' width='50' height = '50' />" % (self.image.url))
    
    def __str__(self):
        return self.review
        
    def get_rating(self):
        return self.rating
    

class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'wishlists'
    
    def __str__(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    mobile = PhoneNumberField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'


class Coupon(models.Model):
    code = models.CharField(max_length=10)
    off = models.DecimalField(max_digits=99999, decimal_places=2, default='0.00', blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code