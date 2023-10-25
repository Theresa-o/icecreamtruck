import factory
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from icecreamtruck.icecreamapi.models import FoodItem, FoodFlavor, Customer

class FoodItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodItem
        # Factory Boy should not save the instance after post generation hooks
        skip_postgeneration_save = True

    name = "test_fooditem"
    price = 5.00


    # Create a SimpleUploadedFile to test images
    @factory.post_generation
    def image_data(self, create, extracted, **kwargs):
        if not create:
            return

        image_path = "images/minticecream/minticecream.jpg"
        image_data = open(image_path, "rb").read()
        self.image = SimpleUploadedFile("minticecream.jpg", image_data, content_type="image/jpeg")


class FoodFlavorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodFlavor

    name = "test_foodflavor"
    food_item = factory.SubFactory(FoodItemFactory)

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = "test_customer"