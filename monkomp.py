import os
from app import create_app

app = create_app("default")


@app.cli.command()
def test():
    """Run Test Suite"""
    import unittest

    try:
        os.remove("test-db.sqlite")
    except FileNotFoundError:
        pass
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
