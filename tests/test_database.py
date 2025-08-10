"""
Tests for database functionality
"""
import unittest
from unittest.mock import patch, MagicMock
from app.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db_manager = DatabaseManager()
    
    def test_mock_nodes(self):
        """Test mock nodes data"""
        nodes = self.db_manager._get_mock_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 0)
        
        for node in nodes:
            self.assertIn('node_id', node)
            self.assertIn('title', node)
            self.assertIn('location', node)
    
    def test_mock_node_info(self):
        """Test mock node info retrieval"""
        node_info = self.db_manager._get_mock_node_info('N1_1')
        self.assertIsNotNone(node_info)
        self.assertEqual(node_info['node_id'], 'N1_1')
        
        # Test non-existent node
        node_info = self.db_manager._get_mock_node_info('NON_EXISTENT')
        self.assertIsNone(node_info)
    
    def test_mock_node_history(self):
        """Test mock node history"""
        history = self.db_manager._get_mock_node_history('N1_1')
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        for reading in history:
            self.assertIn('node_id', reading)
            self.assertIn('timestamp', reading)
    
    def test_region_mapping(self):
        """Test region ID mapping"""
        # Test headquarters
        region_id = self.db_manager._get_region_id('Αρχηγείο / Ε.Σ.Κ.Ε.ΔΙ.Κ.')
        self.assertIsNone(region_id)
        
        # Test valid region
        region_id = self.db_manager._get_region_id('Ανατολικής Μακεδονίας και Θράκης')
        self.assertEqual(region_id, 'FR1')
        
        # Test invalid region
        region_id = self.db_manager._get_region_id('Invalid Region')
        self.assertIsNone(region_id)

if __name__ == '__main__':
    unittest.main() 