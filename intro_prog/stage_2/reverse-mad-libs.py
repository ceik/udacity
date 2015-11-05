# Reverse Mads Libs Generator

texts = [('The best __1__ against __2__ is a five-__3__ __4__ '
    'with the average __5__.'),
    ('Allow __1__ to be in your __2__ that you can not __3__ out on in '
    '__4__ seconds flat if you __5__ the heat around the __6__.'),
    ('Those who find __1__ meanings in beautiful things are __2__ without being '
    'charming. This is a fault. Those who find __3__ meanings in beautiful '
    'things are the __4__. For these there is __5__. They are the elect to whom '
    'beautiful things mean only Beauty. There is no such thing as a __6__ or an '
    '__7__ book. Books are well written, or badly written. That is all.')]

replacements = [['argument', 'democracy', 'minute', 'conversation', 'voter'],
                ['nothing', 'life', 'walk', 'thirty', 'spot', 'corner'],
                ['ugly', 'corrupt', 'beautiful', 'cultivated', 'hope', 'moral',
                'immoral']]

def set_difficulty():
    """Lets user set difficulty, makes sure the choice is valid, and then
    returns an index that corresponds to the difficulty."""
    mapping = {'easy': 0, 'medium': 1, 'hard': 2}
    diff = ''
    while diff not in ['easy', 'medium', 'hard']:
        diff = raw_input('Please select difficulty (easy/medium/hard):')
    print '\n'
    return mapping[diff]

class Sentence:
    def __init__(self, text, replacements):
        """Creates the sentence object with the text and replacements
        attributes."""
        self.text = text
        self.replacements = replacements

    def blank_replace(self, blank_no, guess):
        """Tries to insert a given guess into the given blank. If if fits the
        insert is made and the number 1 returned. Returns 0 if it doesn't fit."""
        if guess == self.replacements[blank_no]:
            self.text = self.text.replace("__" + str(blank_no + 1) + "__",
                guess)
            return 1
        else:
            return 0

def main():
    """Run the reverse mad libs game."""
    diff = set_difficulty()
    sent = Sentence(texts[diff], replacements[diff])
    counter = 0
    print sent.text, '\n'
    while counter < len(sent.replacements):
        guess = raw_input(('Please guess what should go in blank '
            'number {}: ').format(counter + 1))
        counter += sent.blank_replace(counter, guess)
        print '\n', sent.text, '\n'

main()
