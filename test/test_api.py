from email import header
import pytest
import requests
import json

class TestApi():
    petId = 4

    def test_add_pet(self):
        payload = { 
            
                "id": self.petId,
                "category": {
                    "id": 0,
                    "name": "dog"
                },
                "name": "Tuss",
                "photoUrls": [
                    "https://www.google.com/search?q=dog&sxsrf=ALiCzsaW9nb2vrLx4efebqk_ySfsjqf_zA:1665490897583&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiby86Kldj6AhXnlIsKHVCTD_YQ_AUoAXoECAEQAw&biw=1440&bih=720&dpr=2#imgrc=4KuumRzJNAZn_M"
                ],
                "tags": [
                    {
                    "id": 0,
                    "name": "cute"
                    }
                ],
                "status": "available"
        }
        response = requests.post('http://localhost/v2/pet' , json=payload)
        resultJson = json.loads(response.text)
        assert response.status_code == 200 
        assert resultJson['category']['name'] == 'dog'
        assert resultJson['name'] == 'Tuss'
        assert resultJson['id'] == self.petId
        
    @pytest.mark.parametrize("status, expected", [("available", "available"), ("pending", "pending"), ("sold", "sold")]) 
    def test_status_pet(self, status, expected):
        params = {"status": status}
        response = requests.get('http://localhost/v2/pet/findByStatus', params=params)
        resultJson = json.loads(response.text)
        assert response.status_code == 200
        assert resultJson[0]['status'] == expected
   
    @pytest.mark.parametrize("status, quantity", [("placed", 2), ("approved", 3), ("delivered", 4)])
    def test_place_order(self, status, quantity):
        payload = { 
            "id": 0,
            "petId": self.petId,
            "quantity": quantity,
            "shipDate": "2022-10-11T14:26:48.290Z",
            "status": status  
        }

        response = requests.post('http://localhost/v2/store/order', json=payload)
        resultjson = json.loads(response.text)
        assert response.status_code == 200
        assert resultjson['petId'] == self.petId
        assert resultjson['status'] == status
        assert resultjson['quantity'] == quantity

    def test_delete_pet(self):
        response = requests.delete(f'http://localhost/v2/pet/{self.petId}')
        resultjson = json.loads(response.text)
        assert response.status_code == 200
        assert resultjson['message'] == str(self.petId)       


    