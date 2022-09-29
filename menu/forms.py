from django import forms
from menu.models import Category, FoodItem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
    

class FoodItemForm(forms.ModelForm):
    #styling the image input of our add_food.html with custom file
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),validators=[allow_only_images_validator])
    class Meta:
        model = FoodItem  # import from menu.models
        # fields user will enter
        fields = ['category','food_title','description','price','image','is_available'] 