# -*- coding: UTF-8 -*-
#
# Copyright 2015-2021 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def pad(text, **kwargs):
    """ Return a padded text filled with a given character based on a given
    orientation.
    The padded text is sized by default as 79 characters to default as a valid
    pep8 line of code. Add a size parameter will change the padded text size.

    :param text: The text to be padded.
    :key fill: Character to be used to pad the text.
    :key orientation: Orientation to place the fill character. Default is
    'left' but it can be also 'center' and 'right'.
    :key size: Size to be used to pad the text. By default is 79.
    :return: A padded text. """
    size = kwargs.get("size", 79)
    fill = kwargs.get("fill", " ")
    orientation = kwargs.get("orientation", "left").lower()
    align = "<"
    if orientation == "center":
        align = "^"
    elif orientation == "right":
        align = ">"
    pad_format = "".join(["{0:{fill}{align}", str(size), "}"])
    return pad_format.format(text, fill=fill, align=align)


def columnize(text, **kwargs):
    """ Return a text broken in columns. The default columns size is 79 to be a
    valid pep8 line of code. Add the columns parameter to change this value.
    This function will analyze the text based on a category parameter.
    When category value is 'sequence' the text will be broken equally in lines
    with same columns(character length) size and last line could be smaller
    than columns value.
    When category value is 'phrase' or 'phrases' the function break lines
    observing words(sequence of characters separated by space). In this case
    the returned text could be padded by an orientation that could be 'left' or
    'center' or 'right' and filled by the fill character.
    The broken text is separated by a newline character.

    :param text: The one line text to break in columns.
    :key category: Category to decide the strategy to break the text in
    columns. Can be 'sequence' or 'phrase' or 'phrases'. Default is 'sequence'.
    :key fill: Character to be used to pad the text.
    :key orientation: Orientation to place the fill character. Default is
    None but it can be also 'left' or 'center' or 'right'.
    :key columns: Value to be used as size to break the text in columns. By
    default is 79.
    :key newline: Character to be used to break to a new line. Default is \n
    :return: A text broken in columns. """

    columns = kwargs.get("columns", 79)
    category = kwargs.get("category", "sequence").lower()
    newline = kwargs.get("newline", "\n")
    orientation = kwargs.get("orientation", None)
    fill = kwargs.get("fill", " ")
    text = text.replace("\n", "")

    if len(text) >= columns:
        broken_text = ""
        if category == "sequence":
            while len(text) > 0:
                if broken_text == "":
                    broken_text = text[0: columns]
                else:
                    chunk = None
                    if len(text) >= columns:
                        chunk = text[0: columns]
                    else:
                        chunk = text[0:]
                    broken_text = "{}{}{}".format(broken_text, newline, chunk)
                text = text[columns:]
        elif category == "phrase" or "phrases":
            text_x = text.split(" ")
            current_line = ""
            while len(text_x) > 0:
                if (len(current_line) + len(text_x[0])) < columns:
                    if current_line == "":
                        current_line = text_x.pop(0)
                    else:
                        current_line = "{} {}".format(
                            current_line, text_x.pop(0)
                        )
                else:
                    if orientation is not None:
                        current_line = pad(
                            current_line,
                            fill=fill,
                            orientation=orientation,
                            size=columns
                        )
                    if broken_text == "":
                        broken_text = current_line
                        current_line = ""
                    else:
                        broken_text = "{}{}{}".format(broken_text, newline,
                                                      current_line)
                        current_line = ""
        return broken_text
    return text
