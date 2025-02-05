
import subprocess

"""Helper functions, decorators,... for working with locales"""

def get_avail_locales():
    return {loc.decode(errors="replace").strip() for loc in subprocess.check_output(["locale", "-a"]).split()}


def missing_locales(required, available):
    canon_locales = {loc.replace("UTF-8", "utf8") for loc in required}
    return canon_locales - set(available)


def requires_locales(locales):
    """A decorator factory to skip tests that require unavailable locales

    :param set locales: set of required locales

    **Requires the test to have the set of available locales defined as its
    ``avail_locales`` attribute.**

    """

    def decorator(test_method):
        def decorated(test, *args):
            missing = missing_locales(locales, test.avail_locales)
            if missing:
                test.skipTest("requires missing locales: %s" % missing)
            else:
                return test_method(test, *args)

        return decorated

    return decorator
