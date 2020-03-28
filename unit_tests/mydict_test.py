import os
import sys
print("***获取当前目录***")
print(os.getcwd())
sys.path.append(os.getcwd()+"/unit_tests")
try:
    from mydict import Dict
except Exception as e:
    print(e)
import unittest
import logging
logging.basicConfig(level=logging.INFO)
#启动Python解释器时可以用-O参数来关闭assert
#编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。
class TestDict(unittest.TestCase):

    def test_init(self):
        d = Dict(a=1, b='test')
        #最常用的断言就是assertEqual()
        try:
            self.assertEqual(d.a, 1)
            logging.info("[*]self.assertEqual(d.a, 1), [secuess]")
        except Exception as e:
            logging.exception(e)
             
        try:
            self.assertEqual(d.a, 2)
            logging.info("[*]self.assertEqual(d.a, 2), [secuess]")
        except Exception as e:
            logging.exception(e)
            pass

        try:    
            self.assertEqual(d.b, 'test')
            logging.info("[*]self.assertEqual(d.b, 'test'), [secuess]")
        except Exception as e:
            logging.exception(e)

        try:    
            self.assertTrue(isinstance(d, dict))
            logging.info("[*]self.assertTrue(isinstance(d, dict)), [secuess]")
        except Exception as e:
            logging.exception(e)


    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

    def main(self):
        self.test_init()
        self.test_key()
        self.test_attr()
        self.test_keyerror()
        self.test_attrerror()

#另一种方法是在命令行通过参数-m unittest直接运行单元测试,例如python3 -m unittest mydict_test
if __name__ == '__main__':
    t =TestDict()
    TestDict.main(t)