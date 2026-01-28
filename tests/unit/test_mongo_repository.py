from unittest.mock import Mock
from src.mongoAccountsRepository import MongoAccountsRepository
import pytest

def test_save_all_uses_collection_methods(mocker):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository()
    repo._collection = mock_collection
    
    mock_account = mocker.Mock()
    mock_account.pesel = "123"
    mock_account.to_dict.return_value = {"pesel": "123"}
    
    repo.save_all([mock_account])
    
    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.called

def test_load_all_converts_db_data_to_accounts(mocker):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository()
    repo._collection = mock_collection

    mock_db_data = [
        {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "12345678901",
            "balance": 500,
            "history": [500]
        }
    ]
    mock_collection.find.return_value = mock_db_data
    loaded_accounts = repo.load_all()

    assert len(loaded_accounts) == 1
    assert loaded_accounts[0].first_name == "Jan"
    assert loaded_accounts[0].balance == 500
    mock_collection.find.assert_called_once_with({})