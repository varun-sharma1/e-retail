"""
Author: Varun
"""
import json

from rest_framework import viewsets

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus

from .serializers import OrderSerializer
from .models import Order


def validate_user_session(id, token):
    """validates the user session

    id: id of user.
    token: session token.
    """

    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except user_model.DoesNotExist:
        return False


def get_total_products(products):
    """
    counts the number of products in an order.

    products: list of all the products in the cart
    """

    total_count = 0
    product_list = json.loads(products)
    for product in product_list:
        total_count += product['count']

    return total_count


@csrf_exempt
def add(request, id, token):
    """Adds order to db

    id: user id
    token: authentication token
    """
    if not validate_user_session(id, token):
        return {'error': 'Please login again.'}

    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']

        total_pro = get_total_products(products)

        user_model = get_user_model()

        try:
            user = user_model.objects.get(pk=id)
        except user_model.DoesNotExist:
            return {'error': 'User does not exist'}

        ordr = Order(
            user=user, product_names=products, total_products=total_pro,
            transaction_id=transaction_id, total_amount=amount
        )

        ordr.save()
        return JsonResponse({
            'success': True,
            'error': 'False',
            'msg': 'order placed successfully.'
        }, status=HTTPStatus.CREATED)


@csrf_exempt
def get_orders(request, id, token):
    """GET orders by a user

    id: user id
    token: authentication token
    """

    if request.method != 'GET':
        return {'message': 'Error. Please use get method'}

    if not validate_user_session(id, token):
        return {'error': 'Please login again.'}

    query = Order.objects.filter(user_id=id)
    orders_list = list(query.values())

    return JsonResponse({'orders': orders_list}, safe=False, status=HTTPStatus.OK)


class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset"""

    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
