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