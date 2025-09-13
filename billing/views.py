from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Invoice,Payment,InvoiceItem
from .forms import InvoiceForm,PaymentForm,InvoiceItemForm
from .utils import generate_invoice_pdf
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "billing/invoice_list.html", {"invoices": invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "billing/invoice_detail.html", {"invoice": invoice})

@login_required
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("billing:invoice_list")
    else:
        form = InvoiceForm()
    return render(request, "billing/invoice_form.html", {"form": form})

@login_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect("billing:invoice_list")
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, "billing/invoice_form.html", {"form": form})

@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect("billing:invoice_list")
    return render(request, "billing/invoice_confirm_delete.html", {"invoice": invoice})


@login_required
def invoice_pdf(request, pk):
    return generate_invoice_pdf(pk)

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'role', '') == 'admin'


class InvoiceItemCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = InvoiceItem
    form_class = InvoiceItemForm
    template_name = 'billing/invoiceitem_form.html'

    def form_valid(self, form):
        invoice_id = self.kwargs.get('invoice_id')
        invoice = Invoice.objects.get(pk=invoice_id)
        form.instance.invoice = invoice
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('billing:invoice_detail', args=[self.kwargs.get('invoice_id')])


class InvoiceItemUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = InvoiceItem
    form_class = InvoiceItemForm
    template_name = 'billing/invoiceitem_form.html'

    def get_success_url(self):
        return reverse('billing:invoice_detail', args=[self.object.invoice.pk])


class InvoiceItemDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = InvoiceItem
    template_name = 'billing/invoiceitem_confirm_delete.html'

    def get_success_url(self):
        return reverse('billing:invoice_detail', args=[self.object.invoice.pk])


