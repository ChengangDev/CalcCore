import unittest
from operate.observe import Observer, CliffObserver

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)
        ob = Observer(30)
        # ob.watch_history_ticks('600004', '2017-06-12')
        # ob.watch_history_ticks('002415', '2017-06-12')
        # ob.watch_history_ticks('000858', '2017-06-12')
        ob = CliffObserver('600988', '2017-06-14')
        ob.simulate(fetch_interval=0)
        ob.show()


if __name__ == "__main__":
    unittest.main()

    #ob.review('000858', '2017-06-14')
    #ts.get_realtime_quotes('000858')
