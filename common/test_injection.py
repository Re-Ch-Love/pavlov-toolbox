import unittest

from common.injection import SingletonManager


class TestInjectGlobalSingleton(unittest.TestCase):

    def test_01(self):
        singletonManager = SingletonManager()
        singletonManager.register(object())

        class TestCls:
            @singletonManager.inject(object)
            def obj(self):
                pass

        testCls1 = TestCls()
        self.assertFalse(testCls1.obj() is object())

    def test_02(self):
        singletonManager = SingletonManager()
        singletonManager.register(object())

        class TestCls:
            @singletonManager.inject(object)
            def obj(self):
                pass

        testCls1 = TestCls()
        testCls2 = TestCls()
        self.assertTrue(testCls1.obj() is testCls2.obj())

    def test_03(self):
        obj = object()
        singletonManager = SingletonManager()
        singletonManager.register(obj)

        class TestCls:
            @property
            @singletonManager.inject(object)
            def obj(self):
                pass
        
        self.assertTrue(TestCls().obj is obj)

if __name__ == "__main__":
    unittest.main()
