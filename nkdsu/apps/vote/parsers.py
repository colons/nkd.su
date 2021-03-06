from django.conf import settings

from sly import Lexer
from sly.lex import LexError


class ArtistLexer(Lexer):
    tokens = {
        ARTIST_COMPONENT, SPACE, COMMA, VIA, LPAREN, RPAREN, CV,  # type: ignore  # noqa
    }

    VIA = (
        r'\s+('
        r'from|'
        r'ft\.|'
        r'feat(\.|uring)?|'
        r'[Ss]tarring|'
        r'and|'
        r'with|'
        r'adding|'
        r'x|'
        r'×|'
        r'n\'|'
        r'vs\.?|'
        r'/|'
        r'&'
        r')\s+'
    )
    LPAREN = r'(?<=\s)\('
    RPAREN = r'\)(?=\s|,|\)|$)'
    CV = (
        r'('
        r'CV[.:]|'
        r'[Vv]ocal:|'
        r'[Mm]ain\svocals?:|'
        r'[Cc]omposed\sby|'
        r'[Ff]rom|'
        r'[Ff]eat(\.|uring)?|'
        r'Vo\.'
        r')\s+'
    )
    COMMA = r',(\sand)?\s+'
    SPACE = r'\s+'
    ARTIST_COMPONENT = (
        r'('
        r'AKIMA & NEOS|'
        r'ANNA TSUCHIYA inspi\' NANA\(BLACK STONES\)|'
        r'Carole\s&\sTuesday|'
        r'Daisy x Daisy|'
        r'Dejo & Bon|'
        r'Dimitri From Paris|'
        r'Fear,\sand\sLoathing\sin\sLas\sVegas|'
        r'GENERATIONS from EXILE TRIBE|'
        r'HIGH and MIGHTY COLOR|'
        r'Hello, Happy World!|'
        r'Kevin & Cherry|'
        r'King & Queen|'
        r'Kisida Kyodan & The Akebosi Rockets|'
        r'MYTH\s&\sROID|'
        r'OLIVIA inspi\' REIRA\(TRAPNEST\)|'
        r'Oranges\sand\sLemons|'
        r'Run Girls, Run!|'
        r'THE RAMPAGE from EXILE TRIBE|'
        r'Tackey & Tsubasa|'
        r'Voices From Mars|'
        r'Wake Up, [^\s]+!|'
        r'＊\(Asterisk\)|'
        r'[^\s,()]+'
        r')'
    )


artist_lexer = ArtistLexer()


def parse_artist(string, fail_silently=True):
    """
    Generate tuples of (whether or not this is the name of an arist,
    bit of this string), which when combined reform the original string handed
    in.
    """

    # look i don't understand how sly works, and i think i might need to spend
    # like a week learning BNF if i want to use its Parser interface, and even
    # then i don't know that it'd help us here, so im just gonna use the lexer
    # and hack the rest of this:

    try:
        tokens = list(artist_lexer.tokenize(string))
    except LexError as e:
        if fail_silently:
            if settings.DEBUG:
                print(e)
            yield (True, string)
            return
        else:
            raise e

    artist_parts = ('ARTIST_COMPONENT', 'SPACE')

    fragment = None

    for ti, token in enumerate(tokens):
        is_part_of_artist_name = (
            (token.type in artist_parts) and
            (
                (token.type != 'SPACE') or
                (
                    # if this is a space, then:
                    (
                        # be false if the next token isn't an artist component
                        (ti+1 < len(tokens)) and
                        (tokens[ti+1].type == 'ARTIST_COMPONENT')
                    ) and (
                        # or if the previous one wasn't, either
                        (ti > 0) and
                        (tokens[ti-1].type == 'ARTIST_COMPONENT')
                    )
                )
            )
        )

        if fragment:
            if is_part_of_artist_name == fragment[0]:
                fragment = (fragment[0], fragment[1] + token.value)
                continue

            yield fragment

        fragment = (is_part_of_artist_name, token.value)

    yield fragment
