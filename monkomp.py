import os
from app import create_app

app = create_app('default')

@app.cli.command()
def test():
    """Run Test Suite"""
    import unittest
    os.remove('test-db.sqlite')
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
