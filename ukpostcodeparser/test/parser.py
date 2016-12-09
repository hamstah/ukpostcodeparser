import unittest
import inspect

from ukpostcodeparser import parse_uk_postcode
from ukpostcodeparser.exceptions import (
    InvalidPostcodeError, MaxLengthExceededError, IncodeNotFoundError
)


class BackwardsCompatibilityTestCase(unittest.TestCase):

    def test_incode_not_found_error_is_value_error(self):
        """
        Previous iterations of the code raised a ValueError exception when incode was expected but
        not found.
        New exceptions should be caught in the same way in case any code relies on it.
        """

        with self.assertRaises(ValueError) as cm:
            parse_uk_postcode('N16', True, True)
        self.assertEquals(cm.exception.__class__, IncodeNotFoundError)

    def test_max_length_exceeded_error_is_value_error(self):
        """
        Previous iterations of the code raised a ValueError when the postcode provided was too long.
        New exceptions should be caught in the same way in case any code relies on it.
        """

        with self.assertRaises(ValueError) as cm:
            parse_uk_postcode('N16 8QSSS', True, True)
        self.assertEquals(cm.exception.__class__, MaxLengthExceededError)

    def test_invalid_postcode_error_is_value_error(self):
        """
        Previous iterations of the code raised a ValueError when postcode was found to be invalid.
        New exceptions should be caught in the same way in case any code relies on it.
        """

        with self.assertRaises(ValueError) as cm:
            parse_uk_postcode('xx0 2yr', True, True)
        self.assertEquals(cm.exception.__class__, InvalidPostcodeError)


