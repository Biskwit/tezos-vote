from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

# run this test with :
# pytest test.py


class TestContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.test = ContractInterface.create_from(
            join(project_dir, 'src/vote.tz'))

    def test_vote_1(self):
        u = "tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc"
        res = 1
        result = self.test.vote(
            1
        ).result(
            storage={
                "pause": True,
                "oui": 0,
                "non": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["oui"])

    def test_vote_2(self):
        u = "tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc"
        res = 1
        result = self.test.vote(
            2
        ).result(
            storage={
                "pause": True,
                "oui": 0,
                "non": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["non"])

    def test_vote_3(self):
        owner = "tz1hnAvAyuqGPvL8ncmjqVysCyVKi9CK6koG"
        res = 1
        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.vote(
                1
            ).result(
                storage={
                    "pause": True,
                    "oui": 0,
                    "non": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_vote_4(self):
        u = "tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc"
        res = 1
        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.vote(
                1
            ).result(
                storage={
                    "pause": False,
                    "oui": 0,
                    "non": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_reset_1(self):
        owner = "tz1hnAvAyuqGPvL8ncmjqVysCyVKi9CK6koG"
        result = self.test.reset(69).result(
            storage={
                "pause": False,
                "oui": 4,
                "non": 6,
                "voters": set()
            },
            sender = owner
        )
        self.assertEqual(0, result.storage["oui"])

    def test_reset_2(self):
        owner = "tz1hnAvAyuqGPvL8ncmjqVysCyVKi9CK6koG"

        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.reset(69).result(
                storage={
                    "pause": True,
                    "oui": 0,
                    "non": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_reset_3(self):
        u = "tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc"

        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.reset(69).result(
                storage={
                    "pause": True,
                    "oui": 0,
                    "non": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_stdby_1(self):
        owner = "tz1hnAvAyuqGPvL8ncmjqVysCyVKi9CK6koG"
        res = False
        result = self.test.pause("False").result(
                storage={
                    "pause":True,
                    "oui":0,
                    "non":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["oui"])
    
    def test_stdby_2(self):
        owner = "tz1hnAvAyuqGPvL8ncmjqVysCyVKi9CK6koG"
        res = True
        result = self.test.pause("True").result(
                storage={
                    "pause":False,
                    "oui":0,
                    "non":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["pause"])

