import re


def parse_integer(field):
    """
    Cast field value to integer.

    if field value is None, then we return 0. We consider None as 0

    Keyword arguments:
    field -- the field that contains the value to parse

    return
    The integer obtained from the cast or 0 when field value is None
    """

    field = str(field)
    if field == "None":
        return 0
    else:
        return int(field)


def reformat_ince_rink_xml(xml):
    """
    Reformat an ice rink xml in order to ease the parsing of an ice rink.

    This function will embed all the informations of an ice rink
    inside their own xml markup.
    The original ice rink xml is misformatted because all the ice rinks and
    their informations are put side by side and inside a single markup. So when
    we parse it raw, we can't distinguished the informations of a single ice
    rink because everything is gathered.

    Keyword arguments:
    xml -- the ice rink xml string

    return
    the xml string reformated correctly
    """

    xml = re.sub("\n", "", xml)
    xml = re.sub("> +<", "><", xml)
    xml = trim_space_in_name(xml)
    xml = re.sub(
        "</condition><nom_pat>",
        "</condition></patinoire><patinoire><nom_pat>",
        xml,
    )
    return xml


def trim_space_in_name(name):
    """Remove spaces in a name"""

    name = re.sub(" +- +", "-", name)
    name = re.sub("–", "-", name)
    return name
