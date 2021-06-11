import datetime
import simplejson as json

from django.urls import reverse


class CRUDFunctionalTest:
    """Tests for crud object functionality"""

    all_endpoint = None
    concrete_endpoint = None
    model = None

    def test_get_all_endpoint(self):
        """Test: does GET all endpoint return all model entries"""
        response = self._request_get_all_endpoint()
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_all_response())

    def get_all_response(self):
        """Returns response for GET request on all entries endpoint"""
        raise NotImplementedError

    def test_get_all_endpoint_with_bad_user(self):
        """Test: does GET all endpoint requested by bad user return no
        user entries"""
        self.client.login(username='baduser', password='badpass')
        response = self._request_get_all_endpoint()
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_all_bad_response())

    def _request_get_all_endpoint(self):
        """Request GET all endpoint"""
        return self.client.get(reverse(self.all_endpoint))

    def get_all_bad_response(self):
        """Returns bad response for GET request on all entries endpoint"""
        raise NotImplementedError

    def test_create_endpoint(self):
        response = self._request_create_endpoint()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.model.objects.count(), 2)

    def _request_create_endpoint(self):
        """Request POST on all endpoint"""
        return self.client.post(
            reverse(self.all_endpoint), self.get_create_data(),
            content_type='application/json'
        )

    def get_create_data(self):
        """Returns data for creating a new entry"""
        raise NotImplementedError

    def test_get_concrete_endpoint(self):
        response = self._request_get_concrete_endpoint()
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.serialized_entry)

    def test_get_concrete_endpoint_with_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        response = self._request_get_concrete_endpoint()
        self.assertEqual(response.status_code, 404)

    def _request_get_concrete_endpoint(self):
        """Request GET on concrete endpoint"""
        return self.client.get(
            reverse(self.concrete_endpoint, args=[self.entry.pk])
        )

    def test_delete_endpoint(self):
        response = self._request_delete_endpoint()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.model.objects.count(), 0)

    def test_delete_endpoint_with_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        response = self._request_delete_endpoint()
        self.assertEqual(response.status_code, 404)

    def _request_delete_endpoint(self):
        """Request DELETE on concrete endpoint"""
        return self.client.delete(
            reverse(self.concrete_endpoint, args=[self.entry.pk])
        )

    def test_update_endpoint(self):
        response = self._request_update_endpoint()
        self.assertEqual(response.status_code, 204)
        entry = self.model.objects.get(pk=self.entry.pk)
        self.assertNotEqual(str(self.entry), str(entry))

    def get_update_data(self):
        """Returns data for updating a concrete entry"""
        raise NotImplementedError

    def test_update_endpoint_with_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        response = self._request_update_endpoint()
        self.assertEqual(response.status_code, 404)

    def _request_update_endpoint(self):
        """Request PUT on concrete endpoint"""
        return self.client.put(
            reverse(self.concrete_endpoint, args=[self.entry.pk]),
            self.get_update_data(), content_type='application/json'
        )


class DateCRUDFunctionalTest(CRUDFunctionalTest):
    """Functional test with tests for getting by date"""

    month_endpoint = None
    date_endpoint = None

    def test_get_for_the_month(self):
        today = datetime.date.today()
        response = self._request_month_endpoint(today)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_month_response())

    def get_month_response(self):
        """Return response for GET request on month endpoint"""
        raise NotImplementedError

    def test_get_for_the_another_month(self):
        random_date = datetime.date(2020, 1, 1)
        response = self._request_month_endpoint(random_date)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_another_month_response())

    def _request_month_endpoint(self, date_obj: datetime.date):
        """Request GET on month endpoint"""
        return self.client.get(
            reverse(self.month_endpoint, args=[date_obj.year, date_obj.month])
        )

    def get_another_month_response(self):
        """Return response for GET request on another than today
        month endpoint"""
        raise NotImplementedError

    def test_get_for_the_today(self):
        today = datetime.date.today()
        response = self._request_date_endpoint(today)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_today_response())

    def get_today_response(self):
        """Get response for GET request on today date endpoint"""
        raise NotImplementedError

    def test_get_for_the_another_date(self):
        random_date = datetime.date(2020, 1, 1)
        response = self._request_date_endpoint(random_date)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.get_another_date_response())

    def _request_date_endpoint(self, date_obj: datetime.date):
        """Request GET on date endpoint"""
        return self.client.get(
            reverse(self.date_endpoint, args=[
                date_obj.year, date_obj.month, date_obj.day
            ])
        )

    def get_another_date_response(self):
        """Return response for GET reqeust on date endpoint with date
        another than today"""
        raise NotImplementedError
