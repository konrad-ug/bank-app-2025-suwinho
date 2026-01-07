import unittest
from unittest.mock import patch
from src.account import Account
from src.companyaccount import CompanyAccount

class TestAccountEmail(unittest.TestCase):
    def setUp(self):
        self.email = "klient@example.com"

    @patch('src.account.datetime')
    @patch('src.account.SMTPClient')
    def test_send_history_personal_account(self, mock_smtp_class, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = '2025-12-10'
        
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.send.return_value = True

        account = Account("Jan", "Kowalski", "99123456789") 
        account.history = [100, -1, 500]

        result = account.send_history_via_email(self.email)

        self.assertTrue(result)
        mock_smtp_instance.send.assert_called_once_with(
            "Account Transfer History 2025-12-10",
            "Personal account history: [100, -1, 500]",
            self.email
        )

    @patch('src.companyaccount.CompanyAccount.check_nip_in_db')
    @patch('src.companyaccount.datetime')
    @patch('src.companyaccount.SMTPClient')
    def test_send_history_company_account(self, mock_smtp_class, mock_datetime, mock_check_nip):
        mock_check_nip.return_value = True

        mock_datetime.now.return_value.strftime.return_value = '2025-12-10'
        
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.send.return_value = False

        account = CompanyAccount("Januszex Sp. z o.o.", "8881112233")
        account.history = [5000, -1000]

        result = account.send_history_via_email(self.email)

        self.assertFalse(result)
        
        args = mock_smtp_instance.send.call_args[0]
        self.assertEqual(args[1], "Company account history: [5000, -1000]")

if __name__ == '__main__':
    unittest.main()