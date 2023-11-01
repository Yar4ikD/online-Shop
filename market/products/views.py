from comments.forms import CommentAddForm
from comments.models import Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Min
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormMixin, FormView
from shops.models import (
    Offer,
)

from .forms import UploadFileForm
from .models import (
    ProductDetail,
    Product,
)
from basket.forms import BasketAddProductForm
from history.models import BrowsingHistory
from shops.tasks import etl_task


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = CommentAddForm
    template_name = "products/product-detail.jinja2"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        offers = Offer.objects.prefetch_related("shop").filter(product_id=self.object.pk)
        product_details = ProductDetail.objects.prefetch_related("detail", "product").filter(product=self.object)
        comments = Comment.objects.select_related("author", "product").filter(product_id=self.object.pk)[:10]
        comment_count = Comment.objects.filter(product_id=self.object.pk).count()

        form_basket = BasketAddProductForm

        if self.request.user.is_authenticated:
            history_object, created = BrowsingHistory.objects.update_or_create(
                user=self.request.user,
                product=self.get_object(),
                defaults={
                    "user": self.request.user,
                    "product": self.get_object(),
                },
            )
            data["history"] = history_object

        data["offers"] = offers
        data["product_detail"] = product_details
        data["min_price"] = offers.aggregate(Min("price"))["price__min"]
        data["comments_list"] = comments
        data["comment_count"] = comment_count
        data["form_basket"] = form_basket

        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save()
        comment.author = self.request.user
        comment.product = Product.objects.get(pk=self.kwargs["pk"])
        comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.object.pk})


class UploadFileView(PermissionRequiredMixin, FormView):
    template_name = "products/upload_file.jinja2"
    form_class = UploadFileForm
    success_url = reverse_lazy("products:upload_file")
    permission_required = [
        "products.add_detail",
        "products.add_product",
        "products.add_productdetail",
        "products.add_productimage",
    ]

    def form_valid(self, form):
        form.save()
        self.success_message = _("Файл успешно загружен.")

        etl_task.delay()
        return super().form_valid(form)
