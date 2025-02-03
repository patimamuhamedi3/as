from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Item, Customer, Order, Supplier
from inventory.serializers import ItemSerializer, OrderSerializer, CustomerSerializer, SupplierSerializer

# ViewSets for main models
class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# Generic API for CRUD operations
@permission_classes([IsAuthenticated])
def generic_api(model_class, serializer_class):
    """
    A generic API view function for performing CRUD operations.
    """
    @api_view(['GET', 'POST', 'DELETE', 'PUT'])
    def api(request, id=None):
        if request.method == 'GET':
            if id:
                instance = get_object_or_404(model_class, id=id)
                serializer = serializer_class(instance)
                return Response(serializer.data)
            else:
                instances = model_class.objects.all()
                serializer = serializer_class(instances, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            if id:
                instance = get_object_or_404(model_class, id=id)
                serializer = serializer_class(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if id:
                instance = get_object_or_404(model_class, id=id)
                instance.delete()
                return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return api

# Create endpoints using generic_api
manage_item = generic_api(Item, ItemSerializer)
manage_customer = generic_api(Customer, CustomerSerializer)
manage_order = generic_api(Order, OrderSerializer)
manage_supplier = generic_api(Supplier, SupplierSerializer)
