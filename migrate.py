#!/usr/bin/env python3
"""
Migration script to help transition from old structure to new professional structure
"""
import os
import shutil
from pathlib import Path

def backup_old_files():
    """Backup old files before migration"""
    backup_dir = Path('backup_old_structure')
    backup_dir.mkdir(exist_ok=True)
    
    old_files = ['App_test.py', 'DatabaseScript.py']
    
    for file in old_files:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"📦 Backed up {file} to {backup_dir}")
    
    print(f"✅ Backup completed in {backup_dir}")

def check_new_structure():
    """Check if new structure is properly set up"""
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/api.py',
        'app/database.py',
        'app/errors.py',
        'config.py',
        'run.py',
        'requirements.txt',
        'env.example',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files in new structure:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ New structure is properly set up")
    return True

def create_migration_guide():
    """Create a migration guide"""
    guide_content = """# Migration Guide

## From Old Structure to New Professional Structure

### What Changed

1. **Application Structure**
   - Old: Single `App_test.py` file
   - New: Modular blueprint-based structure in `app/` directory

2. **Database Management**
   - Old: `DatabaseScript.py` with global functions
   - New: `app/database.py` with `DatabaseManager` class

3. **Configuration**
   - Old: Hardcoded values in files
   - New: Environment-based configuration in `config.py`

4. **Entry Point**
   - Old: `python App_test.py`
   - New: `python run.py`

### Migration Steps

1. **Backup Old Files**
   - Old files are backed up in `backup_old_structure/`
   - You can safely delete them after confirming everything works

2. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the Application**
   ```bash
   python run.py
   ```

5. **Update Scripts/Deployment**
   - Update any deployment scripts to use `run.py` instead of `App_test.py`
   - Update environment variables as needed

### Key Benefits of New Structure

- **Modularity**: Blueprint-based organization
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new features
- **Testing**: Isolated components for testing
- **Configuration**: Environment-based settings
- **Professional Standards**: Follows Flask best practices

### Troubleshooting

If you encounter issues:

1. Check that all dependencies are installed
2. Verify your `.env` file is properly configured
3. Check logs for error messages
4. Ensure database connection is working

### Support

For help with migration, check the README.md file or contact the development team.
"""
    
    with open('MIGRATION_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("📝 Created MIGRATION_GUIDE.md")

def main():
    """Main migration function"""
    print("🔄 Starting migration to new professional structure...")
    print("=" * 60)
    
    # Backup old files
    backup_old_files()
    
    # Check new structure
    if not check_new_structure():
        print("❌ New structure is not properly set up")
        print("Please ensure all new files are created before running migration")
        return
    
    # Create migration guide
    create_migration_guide()
    
    print("\n" + "=" * 60)
    print("🎉 Migration preparation completed!")
    print("\n📋 Next steps:")
    print("1. Review MIGRATION_GUIDE.md")
    print("2. Set up your .env file")
    print("3. Test the new application with 'python run.py'")
    print("4. Update any deployment scripts")
    print("5. Remove old files when ready (they're backed up)")

if __name__ == '__main__':
    main() 