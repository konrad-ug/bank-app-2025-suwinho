import pytest
from pytest_mock import MockFixture
from unittest.mock import patch
from src.companyaccount import CompanyAccount

class TestCompanyAccount:

    @pytest.fixture
    def default_company_name(self):
        return "MAREK"

    @pytest.fixture(autouse=True)
    def mock_api(self):
        with patch('src.companyaccount.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "result": {"subject": {"statusVat": "Czynny"}}
            }
            yield mock_get

    def test_create_company_account(self, default_company_name, mocker: MockFixture):
        mocker.patch.object(CompanyAccount, 'is_nip_valid', return_value = True)
        account = CompanyAccount(default_company_name, "1234567890")
        assert account.company_name == default_company_name
        assert account.nip == "1234567890"
        assert account.balance == 0

    @pytest.mark.parametrize("invalid_nip", [
        "123456789",       # Too short
        "1234567892131",   # Too long
        "1234567A90",      # Contains letter
        "12345-6789",      # Contains dash
        "1"                # Empty-ish
    ])
    def test_initialization_with_invalid_nip(self, default_company_name, invalid_nip, mock_api):
        account = CompanyAccount(default_company_name, invalid_nip)
        assert account.nip == "Invalid"

    @pytest.mark.parametrize("nip, api_status, should_raise_error", [
        ("1234567890", "Zwolniony", True),   # Should fail
        ("8461627563", "Czynny",    False),  # Should succeed
        ("9999999999", "Nie istnieje", True) # Should fail
    ])
    def test_checking_nip(self, mock_api, default_company_name, nip, api_status, should_raise_error):
        mock_api.return_value.json.return_value = {
            "result": {"subject": {"statusVat": api_status}}
        }


        if should_raise_error:
            with pytest.raises(ValueError, match="COMPANY NOT REGISTERED"):
                CompanyAccount(default_company_name, nip)
        else:
            account = CompanyAccount(default_company_name, nip)
            assert account.nip == nip