class PostcodeTestCase(unittest.TestCase):

    def run_parser(self, postcode, strict, incode_mandatory, expected):
        if inspect.isclass(expected) and issubclass(expected, Exception):
            try:
                parse_uk_postcode(postcode, strict, incode_mandatory)
            except expected:
                pass
            except Exception as e:
                m = '{!r} raised instead of expected {!r} for postcode={!r}, strict={!r} and' \
                    ' incode_mandatory={!r}'
                self.fail(m.format(
                    e.__class__.__name__, expected.__name__, postcode, strict, incode_mandatory
                ))

            else:
                m = '{!r} exception not raised for postcode={!r}, strict={!r} and ' \
                    'incode_mandatory={!r}'

                self.fail(m.format(expected.__name__, postcode, strict, incode_mandatory))

        else:

            result = parse_uk_postcode(postcode, strict, incode_mandatory)
            m = 'Expected {!r} but got {!r} for postcode={!r}, strict={!r} and ' \
                'incode_mandatory={!r}'

            self.assertEquals(
                expected,
                result,
                m.format(
                    expected, result, postcode, strict, incode_mandatory
                )
            )

    def test_001(self):
        self.run_parser(
            postcode='BF1 4BB',
            strict=False,
            incode_mandatory=False,
            expected=('BF1', '4BB')
        )

    def test_002(self):
        self.run_parser(
            postcode='BF2 4BB',
            strict=False,
            incode_mandatory=False,
            expected=('BF2', '4BB')
        )

    def test_003(self):
        self.run_parser(
            postcode='cr0 2yr',
            strict=False,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_004(self):
        self.run_parser(
            postcode='CR0 2YR',
            strict=False,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_005(self):
        self.run_parser(
            postcode='cr02yr',
            strict=False,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_006(self):
        self.run_parser(
            postcode='dn16 9aa',
            strict=False,
            incode_mandatory=False,
            expected=('DN16', '9AA')
        )

    def test_007(self):
        self.run_parser(
            postcode='dn169aa',
            strict=False,
            incode_mandatory=False,
            expected=('DN16', '9AA')
        )

    def test_008(self):
        self.run_parser(
            postcode='ec1a 1hq',
            strict=False,
            incode_mandatory=False,
            expected=('EC1A', '1HQ')
        )

    def test_009(self):
        self.run_parser(
            postcode='ec1a1hq',
            strict=False,
            incode_mandatory=False,
            expected=('EC1A', '1HQ')
        )

    def test_010(self):
        self.run_parser(
            postcode='m2 5bq',
            strict=False,
            incode_mandatory=False,
            expected=('M2', '5BQ')
        )

    def test_011(self):
        self.run_parser(
            postcode='m25bq',
            strict=False,
            incode_mandatory=False,
            expected=('M2', '5BQ')
        )

    def test_012(self):
        self.run_parser(
            postcode='m34 4ab',
            strict=False,
            incode_mandatory=False,
            expected=('M34', '4AB')
        )

    def test_013(self):
        self.run_parser(
            postcode='m344ab',
            strict=False,
            incode_mandatory=False,
            expected=('M34', '4AB')
        )

    def test_014(self):
        self.run_parser(
            postcode='sw19 2et',
            strict=False,
            incode_mandatory=False,
            expected=('SW19', '2ET')
        )

    def test_015(self):
        self.run_parser(
            postcode='sw192et',
            strict=False,
            incode_mandatory=False,
            expected=('SW19', '2ET')
        )

    def test_016(self):
        self.run_parser(
            postcode='w1a 4zz',
            strict=False,
            incode_mandatory=False,
            expected=('W1A', '4ZZ')
        )

    def test_017(self):
        self.run_parser(
            postcode='w1a4zz',
            strict=False,
            incode_mandatory=False,
            expected=('W1A', '4ZZ')
        )

    def test_018(self):
        self.run_parser(
            postcode='cr0',
            strict=False,
            incode_mandatory=False,
            expected=('CR0', '')
        )

    def test_019(self):
        self.run_parser(
            postcode='sw19',
            strict=False,
            incode_mandatory=False,
            expected=('SW19', '')
        )

    def test_020(self):
        self.run_parser(
            postcode='xx0 2yr',
            strict=False,
            incode_mandatory=False,
            expected=('XX0', '2YR')
        )

    def test_021(self):
        self.run_parser(
            postcode='3r0 2yr',
            strict=False,
            incode_mandatory=False,
            expected=('3R0', '2YR')
        )

    def test_022(self):
        self.run_parser(
            postcode='20 2yr',
            strict=False,
            incode_mandatory=False,
            expected=('20', '2YR')
        )

    def test_023(self):
        self.run_parser(
            postcode='3r0 ayr',
            strict=False,
            incode_mandatory=False,
            expected=('3R0', 'AYR')
        )

    def test_024(self):
        self.run_parser(
            postcode='3r0 22r',
            strict=False,
            incode_mandatory=False,
            expected=('3R0', '22R')
        )

    def test_025(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=False,
            incode_mandatory=False,
            expected=('W1M', '4ZZ')
        )

    def test_026(self):
        self.run_parser(
            postcode='3r0',
            strict=False,
            incode_mandatory=False,
            expected=('3R0', '')
        )

    def test_027(self):
        self.run_parser(
            postcode='ec1c 1hq',
            strict=False,
            incode_mandatory=False,
            expected=('EC1C', '1HQ')
        )

    def test_028(self):
        self.run_parser(
            postcode='m344cb',
            strict=False,
            incode_mandatory=False,
            expected=('M34', '4CB')
        )

    def test_029(self):
        self.run_parser(
            postcode='gir 0aa',
            strict=False,
            incode_mandatory=False,
            expected=('GIR', '0AA')
        )

    def test_030(self):
        self.run_parser(
            postcode='gir',
            strict=False,
            incode_mandatory=False,
            expected=('GIR', '')
        )

    def test_031(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=False,
            incode_mandatory=False,
            expected=('W1M', '4ZZ')
        )

    def test_032(self):
        self.run_parser(
            postcode='w1m',
            strict=False,
            incode_mandatory=False,
            expected=('W1M', '')
        )

    def test_033(self):
        self.run_parser(
            postcode='dn169aaA',
            strict=False,
            incode_mandatory=False,
            expected=MaxLengthExceededError
        )

    def test_034(self):
        self.run_parser(
            postcode='BF1 4BB',
            strict=False,
            incode_mandatory=True,
            expected=('BF1', '4BB')
        )

    def test_035(self):
        self.run_parser(
            postcode='BF2 4BB',
            strict=False,
            incode_mandatory=True,
            expected=('BF2', '4BB')
        )

    def test_036(self):
        self.run_parser(
            postcode='cr0 2yr',
            strict=False,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_037(self):
        self.run_parser(
            postcode='CR0 2YR',
            strict=False,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_038(self):
        self.run_parser(
            postcode='cr02yr',
            strict=False,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_039(self):
        self.run_parser(
            postcode='dn16 9aa',
            strict=False,
            incode_mandatory=True,
            expected=('DN16', '9AA')
        )

    def test_040(self):
        self.run_parser(
            postcode='dn169aa',
            strict=False,
            incode_mandatory=True,
            expected=('DN16', '9AA')
        )

    def test_041(self):
        self.run_parser(
            postcode='ec1a 1hq',
            strict=False,
            incode_mandatory=True,
            expected=('EC1A', '1HQ')
        )

    def test_042(self):
        self.run_parser(
            postcode='ec1a1hq',
            strict=False,
            incode_mandatory=True,
            expected=('EC1A', '1HQ')
        )

    def test_043(self):
        self.run_parser(
            postcode='m2 5bq',
            strict=False,
            incode_mandatory=True,
            expected=('M2', '5BQ')
        )

    def test_044(self):
        self.run_parser(
            postcode='m25bq',
            strict=False,
            incode_mandatory=True,
            expected=('M2', '5BQ')
        )

    def test_045(self):
        self.run_parser(
            postcode='m34 4ab',
            strict=False,
            incode_mandatory=True,
            expected=('M34', '4AB')
        )

    def test_046(self):
        self.run_parser(
            postcode='m344ab',
            strict=False,
            incode_mandatory=True,
            expected=('M34', '4AB')
        )

    def test_047(self):
        self.run_parser(
            postcode='sw19 2et',
            strict=False,
            incode_mandatory=True,
            expected=('SW19', '2ET')
        )

    def test_048(self):
        self.run_parser(
            postcode='sw192et',
            strict=False,
            incode_mandatory=True,
            expected=('SW19', '2ET')
        )

    def test_049(self):
        self.run_parser(
            postcode='w1a 4zz',
            strict=False,
            incode_mandatory=True,
            expected=('W1A', '4ZZ')
        )

    def test_050(self):
        self.run_parser(
            postcode='w1a4zz',
            strict=False,
            incode_mandatory=True,
            expected=('W1A', '4ZZ')
        )

    def test_051(self):
        self.run_parser(
            postcode='cr0',
            strict=False,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_052(self):
        self.run_parser(
            postcode='sw19',
            strict=False,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_053(self):
        self.run_parser(
            postcode='xx0 2yr',
            strict=False,
            incode_mandatory=True,
            expected=('XX0', '2YR')
        )

    def test_054(self):
        self.run_parser(
            postcode='3r0 2yr',
            strict=False,
            incode_mandatory=True,
            expected=('3R0', '2YR')
        )

    def test_055(self):
        self.run_parser(
            postcode='20 2yr',
            strict=False,
            incode_mandatory=True,
            expected=('20', '2YR')
        )

    def test_056(self):
        self.run_parser(
            postcode='3r0 ayr',
            strict=False,
            incode_mandatory=True,
            expected=('3R0', 'AYR')
        )

    def test_057(self):
        self.run_parser(
            postcode='3r0 22r',
            strict=False,
            incode_mandatory=True,
            expected=('3R0', '22R')
        )

    def test_058(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=False,
            incode_mandatory=True,
            expected=('W1M', '4ZZ')
        )

    def test_059(self):
        self.run_parser(
            postcode='3r0',
            strict=False,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_060(self):
        self.run_parser(
            postcode='ec1c 1hq',
            strict=False,
            incode_mandatory=True,
            expected=('EC1C', '1HQ')
        )

    def test_061(self):
        self.run_parser(
            postcode='m344cb',
            strict=False,
            incode_mandatory=True,
            expected=('M34', '4CB')
        )

    def test_062(self):
        self.run_parser(
            postcode='gir 0aa',
            strict=False,
            incode_mandatory=True,
            expected=('GIR', '0AA')
        )

    def test_063(self):
        self.run_parser(
            postcode='gir',
            strict=False,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_064(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=False,
            incode_mandatory=True,
            expected=('W1M', '4ZZ')
        )

    def test_065(self):
        self.run_parser(
            postcode='w1m',
            strict=False,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_066(self):
        self.run_parser(
            postcode='dn169aaA',
            strict=False,
            incode_mandatory=True,
            expected=MaxLengthExceededError
        )

    def test_067(self):
        self.run_parser(
            postcode='BF1 4BB',
            strict=True,
            incode_mandatory=False,
            expected=('BF1', '4BB')
        )

    def test_068(self):
        self.run_parser(
            postcode='BF2 4BB',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_069(self):
        self.run_parser(
            postcode='cr0 2yr',
            strict=True,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_070(self):
        self.run_parser(
            postcode='CR0 2YR',
            strict=True,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_071(self):
        self.run_parser(
            postcode='cr02yr',
            strict=True,
            incode_mandatory=False,
            expected=('CR0', '2YR')
        )

    def test_072(self):
        self.run_parser(
            postcode='dn16 9aa',
            strict=True,
            incode_mandatory=False,
            expected=('DN16', '9AA')
        )

    def test_073(self):
        self.run_parser(
            postcode='dn169aa',
            strict=True,
            incode_mandatory=False,
            expected=('DN16', '9AA')
        )

    def test_074(self):
        self.run_parser(
            postcode='ec1a 1hq',
            strict=True,
            incode_mandatory=False,
            expected=('EC1A', '1HQ')
        )

    def test_075(self):
        self.run_parser(
            postcode='ec1a1hq',
            strict=True,
            incode_mandatory=False,
            expected=('EC1A', '1HQ')
        )

    def test_076(self):
        self.run_parser(
            postcode='m2 5bq',
            strict=True,
            incode_mandatory=False,
            expected=('M2', '5BQ')
        )

    def test_077(self):
        self.run_parser(
            postcode='m25bq',
            strict=True,
            incode_mandatory=False,
            expected=('M2', '5BQ')
        )

    def test_078(self):
        self.run_parser(
            postcode='m34 4ab',
            strict=True,
            incode_mandatory=False,
            expected=('M34', '4AB')
        )

    def test_079(self):
        self.run_parser(
            postcode='m344ab',
            strict=True,
            incode_mandatory=False,
            expected=('M34', '4AB')
        )

    def test_080(self):
        self.run_parser(
            postcode='sw19 2et',
            strict=True,
            incode_mandatory=False,
            expected=('SW19', '2ET')
        )

    def test_081(self):
        self.run_parser(
            postcode='sw192et',
            strict=True,
            incode_mandatory=False,
            expected=('SW19', '2ET')
        )

    def test_082(self):
        self.run_parser(
            postcode='w1a 4zz',
            strict=True,
            incode_mandatory=False,
            expected=('W1A', '4ZZ')
        )

    def test_083(self):
        self.run_parser(
            postcode='w1a4zz',
            strict=True,
            incode_mandatory=False,
            expected=('W1A', '4ZZ')
        )

    def test_084(self):
        self.run_parser(
            postcode='cr0',
            strict=True,
            incode_mandatory=False,
            expected=('CR0', '')
        )

    def test_085(self):
        self.run_parser(
            postcode='sw19',
            strict=True,
            incode_mandatory=False,
            expected=('SW19', '')
        )

    def test_086(self):
        self.run_parser(
            postcode='xx0 2yr',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_087(self):
        self.run_parser(
            postcode='3r0 2yr',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_088(self):
        self.run_parser(
            postcode='20 2yr',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_089(self):
        self.run_parser(
            postcode='3r0 ayr',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_090(self):
        self.run_parser(
            postcode='3r0 22r',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_091(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_092(self):
        self.run_parser(
            postcode='3r0',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_093(self):
        self.run_parser(
            postcode='ec1c 1hq',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_094(self):
        self.run_parser(
            postcode='m344cb',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_095(self):
        self.run_parser(
            postcode='gir 0aa',
            strict=True,
            incode_mandatory=False,
            expected=('GIR', '0AA')
        )

    def test_096(self):
        self.run_parser(
            postcode='gir',
            strict=True,
            incode_mandatory=False,
            expected=('GIR', '')
        )

    def test_097(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_098(self):
        self.run_parser(
            postcode='w1m',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )

    def test_099(self):
        self.run_parser(
            postcode='dn169aaA',
            strict=True,
            incode_mandatory=False,
            expected=MaxLengthExceededError
        )

    def test_100(self):
        self.run_parser(
            postcode='BF1 4BB',
            strict=True,
            incode_mandatory=True,
            expected=('BF1', '4BB')
        )

    def test_101(self):
        self.run_parser(
            postcode='BF1 ERR',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_102(self):
        self.run_parser(
            postcode='BF2 4BB',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_103(self):
        self.run_parser(
            postcode='cr0 2yr',
            strict=True,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_104(self):
        self.run_parser(
            postcode='CR0 2YR',
            strict=True,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_105(self):
        self.run_parser(
            postcode='cr02yr',
            strict=True,
            incode_mandatory=True,
            expected=('CR0', '2YR')
        )

    def test_106(self):
        self.run_parser(
            postcode='dn16 9aa',
            strict=True,
            incode_mandatory=True,
            expected=('DN16', '9AA')
        )

    def test_107(self):
        self.run_parser(
            postcode='dn169aa',
            strict=True,
            incode_mandatory=True,
            expected=('DN16', '9AA')
        )

    def test_108(self):
        self.run_parser(
            postcode='ec1a 1hq',
            strict=True,
            incode_mandatory=True,
            expected=('EC1A', '1HQ')
        )

    def test_109(self):
        self.run_parser(
            postcode='ec1a1hq',
            strict=True,
            incode_mandatory=True,
            expected=('EC1A', '1HQ')
        )

    def test_110(self):
        self.run_parser(
            postcode='m2 5bq',
            strict=True,
            incode_mandatory=True,
            expected=('M2', '5BQ')
        )

    def test_111(self):
        self.run_parser(
            postcode='m25bq',
            strict=True,
            incode_mandatory=True,
            expected=('M2', '5BQ')
        )

    def test_112(self):
        self.run_parser(
            postcode='m34 4ab',
            strict=True,
            incode_mandatory=True,
            expected=('M34', '4AB')
        )

    def test_113(self):
        self.run_parser(
            postcode='m344ab',
            strict=True,
            incode_mandatory=True,
            expected=('M34', '4AB')
        )

    def test_114(self):
        self.run_parser(
            postcode='sw19 2et',
            strict=True,
            incode_mandatory=True,
            expected=('SW19', '2ET')
        )

    def test_115(self):
        self.run_parser(
            postcode='sw192et',
            strict=True,
            incode_mandatory=True,
            expected=('SW19', '2ET')
        )

    def test_116(self):
        self.run_parser(
            postcode='w1a 4zz',
            strict=True,
            incode_mandatory=True,
            expected=('W1A', '4ZZ')
        )

    def test_117(self):
        self.run_parser(
            postcode='w1a4zz',
            strict=True,
            incode_mandatory=True,
            expected=('W1A', '4ZZ')
        )

    def test_118(self):
        self.run_parser(
            postcode='cr0',
            strict=True,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_119(self):
        self.run_parser(
            postcode='sw19',
            strict=True,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_120(self):
        self.run_parser(
            postcode='xx0 2yr',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_121(self):
        self.run_parser(
            postcode='3r0 2yr',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_122(self):
        self.run_parser(
            postcode='20 2yr',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_123(self):
        self.run_parser(
            postcode='3r0 ayr',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_124(self):
        self.run_parser(
            postcode='3r0 22r',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_125(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_126(self):
        self.run_parser(
            postcode='3r0',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_127(self):
        self.run_parser(
            postcode='ec1c 1hq',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_128(self):
        self.run_parser(
            postcode='m344cb',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_129(self):
        self.run_parser(
            postcode='gir 0aa',
            strict=True,
            incode_mandatory=True,
            expected=('GIR', '0AA')
        )

    def test_130(self):
        self.run_parser(
            postcode='gir',
            strict=True,
            incode_mandatory=True,
            expected=IncodeNotFoundError
        )

    def test_131(self):
        self.run_parser(
            postcode='w1m 4zz',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_132(self):
        self.run_parser(
            postcode='w1m',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_133(self):
        self.run_parser(
            postcode='dn169aaA',
            strict=True,
            incode_mandatory=True,
            expected=MaxLengthExceededError
        )

    def test_134(self):
        self.run_parser(
            postcode='N1P 2ZX',
            strict=True,
            incode_mandatory=False,
            expected=('N1P', '2ZX')
        )

    def test_135(self):
        self.run_parser(
            postcode='n1p',
            strict=True,
            incode_mandatory=False,
            expected=('N1P', '')
        )

    def test_136(self):
        self.run_parser(
            postcode='n1p1gw',
            strict=True,
            incode_mandatory=True,
            expected=('N1P', '1GW')
        )

    def test_137(self):
        self.run_parser(
            postcode='NPT 0DT',
            strict=True,
            incode_mandatory=True,
            expected=InvalidPostcodeError
        )

    def test_138(self):
        self.run_parser(
            postcode='npt',
            strict=True,
            incode_mandatory=False,
            expected=InvalidPostcodeError
        )
