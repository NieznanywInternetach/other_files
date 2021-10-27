"""#========================================================================================
Friend once asked me to help him with an online coding challenge
the point was to provide dynamic answer/string depending on number of likes one's tweet got
to_return is the static part for no/1/2/3 likes and brackets are meant to display names,
if the number is bigger, 3rd bracket should display number of the rest

I dubbed it as too simple though, so to make it more interesting I created system which
prints each and every name of user that liked the post.

Of course, doing so might create a lot of temporary strings, which if overwhelmingly present
can lead to running out of memory quite easily - to avoid it, many may find "".join(...) quite useful,
although it obscures the code, so if we omit talking about the overhead - custom context manager is the way

It's meant to store all the strings we want to add in a list, and when we're done it concatenates all of them
"""#========================================================================================

to_return = {
    0: "no one likes it",
    1: "{} likes it",
    2: "{} and {} like this",
    3: "{}, {} and {} like this"
}


class StringMerger:
    """
    A simple string merger utilizing power of string.join()
    uses simple concatenation operators with extendable API for error handling
    Usable withing with statement scope (WSS)
    """
    def __init__(self, init_string="", separator=""):
        self._string = init_string
        self._separator = separator
        self._to_merge_list = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_tb:
            self._string = self._separator.join([self._string, *self._to_merge_list])
            self._to_merge_list.clear()
            return True
        else:
            print(f"ERROR: {exc_type}, {exc_val}, {exc_tb}")
            return False

    def __add__(self, other):
        if isinstance(other, str):
            self._to_merge_list.append(other)
        else:
            raise TypeError(f"Only strings allowed, given value: {other}")

    def __iadd__(self, other):
        if isinstance(other, str):
            self._to_merge_list.append(other)
            return self
        else:
            raise TypeError(f"Only strings allowed, given value: {other}")

    def __str__(self): # for printing the string
        return self._string

    def get_string(self): # for managing the string further
        return self._string


def likes(names: list[str]) -> str:
    len_names = len(names)
    if len_names in to_return.keys():
        return to_return[len_names].format(*names)
    else:
        return "{}, {} and {} others like this".format(names[0], names[1], len_names-2)

def better_likes(names: list[str], tweet="You just made a new tweet! ") -> StringMerger:
    len_names = len(names)
    merger = StringMerger(init_string=tweet)
    with merger:
        if len_names in to_return.keys():
            merger += to_return[len_names].format(*names)
            return merger
        else:
            for idx, name in enumerate(names):
                if idx != len_names-2: # so we don't deal with "index out the scope" errors
                    merger += "{}, ".format(name)
                else:
                    merger += "{} and {} like it".format(names[idx], names[idx + 1])
                    return merger


if __name__ == "__main__":
    print("1", better_likes(["Astro", "Asone", "Niez", "Dummy", "Duckie", "Nom"], "Kona tweeted 'E'! "))
    temp = better_likes(["Kona"], "Niez tweeted 'A small step for humanity' ")
    temp += " 'but a step back for the code performance!'" # it's outside of the WSS so won't be printed
    print("2", temp)
    with temp: # unless you write another WSS
        temp += "\nAnd a chance for hidden 'bugs', lol."
        temp += " Check out where ended up the 'but...' part compared to the code"
    print("3", temp)