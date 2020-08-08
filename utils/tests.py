"""Module with tests utilities"""


class CRUDTests:

    def test_get_all(self):
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 1)
        self.assertEqual(all_instances[0], self.instance)

    def test_get_concrete(self):
        instance = self.service.get_concrete(self.instance.pk, self.user)
        self.assertEqual(instance, self.instance)

    def test_delete(self):
        self.service.delete(self.instance.pk, self.user)
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 0)

    def test_get_create_form(self):
        form = self.service.get_create_form()
        self.assertEqual(form.is_bound, False)

    def test_get_change_form(self):
        form = self.service.get_change_form(self.instance.pk, self.user)
        self.assertEqual(form.is_bound, True)


class DatesTests:

    def test_get_for_the_month(self):
        entries = self.service.get_for_the_month(self.user, self.today)
        self.assertEqual(entries[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        entries = self.service.get_for_the_date(
            self.user, self.today
        )
        self.assertEqual(entries[0].date, self.today)

