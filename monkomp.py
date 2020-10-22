from app import create_app


app = create_app('default')
# app.run()

@app.cli.command()
def test():
    """Run Test Suite"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)