from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Categoria, Plato, Pedido
from .forms import MesaForm, DomicilioForm, RecogerForm, DetallePedidoFormSet

# ==============================================
# Vistas para Administración (CRUD Categorías)
# ==============================================
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'administracion/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

    def get_queryset(self):
        return Categoria.objects.all().order_by('nombre')

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre', 'icono', 'activa']
    template_name = 'administracion/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nombre', 'icono', 'activa']
    template_name = 'administracion/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente')
        return super().form_valid(form)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'administracion/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría eliminada exitosamente')
        return super().form_valid(form)

# ==============================================
# Vistas para Administración (CRUD Platos)
# ==============================================
class PlatoListView(LoginRequiredMixin, ListView):
    model = Plato
    template_name = 'administracion/plato_list.html'
    context_object_name = 'platos'
    paginate_by = 10

    def get_queryset(self):
        return Plato.objects.all().select_related('categoria').order_by('categoria__nombre', 'nombre')

class PlatoCreateView(LoginRequiredMixin, CreateView):
    model = Plato
    fields = ['categoria', 'nombre', 'descripcion', 'precio', 'imagen', 'disponible']
    template_name = 'administracion/plato_form.html'
    success_url = reverse_lazy('plato-list')

    def form_valid(self, form):
        messages.success(self.request, 'Plato creado exitosamente')
        return super().form_valid(form)

class PlatoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plato
    fields = ['categoria', 'nombre', 'descripcion', 'precio', 'imagen', 'disponible']
    template_name = 'administracion/plato_form.html'
    success_url = reverse_lazy('plato-list')

    def form_valid(self, form):
        messages.success(self.request, 'Plato actualizado exitosamente')
        return super().form_valid(form)

class PlatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Plato
    template_name = 'administracion/plato_confirm_delete.html'
    success_url = reverse_lazy('plato-list')

    def form_valid(self, form):
        messages.success(self.request, 'Plato eliminado exitosamente')
        return super().form_valid(form)

# ==============================================
# Vistas Públicas (Páginas Principales)
# ==============================================
class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'platos_por_categoria'

    def get_queryset(self):
        categorias = Categoria.objects.filter(activa=True)
        platos_por_categoria = {}
        
        for categoria in categorias:
            platos_por_categoria[categoria] = Plato.objects.filter(
                categoria=categoria, 
                disponible=True
            )[:8]  # Limita a 8 platos por categoría
        
        return platos_por_categoria

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activa=True)
        return context

class ServiciosView(TemplateView):
    template_name = 'servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuestros Servicios'
        return context

class QuienesSomosView(TemplateView):
    template_name = 'quienes_somos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quiénes Somos'
        return context

class ContactenosView(TemplateView):
    template_name = 'contactenos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contáctenos'
        return context

# ==============================================
# Vistas para Servicios (Pedidos)
# ==============================================
class PedidoBaseCreateView(CreateView):
    model = Pedido
    success_url = reverse_lazy('servicios')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DetallePedidoFormSet(self.request.POST)
        else:
            context['formset'] = DetallePedidoFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save(commit=False)
            # Asignar el tipo de servicio desde el formulario
            self.object.servicio = self.get_service_type()
            self.object.save()
            
            formset.instance = self.object
            formset.save()
            
            messages.success(self.request, f'Pedido de {self.object.get_servicio_display()} creado exitosamente')
            return super().form_valid(form)
        
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_service_type(self):
        """Método abstracto que debe implementarse en cada subclase"""
        raise NotImplementedError("Debes especificar el tipo de servicio")

class MesaCreateView(PedidoBaseCreateView):
    form_class = MesaForm
    template_name = 'mesa_form.html'
    
    def get_service_type(self):
        return 'MESA'

class DomicilioCreateView(PedidoBaseCreateView):
    form_class = DomicilioForm
    template_name = 'domicilio_form.html'
    
    def get_service_type(self):
        return 'DOMICILIO'

class RecogerCreateView(PedidoBaseCreateView):
    form_class = RecogerForm
    template_name = 'recoger_form.html'
    
    def get_service_type(self):
        return 'RECOGER'