"""Unit tests for DatabaseCore module"""

import pytest


class TestDatabaseCore:
    """Test DatabaseCore module"""

    def test_import_database_core(self):
        """Test that DatabaseCore can be imported"""
        from App.Core.Database import DatabaseCore
        assert DatabaseCore is not None

    def test_create_database_core_instance(self):
        """Test creating DatabaseCore instance"""
        from App.Core.Database import DatabaseCore

        core = DatabaseCore()
        assert core is not None

    def test_health_check_method_exists(self):
        """Test that health_check method exists"""
        from App.Core.Database import DatabaseCore

        assert hasattr(DatabaseCore, 'health_check')
        assert callable(getattr(DatabaseCore, 'health_check'))

    def test_get_connection_info_method_exists(self):
        """Test that get_connection_info method exists"""
        from App.Core.Database import DatabaseCore

        assert hasattr(DatabaseCore, 'get_connection_info')
        assert callable(getattr(DatabaseCore, 'get_connection_info'))

    def test_get_db_method_exists(self):
        """Test that get_db method exists"""
        from App.Core.Database import DatabaseCore

        assert hasattr(DatabaseCore, 'get_db')
        assert callable(getattr(DatabaseCore, 'get_db'))

    def test_commit_rollback_method_exists(self):
        """Test that commit_rollback method exists"""
        from App.Core.Database import DatabaseCore

        assert hasattr(DatabaseCore, 'commit_rollback')
        assert callable(getattr(DatabaseCore, 'commit_rollback'))
