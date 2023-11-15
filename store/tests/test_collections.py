from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth.models import User

import pytest

from model_bakery import baker

from store.models import Collection

@pytest.fixture
def create_collection(api_client):
        def do_create_collection(collection):
                return api_client.post('/store/collections/',collection)
        return do_create_collection


# @pytest.mark.filterwarnings("ignore::DeprecationWarning:pkg_resources")
@pytest.mark.django_db
class TestCreateCollection:
        # @pytest.mark.skip
        # api_client is from fixture
        def test_if_user_is_anonymous_returns_401(self,api_client,create_collection):
                # AAA (Arrange, Act, Assert)

                # Arrange → Prepare system under test:create objects or put database on initial state

                # Act → kick of the behavior to test: 
                # send the request
                # client = APIClient()
                # response =  client.post('/store/collections/',{'title':'test'})

                # response =  api_client.post('/store/collections/',{'title':'test'})
                
                response = create_collection({'title':'a'})
                


                # assert
                assert response.status_code == status.HTTP_401_UNAUTHORIZED


        def test_if_user_is_not_admin_returns_403(self,authenticate,create_collection):

                # send the request
                # client = APIClient()
                # client.force_authenticate(user={})
                # response =  client.post('/store/collections/',{'title':'test'})

                # after fixture
                authenticate()
                response =  create_collection({'title':'test'})

                # assert
                assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_data_is_invalid_return_400(self):
                client = APIClient()
                client.force_authenticate(user=User(is_staff=True))
                response =  client.post('/store/collections/',{'title':''})


                # assert
                assert response.status_code == status.HTTP_400_BAD_REQUEST
                assert response.data['title'] is not None
        
        def test_if_data_is_valid_return_201(self):
                client = APIClient()
                client.force_authenticate(user=User(is_staff=True))
                response =  client.post('/store/collections/',{'title':'test'})


                # assert
                assert response.status_code == status.HTTP_201_CREATED
                assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self,api_client):
        # Arrange
        # Collection.objects.create(title='a')
        collection = baker.make(Collection)
        # print(collection.__dict__)

        response =  api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id':collection.id,'title':collection.title,'products_count':0}