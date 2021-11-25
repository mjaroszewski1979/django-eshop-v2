from django.test import TestCase, Client
from vendor.models import Vendor
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import become_vendor, vendor_admin, edit_vendor, vendors, vendor
from django.contrib.auth.forms import UserCreationForm




class VendorTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.data={
            'username' : 'maciej',
            'password1' : 'jaroszewski123',
            'password2' : 'jaroszewski123'
        }
        self.form = UserCreationForm(self.data)
        self.user = self.form.save()
        self.new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        self.pk=self.new_vendor.id

    def test_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_form_no_valid_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_become_vendor_url_is_resolved(self):
        url = reverse('become_vendor')
        self.assertEquals(resolve(url).func, become_vendor)

    def test_become_vendor_get(self):
        response = self.client.get(reverse('become_vendor'))
        form = UserCreationForm()
        self.assertContains(response, 'Become vendor | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/become_vendor.html') 
        self.assertIsNotNone(response.context['form'])
        self.assertEquals(type(response.context['form']), type(form))

    def test_become_vendor_post(self):
        data={
            'username' : 'maciej123',
            'password1' : 'jaroszewski',
            'password2' : 'jaroszewski'
        }
        response = self.client.post(reverse('become_vendor'), data, follow=True)
        self.assertContains(response, 'Welcome | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/frontpage.html')

    def test_vendors_url_is_resolved(self):
        url = reverse('vendors')
        self.assertEquals(resolve(url).func, vendors)

    def test_vendors_view(self):
        vendors = Vendor.objects.all()
        response = self.client.get(reverse('vendors'))
        self.assertContains(response, 'Vendors | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendors.html') 
        self.assertIsNotNone(response.context['vendors'])
        self.assertIsNotNone(self.new_vendor)
        self.assertEquals(vendors.count(), 1)

    def test_vendor_url_is_resolved(self):
        url = reverse('vendor', args=(self.pk,))
        self.assertEquals(resolve(url).func, vendor)

    def test_vendor_view(self):
        response = self.client.get(reverse('vendor', args=(self.pk,)))
        vendor = Vendor.objects.get(id=self.pk)
        self.assertContains(response, vendor.name , status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor.html') 
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(vendor))
        self.assertIsNotNone(vendor)

    def test_vendor_admin_url_is_resolved(self):
        url = reverse('vendor_admin')
        self.assertEquals(resolve(url).func, vendor_admin)

    def test_vendor_admin_view(self):
        self.client.login(username='maciej', password='jaroszewski123')
        response = self.client.get(reverse('vendor_admin'))
        self.assertContains(response, 'Vendor admin | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor_admin.html')
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(self.new_vendor))

    def test_edit_vendor_url_is_resolved(self):
        url = reverse('edit_vendor')
        self.assertEquals(resolve(url).func, edit_vendor)

    def test_edit_vendor_get(self):
        self.client.login(username='maciej', password='jaroszewski123')
        response = self.client.get(reverse('edit_vendor'))
        self.assertContains(response, 'Edit vendor | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/edit_vendor.html')
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(self.new_vendor))

    def test_edit_vendor_post(self):
        self.client.login(username='maciej', password='jaroszewski123')
        data = {
            'name': 'maciej_new',
            'email': 'maciej@gmail.com'
        }
        response = self.client.post(reverse('edit_vendor'), data, follow=True)
        self.assertContains(response, 'Vendor admin | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor_admin.html')
