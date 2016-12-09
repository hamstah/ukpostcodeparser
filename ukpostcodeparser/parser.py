# Module     : postcode.py
# Synopsis   : UK postcode parser
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 14 April 2004
# Version    : 1.0
# Copyright  : Released to the public domain. Provided as-is, with no warranty.
# Notes      :
'''UK postcode parser

Provides the parse_uk_postcode function for parsing UK postcodes.'''

import re

from ukpostcodeparser import exceptions


# Build up the regex patterns piece by piece
POSTAL_ZONES = ['AB', 'AL', 'B' , 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR',
                'BS', 'BT', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT',
                'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
                'DY', 'E' , 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G' , 'GL',
                'GY', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HS', 'HU', 'HX',
                'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L' ,
                'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M' , 'ME', 'MK',
                'ML', 'N' , 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX',
                'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S' ,
                'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR',
                'SS', 'ST', 'SW', 'SY', 'TA', 'TD', 'TF', 'TN', 'TQ', 'TR',
                'TS', 'TW', 'UB', 'W' , 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
                'WS', 'WV', 'YO', 'ZE']
POSTAL_ZONES_ONE_CHAR = [zone for zone in POSTAL_ZONES if len(zone) == 1]
POSTAL_ZONES_TWO_CHARS = [zone for zone in POSTAL_ZONES if len(zone) == 2]
THIRD_POS_CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M',
                   'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
FOURTH_POS_CHARS = ['A', 'B', 'E', 'H', 'M', 'N', 'P', 'R', 'V', 'W', 'X',
                    'Y']
INCODE_CHARS = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'L', 'N', 'P', 'Q',
                'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
OUTCODE_PATTERN = (r'(' +
                   r'(?:(?:' +
                   '|'.join(POSTAL_ZONES_ONE_CHAR) +
                   r')(?:\d[' +
                   ''.join(THIRD_POS_CHARS) +
                   r']|\d{1,2}))' +
                   r'|' +
                   r'(?:(?:' +
                   '|'.join(POSTAL_ZONES_TWO_CHARS) +
                   r')(?:\d[' +
                   ''.join(FOURTH_POS_CHARS) +
                   r']|\d{1,2}))' +
                   r'|(?:BF1)' +  # special case for british forces postcodes
                   r')')
INCODE_PATTERN = (r'(\d[' +
                  ''.join(INCODE_CHARS) +
                  r'][' +
                  ''.join(INCODE_CHARS) +
                  r'])')
POSTCODE_PATTERN = OUTCODE_PATTERN + INCODE_PATTERN
STANDALONE_OUTCODE_PATTERN = OUTCODE_PATTERN + r'\s*$'

# Compile regexs
POSTCODE_REGEX = re.compile(POSTCODE_PATTERN)
STANDALONE_OUTCODE_REGEX = re.compile(STANDALONE_OUTCODE_PATTERN)


def parse_uk_postcode(postcode, strict=True, incode_mandatory=True):
    '''Split UK postcode into outcode and incode portions.

    Arguments:
    postcode            The postcode to be split.
    strict              If true, the postcode will be validated according to
                        the rules as specified at the Universal Postal Union[1]
                        and The UK Government Data Standards Catalogue[2]. If
                        the supplied postcode doesn't adhere to these rules a
                        ValueError will be thrown.
    incode_mandatory    If true, and only an outcode has been supplied, the
                        function will throw a ValueError.

    Returns:            outcode, incode

    Raises:             ValueError, if postcode is longer than seven
                        characters, or if 'strict' or 'incode_mandatory'
                        conditions are broken - see above.

    Usage example:      >>> from postcode import parse_uk_postcode
                        >>> parse_uk_postcode('cr0 2yr')
                        ('CR0', '2YR')
                        >>> parse_uk_postcode('cr0')
                        Traceback (most recent call last):
                          File "<interactive input>", line 1, in ?
                          File "postcode.py", line 101, in parse_uk_postcode
                            raise ValueError('Incode mandatory')
                        ValueError: Incode mandatory
                        >>> parse_uk_postcode('cr0', False, False)
                        ('CR0', '')

    [1] http://www.upu.int/fileadmin/documentsFiles/activities/addressingUnit/gbrEn.pdf
    [2] http://web.archive.org/web/20090930140939/http://www.govtalk.gov.uk/gdsc/html/noframes/PostCode-2-1-Release.htm
    '''

    postcode = postcode.replace(' ', '').upper()  # Normalize

    if len(postcode) > 7:
        raise exceptions.MaxLengthExceededError()

    # Validate postcode
    if strict:

        # Try for full postcode match
        postcode_match = POSTCODE_REGEX.match(postcode)
        if postcode_match:
            return postcode_match.group(1, 2)

        # Try for outcode only match
        outcode_match = STANDALONE_OUTCODE_REGEX.match(postcode)
        if outcode_match:
            if incode_mandatory:
                raise exceptions.IncodeNotFoundError('Incode mandatory')
            else:
                return outcode_match.group(1), ''

        # Try Girobank special case
        if postcode == 'GIR0AA':
            return 'GIR', '0AA'
        elif postcode == 'GIR':
            if incode_mandatory:
                raise exceptions.IncodeNotFoundError('Incode mandatory')
            else:
                return 'GIR', ''

        # None of the above
        raise exceptions.InvalidPostcodeError(
            'Value provided does not align with UK postcode rules'
        )

    # Just chop up whatever we've been given.
    else:
        # Outcode only
        if len(postcode) <= 4:
            if incode_mandatory:
                raise exceptions.IncodeNotFoundError('Incode mandatory')
            else:
                return postcode, ''
        # Full postcode
        else:
            return postcode[:-3], postcode[-3:]
