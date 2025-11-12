from src.companyaccount import CompanyAccount

class TestCompanyAccount:
    def test_create_company_account(self):
        account = CompanyAccount("MAREK","1234567890")
        assert account.company_name == "MAREK"
        assert account.nip == "1234567890"
        assert account.balance == 0
    
    def test_nip_too_short(self):
        account = CompanyAccount("MAREK","123456789")
        assert account.nip == "Invalid"

    def test_nip_too_long(self):
        account = CompanyAccount("MAREK","1234567892131")
        assert account.nip == "Invalid"
    
    def test_nip_contains_letter(self):
        account = CompanyAccount("MAREK","1234567A90")
        assert account.nip == "Invalid"
    
    def test_nip_with_special_characters(self):
        account = CompanyAccount("MAREK", "12345-6789")
        assert account.nip == "Invalid"