import pytest
from src.companyaccount import CompanyAccount

class TestCompanyAccount:
    
    @pytest.fixture
    def default_company_name(self):
        return "MAREK"

    def test_create_company_account(self, default_company_name):
        account = CompanyAccount(default_company_name, "1234567890")
        assert account.company_name == default_company_name
        assert account.nip == "1234567890"
        assert account.balance == 0
    

    @pytest.mark.parametrize("invalid_nip", [
        "123456789",       # Za krótki
        "1234567892131",   # Za długi
        "1234567A90",      # Zawiera literę
        "12345-6789",      # Zawiera myślnik
        "1"                # Pusty string
        
    ])
    def test_initialization_with_invalid_nip(self, default_company_name, invalid_nip):
        account = CompanyAccount(default_company_name, invalid_nip)
        assert account.nip == "Invalid"